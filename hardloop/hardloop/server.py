import subprocess
from mcrcon import MCRcon
import os
import asyncio
import time


async def start_server():
    print("Starting server")
    process = subprocess.Popen(
        ["java", "-Xmx1024M", "-Xms1024M", "-jar", "server.jar", "nogui"]
    )
    while True:
        try:
            with MCRcon("hardloop", "password", port=25575) as client:
                client.command("/scoreboard objectives add Deaths deathCount")
                break
        except Exception:
            await asyncio.sleep(1)
    return process


async def rename_world():
    os.system("mv /hardloop/world /hardloop/world_" + str(time.time()))
    print("World renamed")
