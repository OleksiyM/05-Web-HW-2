import json
import logging
from datetime import datetime

import aiofiles
import aiohttp

from DateHandler import DateHandler
from constants import BASE_CURRENCIES, ALL_CURRENCIES, MAX_ARCHIVE_DAYS, LOG_FILE, BANK_URL, MAX_ARCHIVE_DAYS

logger = logging.getLogger(__name__)


class HttpGetError(Exception):
    ...


def check_all_currencies(param: str) -> list:
    if param.lower() == 'all':
        logger.debug(f"Using all currencies for exchange rate data retrieval: {ALL_CURRENCIES}")
        return ALL_CURRENCIES
    else:
        logger.debug(f"Using base currencies for exchange rate data retrieval: {BASE_CURRENCIES}")
        return BASE_CURRENCIES


def check_days(days: str) -> int:
    try:
        days = int(days)
    except ValueError:
        logger.info("Invalid input for days. Using default value (0).")
        return 0

    days = min(max(days, 0), MAX_ARCHIVE_DAYS)  # valid range (0-10)

    if days != 0:
        logger.debug(f"Using {days} days for exchange rate data retrieval.")
    else:
        logger.debug("Using current day for exchange rate data.")

    return days


def create_storage_dir(storage_dir):
    if not storage_dir.exists():
        storage_dir.mkdir()


def save_data_to_file(r, filename):
    with open(filename, 'w') as file:
        json.dump(r, file, ensure_ascii=False, indent=4)
        # file.write(str(r))


async def generate_html_table_1(data: list) -> str:
    html_table = ""
    for item in data:
        date, currency_rates = list(item.items())[0]

        html_table += f"<h3>{date}:</h3>\n"
        html_table += "<table>\n"
        html_table += "<thead>\n"
        html_table += "<tr>\n"
        html_table += "<th>Currency</th>\n"
        html_table += "<th>Sale</th>\n"
        html_table += "<th>Purchase</th>\n"
        html_table += "</tr>\n"
        html_table += "</thead>\n"
        html_table += "<tbody>\n"

        for currency, rates in currency_rates.items():
            html_table += "<tr>\n"
            html_table += f"<td>{currency}</td>\n"
            html_table += f"<td>{rates['sale']}</td>\n"
            html_table += f"<td>{rates['purchase']}</td>\n"
            html_table += "</tr>\n"

        html_table += "</tbody>\n"
        html_table += "</table>\n"

    return html_table


from markupsafe import Markup


async def generate_html_table(data: list) -> str:
    html_table = ""
    for item in data:
        date, currency_rates = list(item.items())[0]

        html_table += f"<h3>{date}:</h3>\n"
        html_table += Markup("<table>\n")
        html_table += Markup("<thead>\n")
        html_table += Markup("<tr>\n")
        html_table += Markup("<th>Currency</th>\n")
        html_table += Markup("<th>Sale</th>\n")
        html_table += Markup("<th>Purchase</th>\n")
        html_table += Markup("</tr>\n")
        html_table += Markup("</thead>\n")
        html_table += Markup("<tbody>\n")

        for currency, rates in currency_rates.items():
            html_table += Markup("<tr>\n")
            html_table += Markup(f"<td>{currency}</td>\n")
            html_table += Markup(f"<td>{rates['sale']}</td>\n")
            html_table += Markup(f"<td>{rates['purchase']}</td>\n")
            html_table += Markup("</tr>\n")

        html_table += Markup("</tbody>\n")
        html_table += Markup("</table>\n")

    return str(html_table)


async def generate_text_table_html(data) -> list:
    text_table = []
    for item in data:
        date, currency_rates = list(item.items())[0]
        text_table.append(' \n')
        text_table.append(f'{date}:\n')
        text_table.append("Cur Sale  Purchase\n")
        text_table.append("------------------\n")

        for currency, rates in currency_rates.items():
            text_table.append(f"{currency:<10}  {rates['sale']:>5.2f}  {rates['purchase']:>8.2f}\n")

        text_table.append("\n")

    return text_table


async def generate_text_table_console(data):
    text_table = ""
    for item in data:
        date, currency_rates = list(item.items())[0]

        text_table += f"{date}:\n"
        text_table += Markup("Currency  Sale  Purchase\n")
        text_table += Markup("--------  ----  --------\n")

        for currency, rates in currency_rates.items():
            text_table += Markup(f"{currency:<10}  {rates['sale']:>5.2f}  {rates['purchase']:>8.2f}\n")

        text_table += Markup("\n")

    return str(text_table)


async def check_day_range(day):
    days = min(max(day, 0), MAX_ARCHIVE_DAYS)  # valid range (0-10)
    # if day < 0 or day > MAX_ARCHIVE_DAYS:
    #     return 0
    return days


async def check_exchange_message(message: str) -> [bool, int, tuple()]:
    command, *params = message.split()

    if command.lower() == "exchange":
        logger.debug(f'{params=}')

        days = 0  # Default value for days
        currencies = BASE_CURRENCIES  # Default currencies

        if params:
            if params[0].isdigit():
                days = int(params[0])
            else:
                if params[0].lower() == "all":
                    currencies = ALL_CURRENCIES

            # Handle "all" keyword only if it's not the first argument
            if len(params) >= 2 and params[1].lower() == "all":
                currencies = ALL_CURRENCIES
        # days should be in 0-10
        days = await check_day_range(days)
        return [True, days, currencies]

    return [False, 0, BASE_CURRENCIES]


async def handle_exchange(message):
    logger = logging.getLogger("exchange")

    async with aiofiles.open(LOG_FILE, "a") as log_file:
        logger.info("Exchange command executed\n")
        await log_file.write(f"{datetime.now()} Exchange command: {message}\n")


async def get_data(days, currencies):
    date_handler = DateHandler()
    output_list = []
    current_day = 0
    async for day in date_handler.dates_list(days):  # Use async for loop
        try:
            current_day += 1
            logger.info(f"Getting data for {day} ({current_day}/{days + 1})")
            response = await get_exchange_rate(BANK_URL + day)
            logger.debug(response)
            result = await process_response_data(response, currencies)
            output_list.append(result) if result else None
        except HttpGetError as e:
            logger.error(f'{e}')
    return output_list


async def process_response_data(data: dict, currencies: tuple) -> dict | None:
    date_key = data['date']
    currency_dict = {
        currency['currency']: {
            'sale': currency['saleRate'],
            'purchase': currency['purchaseRate']
        }
        for currency in data['exchangeRate']
        if currency['currency'] in currencies  # ('EUR', 'USD')
    }
    day_dict = {date_key: currency_dict}
    # check empty currency_dict
    if not currency_dict:
        logging.warning(f'No data for currencies: {currencies}')
        return None
    else:
        logging.debug(f'Parsed data: {day_dict}')
        return day_dict


async def get_exchange_rate(url: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, ) as response:
                if response.status == 200:
                    result = await response.json(content_type='application/json')
                    return result
                else:
                    raise HttpGetError(f'Error when opening URL: {url}, Error: {response.status}')
        except (
                aiohttp.ClientError, aiohttp.ClientConnectionError, aiohttp.ClientResponseError,
                aiohttp.InvalidURL) as e:
            raise HttpGetError(f'Connection error when opening URL: {url}, Error: {e}')


def main():
    ...


if __name__ == '__main__':
    main()
