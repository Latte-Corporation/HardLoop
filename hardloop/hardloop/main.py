from .get_serv_jar import download_server_file
from .observer import listen

import asyncio


async def main():
    download_server_file()
    await listen()


if __name__ == "__main__":
    asyncio.run(main())
