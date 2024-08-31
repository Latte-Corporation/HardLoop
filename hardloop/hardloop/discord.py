from discord_webhook import DiscordWebhook
import io, os, asyncio, time

LOG_FILE = "/hardloop/logs/latest.log"

async def discord_logger(webhook_url_arg: str, log_level_arg: str):
    async def open_log_file():
        while True:
            try:
                return io.open(LOG_FILE)
            except FileNotFoundError:
                asyncio.sleep(1)

    def file_changed(stat1, stat2):
        return stat1.st_ino != stat2.st_ino or stat2.st_size == 0

    f = await open_log_file()
    last_stat = os.stat(LOG_FILE)

    while True:
        try:
            current_stat = os.stat(LOG_FILE)
            if file_changed(last_stat, current_stat):
                f.close()
                webhook = DiscordWebhook(url=webhook_url_arg, content="```ansi\n[2;31m[1;31mSERVER RESTARTED[0m[2;31m[0m\n```")
                webhook.execute()
                f = await open_log_file()
                last_stat = current_stat

            line = f.readline().strip()
            if not line:
                await asyncio.sleep(1)
                continue

            webhook = DiscordWebhook(url=webhook_url_arg, content=line)
            webhook.execute()
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(5) 

