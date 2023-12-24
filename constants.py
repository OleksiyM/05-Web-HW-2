from pathlib import Path

import aiopath

# https://api.privatbank.ua/#p24/exchangeArchive
BANK_URL = 'https://api.privatbank.ua/p24api/exchange_rates?date='

ROOT_DIR = Path()
STORAGE_DIR = ROOT_DIR.joinpath('storage')
STORAGE_DATA_FILE = STORAGE_DIR.joinpath('data.txt')
LOG_FILE = aiopath.Path(STORAGE_DIR.joinpath('exchange.log'))

BASE_CURRENCIES = ('EUR', 'USD')
ALL_CURRENCIES = ('EUR', 'USD', 'CHF', 'CZK', 'GBP', 'PLN')
MAX_ARCHIVE_DAYS: int = 10


def main():
    ...


if __name__ == '__main__':
    main()
