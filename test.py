import unittest
import bot
import discord


class FakeChannel:
    def __init__(self, channel_id):
        self.id = channel_id


class FakeMessage:
    def __init__(self, content="", timestamp=1, channel_id=1):
        self.content = content
        self.created_at = timestamp
        self.channel = FakeChannel(channel_id)


class UndeleteBotTest(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        bot_intents = discord.Intents.default()
        bot_intents.messages = True
        bot_intents.message_content = True
        cls.bot = bot.UndeleteBot(intents=bot_intents)

    async def test_on_delete_call(self):
        message = FakeMessage()
        message.content = "Message 1"
        message.channel.id = 1
        await self.bot.on_message_delete(message)
        time, value = self.bot.message_queues[1].get()
        self.assertEqual(time, 1)
        self.assertEqual(value.content, "Message 1")

    async def test_out_of_order_delete_calls(self):
        message1 = FakeMessage("1", 1)
        message2 = FakeMessage("2", 2)
        message3 = FakeMessage("3", 3)

        await self.bot.on_message_delete(message2)
        await self.bot.on_message_delete(message3)
        await self.bot.on_message_delete(message1)

        for i in range(1, 3):
            time, value = self.bot.message_queues[1].get()
            self.assertEqual(time, i)
            self.assertEqual(value.content, str(i))


if __name__ == '__main__':
    unittest.main()
