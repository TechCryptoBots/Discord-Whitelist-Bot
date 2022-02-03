from loaders.account_loader import AccountLoader
from loaders.message_loader import FileMessageLoader
from discord.discord_sender import DiscordSender
from discord.discord_reader import DiscordReader
import logging
import random
from time import sleep
import threading
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class DiscordBot:

    def __init__(self, config) -> None:
        self.config = config

        account_loader = AccountLoader(accounts_file=config["accounts_file"])
        if config["use_proxy"]:
            account_loader.proxy_file = config["proxy_file"]
        self.accounts = account_loader.load_accounts()
        self.message_reader = FileMessageLoader(
            message_file=config["messages_file"], accounts_amount=len(self.accounts))

        self.discord_sender = DiscordSender(chat_id=config["chat_id"], log=config["log_send"])
        self.discord_reader = DiscordReader(chat_id=config["chat_id"], log=config["log_read"])

        self.send_delay = config["send_delay"]
        self.read_delay = config["read_delay"]

        self.send_thread = None
        self.read_thread = None

    def send_next_message(self, simulate_typing=True):
        message = self.message_reader.get_next_message()
        if message.account_id > len(self.accounts):
            raise ValueError(f'Бот хочет отправить сообщение от аккаунта номер {message.account_id}, но аккаунтов всего  {len(self.accounts)}')
        current_account = self.accounts[message.account_id - 1]
        if simulate_typing:
            secs_per_character = self.config['typing_delay_per_character']
            self.discord_sender.simulate_typing(
                len(message.text) * secs_per_character, current_account)

        self.discord_sender.send_message(message, current_account)

    def read_last_message(self):
        self.discord_reader.read_last_message(self.accounts[0])

    def start_bot(self):
        self.send_thread = threading.Thread(target=self.start_sending)
        self.read_thread = threading.Thread(target=self.start_reading)

        self.read_thread.start()
        self.send_thread.start()

        self.send_thread.join()

    def start_sending(self):
        logging.info("Работаем...")
        while self.message_reader.has_messages():
            self.send_next_message()
            delay = self.config['send_delay']
            if self.config["log_send"]:
                logging.info("Задержка до следующего сообщения " + "{:.2f}".format(delay))
            sleep(delay)
        logging.warning("🏁 Последнее сообщение из файла было отправлено!")

    def start_reading(self):
        while True:
            self.read_last_message()
            sleep(self.read_delay)
