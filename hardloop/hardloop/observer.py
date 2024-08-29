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
    return int_to_date(server_uptime)

def played_time_incr():
    global played_time
    played_time = played_time + 1
    return int_to_date(played_time)

def int_to_date(time: int) -> str:
    seconds = time % 60
    minutes = time // 60 % 60
    hours = time // 3600 % 24
    days = time // 86400
    if (minutes == 0 and hours == 0 and days == 0): return f"{seconds}s"
    if (hours == 0 and days == 0): return f"{minutes}m {seconds}s"
    if (days == 0): return f"{hours}h {minutes}m {seconds}s"
    return f"{days}d {hours}h {minutes}m {seconds}s"
