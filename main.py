import discord
from discord.ext import tasks
import datetime

TOKEN = ""
CHANNEL_ID = 0

intents = discord.Intents.default()
intents.message_content = True


class Client(discord.Client):
    def __init__(self, *, intents):
        super().__init__(intents=intents)
        self.last_sent_date = None
        self.task_started = False

    async def on_ready(self):
        print(f"Bot está online como {self.user}!")
        if not self.task_started:
            self.send_everyone_message.start()
            self.task_started = True

    async def on_message(self, message):
        print(f"Mensagem recebida: {message.content}")

    @tasks.loop(minutes=1)
    async def send_everyone_message(self):
        now = datetime.datetime.utcnow()
        if now.weekday() == 2 and now.hour == 15:
            today = now.date()
            if self.last_sent_date != today:
                channel = self.get_channel(CHANNEL_ID)
                if channel:
                    await channel.send("@everyone Não esqueçam de enviar a weekly!")
                    self.last_sent_date = today

    @send_everyone_message.before_loop
    async def before_send(self):
        await self.wait_until_ready()


client = Client(intents=intents)
client.run(TOKEN)
