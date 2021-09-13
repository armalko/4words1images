from django.apps import AppConfig
from django.conf import settings
from tg_bot.TgBot import TgBot

import logging
logging.basicConfig(level=logging.INFO)


class TgBotConfig(AppConfig):
    name = 'tg_bot'

    bot = None
    bot_ready = False

    def ready(self):
        if self.bot_ready:
            return

        self.bot_ready = True
        tb = TgBot(token=settings.BOT_TOKEN)

        tb.setup()

        TgBotConfig.bot = tb

        logging.info('TgBotConfig: bot has been setup.')
