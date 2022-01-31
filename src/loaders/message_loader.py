import re


class Message:
    def __init__(self, text, account_id, is_reply=False, reply_account_id=0) -> None:
        self.account_id = account_id
        self.text = text
        self.is_reply = is_reply
        self.reply_account_id = reply_account_id
        
    def __str__(self) -> str:
        return f"[{self.account_id}]: {self.text};" + (" reply to {self.reply_account_id}" if self.is_reply else '')


class FileMessageLoader:

    def __init__(self, message_file, accounts_amount=1) -> None:
        self.message_file = message_file
        self.accounts_amount = accounts_amount
        self.current_message_id = 0
        if accounts_amount > 1:
            self.check_message_file()

    def load_message_file(self):
        return open(self.message_file, 'r', encoding='utf-8').read()

    def check_message_file(self):
        pattern = re.compile("([1-9][0-9]*:.*(\n|$))*")
        match = pattern.fullmatch(self.load_message_file())
        if match:
            print("Файл с сообщениями проверен")
        else:
            raise ValueError("Файл с сообщениями сформатирован неправильно!")

    def has_messages(self):
        message_set_length = len(self.load_message_file().splitlines())
        return self.current_message_id < message_set_length

    def get_next_message(self) -> Message:
        message_set = self.load_message_file().splitlines()
        next_msg = message_set.pop(self.current_message_id)
        self.current_message_id += 1

        if self.accounts_amount > 1:
            split_idx = next_msg.find(":")
            text = next_msg[split_idx + 1:]
            account_id = int(next_msg[:split_idx])
            
            pattern = re.compile("^[1-9][0-9]*:.*$")
            if pattern.fullmatch(text):
                reply_split_idx = text.find(":")
                reply_account_id = int(text[:reply_split_idx])
                text = text[reply_split_idx + 1:]

                return Message(text=str(text), account_id=account_id, is_reply=True, reply_account_id=reply_account_id)
            else:
                return Message(text=str(text), account_id=account_id, is_reply=False)
        else:
            return Message(text=str(next_msg), account_id=1, is_reply=False)
