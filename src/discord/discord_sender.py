from email import message
from time import sleep
import json
import requests
import logging
import math

from loaders.account_loader import Account
from loaders.message_loader import Message
from discord.utils import create_discord_session


class DiscordError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class DiscordSender:
    def __init__(self, chat_id, log=False) -> None:
        self.chat_id = chat_id
        self.log = log
        self.last_messages = {}

    def simulate_typing(self, time, account: Account):
        session = create_discord_session(account)

        r = session.post(
            f'https://discord.com/api/v9/channels/{self.chat_id}/typing', verify=False)

        if r.status_code >= 200 and r.status_code < 300:
            sleep(time)
        elif r.status_code == 429:
            logging.error("❌  Discord вернул ошибку 429 (слишком много запросов), попробуйте увеличить задержку или переставить отправляемые сообщения")
            logging.error(r.text)
        else:
            logging.error("❌  Discord вернул ошибку, возможно введен неправильный ID чата или токены аккаунтов больше не действительны")
            raise DiscordError(
                "Discord вернул код: " + str(r.status_code))

    def send_message(self, msg: Message, account: Account):
        if account.auth_token == '' or account.auth_token == None:
            raise KeyError('Токен авторизации не загружен')

        data = {'content': msg.text, 'tts': False}
        
        # Create reply to a message
        if msg.is_reply:
            if self.last_messages.get(msg.reply_account_id):
                reply_data = {
                    'channel_id': self.chat_id, 
                    'message_id': self.last_messages[msg.reply_account_id]['id']
                }
                data['message_reference'] = reply_data
        
        session = create_discord_session(account)

        r = session.post(
            f'https://discord.com/api/v9/channels/{self.chat_id}/messages', json=data, verify=False)
        if r.status_code == 200:
            response_message = json.loads(r.text)
            self.last_messages[account.account_id] = response_message
            if self.log:
                self.print_message_result(response_message)
        elif r.status_code == 429:
            logging.error("❌  Discord вернул ошибку 429 (слишком много запросов), попробуйте увеличить задержку или переставить отправляемые сообщения")
            logging.debug(r.text)
            error_message = json.loads(r.text)
            logging.info(f"Возобновляю отправку через {error_message['retry_after']}")
            sleep(math.ceil(error_message['retry_after']))
            # Retry
            self.send_message(msg, account)
        else:
            raise DiscordError("Discord returned status code: " + str(r.status_code)
                               + ("\n This status code likely means that the token is no longer valid" if r.status_code == 401 else ""))

    def print_message_result(self, message_result):
        logging.info(
            "SEND: " + message_result['author']['username'] + ": " + message_result['content'])
