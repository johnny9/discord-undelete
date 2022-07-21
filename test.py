import unittest
import bot
import discord


class FakeAuthor:
    def __init__(self, name):
        self.name = name


class FakeChannel:
    def __init__(self, channel_id):
        self.id = channel_id
        self.buffer = ""

    async def send(self, buffer):
        self.buffer += buffer


class FakeMessage:
    def __init__(self, channel, content="", timestamp=1, author="nobody"):
        self.content = content
        self.created_at = timestamp
        self.channel = channel
        self.author = FakeAuthor(author)


class UndeleteBotTest(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        bot_intents = discord.Intents.default()
        bot_intents.messages = True
        bot_intents.message_content = True
        cls.bot = bot.UndeleteBot(intents=bot_intents)

    async def test_on_delete_call(self):
        channel_id = 1
        channel = FakeChannel(channel_id)
        message = FakeMessage(channel)
        message.content = "Message 1"
        await self.bot.on_message_delete(message)
        time, value = self.bot.message_queues[1].get()
        self.assertEqual(time, 1)
        self.assertEqual(value.content, "Message 1")

    async def test_out_of_order_delete_calls(self):
        channel_id = 1
        channel = FakeChannel(channel_id)
        message1 = FakeMessage(channel, "1", 1)
        message2 = FakeMessage(channel, "2", 2)
        message3 = FakeMessage(channel, "3", 3)

        await self.bot.on_message_delete(message2)
        await self.bot.on_message_delete(message3)
        await self.bot.on_message_delete(message1)

        for i in range(1, 3):
            time, value = self.bot.message_queues[1].get()
            self.assertEqual(time, i)
            self.assertEqual(value.content, str(i))

    async def test_command(self):
        channel_id = 1
        channel = FakeChannel(channel_id)
        message1 = FakeMessage(channel, "1", 1)
        await self.bot.on_message_delete(message1)
        command_message = FakeMessage(channel, "$undelete", 2)
        await self.bot.on_message(command_message)
        expected_output = "{}: {}\n".format(message1.author.name, message1.content)
        self.assertEqual(channel.buffer, expected_output)


if __name__ == '__main__':
    unittest.main()
