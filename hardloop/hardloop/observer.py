import asyncio
from mcrcon import MCRcon
from .server import update_motd
import aioping

last_dead_player = "Unknown"


async def listen():
    global last_dead_player
    print("Listening for deaths")
    with MCRcon("0.0.0.0", "password", port=25575) as client:
        while True:
            try:
                response = client.command("/scoreboard players list")
                if "There are no tracked entities" not in response:
                    last_dead_player = response.split(": ")[1]
                    client.command(f"/kick @a {last_dead_player} is dead !")
                    update_motd(last_dead_player)
                    await reset_server(client)
                    break
            except Exception:
                print("error fetching deaths")

            await asyncio.sleep(0.1)


async def reset_server(client):
    client.command("/stop")
