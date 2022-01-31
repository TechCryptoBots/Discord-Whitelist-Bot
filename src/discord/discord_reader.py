import requests
import json
import logging

from loaders.account_loader import Account
from discord.utils import create_discord_session


class DiscordReader:

    def __init__(self, chat_id, log=True) -> None:
        self.chat_id = chat_id
        self.last_message = None
        self.log = log

    def read_last_message(self, account: Account):
        session = create_discord_session(account=account)
        r = session.get(
            f'https://discord.com/api/v9/channels/{self.chat_id}/messages?limit=1')
        message = json.loads(r.text)[0]

        if self.last_message != message:
            self.last_message = message
            if self.log:
                self.print_message(message)

    def print_message(self, message_dict):
        logging.info(
            f"READ: Получил сообщение: [{message_dict['author']['username']}] {message_dict['content']}")
