import logging
import telegram
from time import sleep

class BotLogger(logging.NullHandler):

    def __init__(self, bot: telegram.Bot, chat_id, level=...) -> None:
        super().__init__(level)
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record: logging.LogRecord) -> None:
        sleep(0.1)
        self.bot.send_message(text=record.message, chat_id=self.chat_id)

    def handle(self, record: logging.LogRecord) -> bool:
        return self.emit(record)
