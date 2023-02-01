import asyncio
import logging
from datetime import datetime

import websockets
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK
import names
from aiofile import async_open

from constants import (
    LOGFILE_TXT,
    DEFAULT_CURRENCIES,
)
from src import get_exchange_rates
from src.response_formatter import exchange_rates_format_to_text

logging.basicConfig(level=logging.INFO)


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol) -> None:
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol) -> None:
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str) -> None:
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol) -> None:
        await self.register(ws)
        try:
            await self.distribute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distribute(self, ws: WebSocketServerProtocol) -> None:
        async for message in ws:
            await self.send_to_clients(f"{ws.name}: {message}")

            if str(message).lower().startswith('exchange'):
                asyncio.create_task(
                    write_log(f"{str(datetime.now()):<28}|{ws.name:^20}| the exchange command is called\n")
                )
                await self.send_exchange_rates(message)

    async def send_exchange_rates(self, message: str) -> None:
        command, *data = message.strip().split(' ', maxsplit=1)

        days = None

        if data:
            try:
                days = int(data[0].strip())
            except ValueError:
                days = 0

            if days <= 0:
                await self.send_to_clients("You will be shown the exchange rate for the current day")

            elif days > 10:
                await self.send_to_clients("The period for which you can receive exchange rates cannot exceed 10 days!")
                return

        exchange_rates = await get_exchange_rates(DEFAULT_CURRENCIES.keys(), days)

        [await self.send_to_clients(exchange_rates_format_to_text(exr)) for exr in exchange_rates]


async def write_log(message: str) -> None:
    async with async_open(LOGFILE_TXT, 'a') as afp:
        await afp.write(message)


async def main() -> None:
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    asyncio.run(main())
