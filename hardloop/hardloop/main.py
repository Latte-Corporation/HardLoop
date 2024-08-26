from .get_serv_jar import download_server_file
from .observer import listen
from .server import start_server, rename_world

import asyncio


async def main():
    download_server_file()
    while True:
        server_process = await start_server()
        listen_task = asyncio.create_task(listen())

        await asyncio.to_thread(server_process.wait)

        print("Server has stopped, restarting...")
        listen_task.cancel()
        await rename_world()


if __name__ == "__main__":
    asyncio.run(main())
