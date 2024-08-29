import subprocess
from mcrcon import MCRcon
import os
import asyncio
import time


async def start_server(server_port=25565):
    if server_port != 25565:
        update_server_properties("server-port", server_port)
    print(f"Starting server on port {server_port}")
    process = subprocess.Popen(
        ["java", "-Xmx1024M", "-Xms1024M", "-jar", "server.jar", "nogui"]
    )
    while True:
        try:
            with MCRcon("hardloop", "password", port=25575) as client:
                client.command("/scoreboard objectives add Deaths deathCount")
                client.command("/scoreboard objectives add health health")
                client.command("/scoreboard objectives setdisplay list health")
                client.command("/scoreboard objectives add Hardloop dummy {\"text\":\"HardLoop\",\"bold\":true,\"color\":\"light_purple\"}")
                client.command("/scoreboard objectives setdisplay sidebar Hardloop")
                client.command("/scoreboard players set =-=-=-=-=-=-=-=-=-=-=-=-= Hardloop 3")
                client.command("/scoreboard players set Uptime Hardloop 2")
                client.command("/scoreboard players set Played Hardloop 1")
                client.command("/scoreboard players set -=-=-=-=-=-=-=-=-=-=-=-=- Hardloop 0")
                client.command("/team add uptime")
                client.command("/team add played")
                client.command("/team add separators")
                client.command("/team join uptime Uptime")
                client.command("/team join played Played")
                client.command("/team join separators -=-=-=-=-=-=-=-=-=-=-=-=-")
                client.command("/team join separators =-=-=-=-=-=-=-=-=-=-=-=-=")
                client.command("/team modify separators color light_purple")
                client.command("/team modify uptime color red")
                client.command("/team modify played color red")
                client.command("/team modify uptime suffix {\"text\":\" : 00m00\",\"color\":\"red\"}")
                client.command("/team modify played suffix {\"text\":\" Time : 00m00\",\"color\":\"red\"}")
                break
        except Exception:
            await asyncio.sleep(1)
    return process


async def rename_world(backup_enabled="true"):
    if backup_enabled.lower() == "true":
        os.system("mv /hardloop/world /hardloop/old_worlds/world_" +
                  str(time.time()))
        print("World saved")
    else:
        os.system("rm -rf /hardloop/world")
        os.system("mkdir /hardloop/old_worlds/world_" + str(time.time()))
        print("World deleted")


def count_world_resets():
    world_dir = "/hardloop/old_worlds"
    world_count = len(
        [d for d in os.listdir(world_dir) if d.startswith("world")]
    )
    return world_count + 1


def update_server_properties(properties, value):
    properties_path = "server.properties"
    with open(properties_path, "r") as file:
        lines = file.readlines()

    with open(properties_path, "w") as file:
        for line in lines:
            if line.startswith(properties):
                file.write(f"{properties}={value}\n")
            else:
                file.write(line)

    print(f"{properties} updated successfully to {value}")


def update_motd(last_dead_player):
    reset_time = count_world_resets()
    new_motd = f"\u00a7bServer has been reset\u00a7d {reset_time}\u00a7b times\u00a7r\\n\u00a7bLast death was\u00a7d {last_dead_player}"
    update_server_properties("motd", new_motd)
