import asyncio
from mcrcon import MCRcon
from .server import update_motd

last_dead_player = "Unknown"
server_uptime = 0
played_time = 0


async def listen():
    global last_dead_player
    global server_uptime
    global played_time
    print("Listening for deaths")
    with MCRcon("0.0.0.0", "password", port=25575) as client:
        while True:
            try:
                client.command("/team modify uptime suffix {\"text\":\" : \",\"color\":\"red\",\"extra\":[{\"text\":\""+ f"{uptime_incr()}" +"\",\"color\":\"green\"}]}")
                players = client.command("/list")
                if "There are 0 of a max" not in players : 
                    client.command("/team modify played suffix {\"text\":\" Time : \",\"color\":\"red\",\"extra\":[{\"text\":\""+ f"{played_time_incr()}" +"\",\"color\":\"green\"}]}")
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
                            server_uptime = 0
                            played_time = 0
                            break
            except Exception as e:
                print(f"error fetching deaths : {e}")

            await asyncio.sleep(1)


async def reset_server(client):
    client.command("/stop")

def uptime_incr():
    global server_uptime
    server_uptime = server_uptime + 1
    return server_uptime

def played_time_incr():
    global played_time
    played_time = played_time + 1
    return played_time