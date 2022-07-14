import discord
import queue
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
                    buffer += message.author.name + ": " + message.content + '\n'
                if buffer:
                    await channel.send(buffer)

    async def on_message_delete(self, message):
        if message.channel.id not in self.message_queues:
            self.message_queues[message.channel.id] = PQueue(maxsize=30)
        self.message_queues[message.channel.id].put((message.created_at, message))


client = UndeleteBot()
TOKEN = os.environ.get("DISCORD_TOKEN")
client.run(TOKEN)

