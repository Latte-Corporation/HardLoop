import asyncio
from mcrcon import MCRcon
from .server import update_motd

last_dead_player = "Unknown"


async def listen():
    global last_dead_player
    print("Listening for deaths")
    with MCRcon("0.0.0.0", "password", port=25575) as client:
        while True:
            try:
                players = client.command("/list")
                players = players.split(": ")[1].split(", ")
                if len(players) != 0:
                    for player in players:
                        response = client.command(
                            f"/scoreboard players get {player} Deaths"
                        )
                        if "has" in response:
                            last_dead_player = player
                            client.command(
                                f"/kick @a {last_dead_player} is dead !"
                            )
                            update_motd(last_dead_player)
                            await reset_server(client)
                            break
            except Exception:
                print("error fetching deaths")

            await asyncio.sleep(0.1)


async def reset_server(client):
    client.command("/stop")
