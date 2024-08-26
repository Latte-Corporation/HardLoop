import asyncio
import json
import os

async def main():
    while True:
        try:
            # Get the list of all files in the directory
            file_list = os.listdir("world/stats")

            # Print the list of files
            for file_name in file_list:
                file = open("world/stats/" + file_name, "r")
                json_data = json.load(file)
                print(json_data['stats']['minecraft:deaths'])
                file.close()
        except:
            print("Error reading file")

        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())