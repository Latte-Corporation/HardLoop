import asyncio
import json
import os
import signal
from subprocess import PIPE, Popen
import time

async def main():
    while True:
        try:
            # Get the list of all files in the directory
            file_list = os.listdir("world/stats")

            # Print the list of files
            for file_name in file_list:
                file = open("world/stats/" + file_name, "r")
                json_data = json.load(file)
                if json_data['stats']['minecraft:deaths'] > 0:
                    kill_process()
                    start_server()
        except:
            print("Error reading file")

        await asyncio.sleep(5)

def kill_process():
    processes = Popen(['ps', '-ef'], stdout=PIPE, stderr=PIPE)
    stdout, _ = processes.communicate()

    for line in stdout.splitlines():

        if (line.__contains__("java")):

            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGKILL)

def start_server():
    os.system("java -Xmx1024M -Xms1024M -jar server.jar nogui")

def rename_world():
    os.system("mv world world_" + str(time.time()))

if __name__ == "__main__":
    asyncio.run(main())