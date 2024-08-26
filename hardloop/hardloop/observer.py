import asyncio
from mcrcon import MCRcon


async def listen():
    print("Listening for deaths")
    while True:
        try:
            with MCRcon("0.0.0.0", "password", port=25575) as client:
                response = client.command("/scoreboard players list")
                if "There are no tracked entities" not in response:
                    player = response.split(": ")[1]
                    client.command(f"/kick @a {player} is dead !")
                    await reset_server()
        except Exception:
            asyncio.sleep(0)
            print("error fetching deaths")

        await asyncio.sleep(0.1)


async def reset_server():
    with MCRcon("0.0.0.0", "password", port=25575) as client:
        client.command("/stop")
        print("Sending stop command")
