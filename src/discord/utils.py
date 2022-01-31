import requests
from loaders.account_loader import Account


def create_discord_session(account: Account):
    session = requests.Session()
    session.headers['authorization'] = account.auth_token
    session.headers.update(
        {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"})

    if account.use_proxy:
        session.proxies.update({'http': account.proxy, 'https': account.proxy})

    return session
