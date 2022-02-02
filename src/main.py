import logging
import yaml
import telegram

from telegram_logger.logger import BotLogger

from discord.discord_bot import DiscordBot

class WarningFormatter(logging.Formatter):
    def format(self, record):
        result = super().format(record)
        if record.levelno == logging.WARNING:
            result = f"⚠️ {result}"

if __name__ == "__main__":
    # logging.basicConfig(
    #     format='%(levelname)s: %(message)s', level=logging.INFO)
    logging.basicConfig(
        format='%(message)s', level=logging.INFO)
    logger = logging.getLogger()
    # warning_handler = logging.StreamHandler()
    # warning_handler.setFormatter(WarningFormatter())
    # logger.addHandler(warning_handler)
    
    with open("config/config.yaml", "r", encoding="utf8") as stream:
        config = yaml.safe_load(stream)
    
    # Set up telegram bot
    if config['log_tg'] and config.get('telegram_settings'):
        with open(config['telegram_settings'], "r", encoding="utf8") as stream:
            tg_config = yaml.safe_load(stream)
        bot = telegram.Bot(tg_config['telegram_token'])
        logger.addHandler(BotLogger(bot=bot, chat_id=tg_config['chat_id'], level=logging.INFO))

    logging.info("▶️  Включаю бота...")
    bot = DiscordBot(config=config)
    bot.start_bot()
