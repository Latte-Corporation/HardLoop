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


def count_world_resets():
    world_dir = "/hardloop"
    world_count = len(
      [d for d in os.listdir(world_dir) if d.startswith("world")]
      )
    return world_count


def update_motd(last_dead_player):
    properties_path = "server.properties"
    reset_time = count_world_resets()
    new_motd = f"\u00a7bServer has been reset\u00a7d {reset_time}\u00a7b times\u00a7r\\n\u00a7bLast death was\u00a7d {last_dead_player}"

    with open(properties_path, "r") as file:
        lines = file.readlines()

    with open(properties_path, "w") as file:
        for line in lines:
            if line.startswith("motd="):
                file.write(f"motd={new_motd}\n")
            else:
                file.write(line)

    print("MOTD updated successfully")
