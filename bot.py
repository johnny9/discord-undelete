import discord
from discord import app_commands
import os


class PQueue(object):
    items = []

    def __init__(self, maxsize=30):
        self.maxsize = maxsize

    def put(self, item):
        self.items.append(item)
        self.items.sort(reverse=True)
        while len(self.items) > self.maxsize:
            self.items.pop()

    def get(self):
        return self.items.pop()

    def get_nowait(self):
        return self.get()

    def empty(self):
        return len(self.items) == 0


class UndeleteBot(discord.Client):
    message_queues = dict()

    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.content.startswith('$undelete'):
            channel = message.channel
            if channel.id in self.message_queues:
                q = self.message_queues[channel.id]
                buffer = ""
                while not q.empty():
                    key, message = q.get()
                    next_line = message.author.name + ": " + message.content + '\n'
                    if len(buffer) + len(next_line) > 2000:
                        await channel.send(buffer)
                        buffer = ""
                    buffer += message.author.name + ": " + message.content + '\n'
                if buffer:
                    await channel.send(buffer)

    async def on_message_delete(self, message):
        if message.channel.id not in self.message_queues:
            self.message_queues[message.channel.id] = PQueue(maxsize=30)
        self.message_queues[message.channel.id].put((message.created_at, message))


if __name__ == '__main__':
    bot_intents = discord.Intents.default()
    bot_intents.messages = True
    bot_intents.message_content = True
    client = UndeleteBot(intents=bot_intents)

    @client.tree.command()
    async def hello(interaction: discord.Interaction):
        """Says hello!"""
        await interaction.response.send_message(f'Hi, {interaction.user.mention}')

    TOKEN = os.environ.get("DISCORD_TOKEN")
    client.run(TOKEN)
