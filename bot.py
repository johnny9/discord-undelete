import discord
import queue


class QueueDrainer(object):
    def __init__(self, q):
        self.q = q

    def __iter__(self):
        while True:
            try:
                yield self.q.get_nowait()
            except queue.Empty:  # on python 2 use Queue.Empty
                break

class UndeleteBot(discord.Client):
    message_queues = dict()

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.content.startswith('$undelete'):
            channel = message.channel
            if channel.id in self.message_queues:
                q = self.message_queues[channel.id]
                while True:
                    try:
                        message = q.get_nowait()
                        await channel.send(message.author.name + ": " + message.content)
                    except queue.Empty:  # on python 2 use Queue.Empty
                        break

    async def on_message_delete(self, message):
        if message.channel.id not in self.message_queues:
            self.message_queues[message.channel.id] = queue.Queue()
        self.message_queues[message.channel.id].put(message)


client = UndeleteBot()
client.run("", bot=False)

