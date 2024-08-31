from .get_serv_jar import download_server_file
from .observer import listen
from .server import start_server, rename_world
from .discord import discord_logger

import asyncio
import os

mc_version = os.getenv("MC_VERSION", None)
mc_port = os.getenv("MC_PORT", 25565)
mc_eula = os.getenv("MC_EULA", "false")
mc_backup = os.getenv("MC_BACKUP", "true")
discord_enabled = os.getenv("DISCORD_ENABLED", "false")
discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL", None)
discord_log_level = os.getenv("DISCORD_LOG_LEVEL", "INFO")

async def main():

    if mc_eula.lower() == "true":
        with open("eula.txt", "w") as f:
            f.write("eula=true")
            print("EULA accepted")
    else:
        print("EULA not accepted, exiting")
        return

    download_server_file(mc_version)

    if discord_enabled.lower() == "true":
        asyncio.create_task(discord_logger(discord_webhook_url, discord_log_level))
    while True:
        server_process = await start_server(mc_port)
        listen_task = asyncio.create_task(listen())

        await asyncio.to_thread(server_process.wait)

        print("Server has stopped, restarting...")
        listen_task.cancel()
        await rename_world(mc_backup)


if __name__ == "__main__":
    asyncio.run(main())
