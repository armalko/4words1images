from django.core.management.base import BaseCommand

from tg_bot.apps import TgBotConfig


class Command(BaseCommand):

    help = "Started bot"

    def handle(self, *args, **options):
        bot = TgBotConfig.bot
        bot.updater.start_polling()
