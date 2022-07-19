import unittest
import bot
import discord


class FakeChannel:
    def __init__(self, id):
        self.id = id


class FakeMessage:
    content = ""
    channel = FakeChannel(1)
    created_at = 1


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


if __name__ == '__main__':
    unittest.main()
