from .get_serv_jar import download_server_file
from .observer import listen
from .server import start_server, rename_world

import asyncio
import os

mc_version = os.getenv("MC_VERSION", None)
mc_port = os.getenv("MC_PORT", 25565)


async def main():
    download_server_file(mc_version)
    while True:
        server_process = await start_server(mc_port)
        listen_task = asyncio.create_task(listen())

        await asyncio.to_thread(server_process.wait)

        print("Server has stopped, restarting...")
        listen_task.cancel()
        await rename_world()


if __name__ == "__main__":
    asyncio.run(main())