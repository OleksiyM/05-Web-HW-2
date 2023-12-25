import logging

import names
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK

from utils import generate_html_table, check_exchange_message, handle_exchange, get_data

logging.basicConfig(level=logging.INFO)


# logging.basicConfig(level=logging.DEBUG)


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connected')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnected')

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distribute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distribute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            is_exchange, rates_days, currencies = await check_exchange_message(message)
            await self.send_to_clients(f"{ws.name}: {message}")
            if is_exchange:
                logging.debug(f'{rates_days=}, {currencies=}')
                await handle_exchange(
                    f'{ws.name}: {message}; Request handled for current day and {rates_days} archive days and {currencies}')

                await self.send_to_clients(
                    f'Server: getting rates from Privat Bank for current day and {rates_days} archive days for {currencies}')

                result = await get_data(rates_days, currencies)
                html_table = await generate_html_table(result)
                # html_table_m = await generate_html_table_1(result)
                # decoded_html_table = html.unescape(html_table)

                # text formatted table
                # text_table = await generate_text_table_html(result)
                # for l in text_table:
                #     await self.send_to_clients(l)
                await self.send_to_clients('<h3>Exchange rates</h3>\n')
                await self.send_to_clients(html_table)
                # await self.send_to_clients(html_table_m)
                # await self.send_to_clients(decoded_html_table)
                # logging.debug(html_table)
                # logging.debug(text_table)
            # await self.send_to_clients(f"{ws.name}: {message}")
