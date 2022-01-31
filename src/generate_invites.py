from loaders.account_loader import Account, AccountLoader
from discord.utils import create_discord_session

import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def generate_invite(account: Account, chat_id):
    session = create_discord_session(account)
    data = {"Content-Type": "application/json"}
    r = session.post(
        f'https://discord.com/api/v9/channels/{chat_id}/invites', json=data, verify=False)
    response = json.loads(r.text)
    invite_link = f"https://discord.gg/{response['code']}"
    expires_at = response["expires_at"]
    username = response["inviter"]["username"]

    invite = {
        "invite_link": invite_link,
        "expires_at": expires_at,
        "username": username
    }

    return invite


if __name__ == "__main__":
    chat_id = str(input("Chat ID: "))

    loader = AccountLoader("config/accounts.txt")
    accounts = loader.load_accounts()
    for account in accounts:
        invite = generate_invite(account, chat_id)
        print(invite)
