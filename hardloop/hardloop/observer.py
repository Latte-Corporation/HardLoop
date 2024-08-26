import asyncio
import json
import os
from rcon.source import Client
import time


async def listen():
    print("Starting server ...")
    start_server()
    while True:
        try:
            # Get the list of all files in the directory
            file_list = os.listdir("world/stats")

            # Print the list of files
            for file_name in file_list:
                file = open("world/stats/" + file_name, "r")
                json_data = json.load(file)
                print(json_data["stats"]["minecraft:deaths"])
                if json_data["stats"]["minecraft:deaths"] > 0:
                    stop_server()
        except Exception:
            asyncio.sleep(0)
            print("error accessing death file")

        await asyncio.sleep(0.1)


def stop_server():
    with Client("hardloop", 25575, password="password") as client:
        with open("/server/logs/latest.log", "r") as f:
            try:  # catch OSError in case of a one line file
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b"\n":
                    f.seek(-2, os.SEEK_CUR)
            except OSError:
                f.seek(0)
            last_line = f.readline().decode()
            client.run(f"kick @a {last_line}")
            rename_world()
            client.run("stop")
            start_server()


def start_server():
    os.system("java -Xmx1024M -Xms1024M -jar server.jar nogui")


def rename_world():
    os.system("mv /server/world /server/world_" + str(time.time()))
