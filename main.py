import asyncio
import logging
import os
import sys

import websockets

from Server import Server
from constants import STORAGE_DIR
from utils import create_storage_dir

logging.basicConfig(level=logging.INFO)


# logging.basicConfig(level=logging.DEBUG)


async def main():
    create_storage_dir(STORAGE_DIR)
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    abspath = os.path.abspath(__file__)
    dir_name = os.path.dirname(abspath)
    os.chdir(dir_name)

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(levelname)s - %(message)s')

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Exiting after Control+C...")
        sys.exit(0)
