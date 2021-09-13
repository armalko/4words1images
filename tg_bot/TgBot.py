# Telegram stuff
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

# Django stuff
from django.core.exceptions import ObjectDoesNotExist

# Utilities
from tg_bot.game_utils.utilities import Game

# Logging
import logging
logging.basicConfig(level=logging.INFO)


class TgBot:
    token = None
    updater = None

    def __init__(self, token):
        self.token = token
        self.updater = Updater(token=token, use_context=True)
        logging.info('Updater has been initialized')

    @property
    def dispatcher(self):
        return self.updater.dispatcher

    @property
    def bot(self):
        return self.updater.bot

    def setup(self):
        # Here goes handlers
        self.dispatcher.add_handler(CommandHandler('start', self.start_message_handler))
        self.dispatcher.add_handler(CallbackQueryHandler(self.callback_handler))
        self.dispatcher.add_handler(MessageHandler(Filters.text, self.text_message_handler))

    @staticmethod
    def start_message_handler(update, context):

        from tg_bot.models import User
        try:
            User.objects.get(telegram_id=update.message.chat.id)
        except ObjectDoesNotExist:
            User(
                telegram_id=update.effective_user.id,
                first_name=update.effective_user.first_name if not update.effective_user.first_name is None else '',
                last_name=update.effective_user.last_name if not update.effective_user.last_name is None else '',
                tag=update.effective_user.username if not update.effective_user.username is None else '',
            ).save()

        context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот 4 картинки 1 слово.\n\n"
                                                                        "Правила простые:\n"
                                                                        "Я даю тебе 4 картинки и набор букв, "
                                                                        "ты должен составить слово из букв, которое"
                                                                        " подходит под каждую картинку. \n\n"
                                                                        "Начнем?",
                                 reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Давай!",
                                                                                          callback_data="yes_start")
                                                                     ]]))

    @staticmethod
    def callback_handler(update, context):
        from tg_bot.models import User
        if update.callback_query.data == "yes_start":
            user = User.objects.get(telegram_id=update.callback_query.from_user.id)
            if user.game_in_process:
                context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                         text="Доиграй сначала предыдущую игру :)")

            else:
                new_game = Game.get_random_game()
                user.game_in_process = True
                user.current_game_id = new_game['id']
                user.save()
                context.bot.send_media_group(chat_id=update.callback_query.from_user.id,
                                             media=[InputMediaPhoto("https://4fotki1slovo.net" + new_game['photos'][0],
                                                                    caption=Game.get_ready_to_send_text(new_game)),
                                                    InputMediaPhoto("https://4fotki1slovo.net" + new_game['photos'][1]),
                                                    InputMediaPhoto("https://4fotki1slovo.net" + new_game['photos'][2]),
                                                    InputMediaPhoto("https://4fotki1slovo.net" + new_game['photos'][3]),
                                                    ])

    @staticmethod
    def text_message_handler(update, context):
        from tg_bot.models import User

        try:
            user = User.objects.get(telegram_id=update.message.chat.id)
        except ObjectDoesNotExist:
            User(
                telegram_id=update.effective_user.id,
                first_name=update.effective_user.first_name if not update.effective_user.first_name is None else '',
                last_name=update.effective_user.last_name if not update.effective_user.last_name is None else '',
                tag=update.effective_user.username if not update.effective_user.username is None else '',
            ).save()

            context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот 4 картинки 1 слово.\n\n"
                                                                            "Правила простые:\n"
                                                                            "Я даю тебе 4 картинки и набор букв, "
                                                                            "ты должен составить слово из букв, которое"
                                                                            " подходит под каждую картинку. \n\n"
                                                                            "Начнем?",
                                     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Давай!",
                                                                                              callback_data="yes_start")
                                                                         ]]))
            return

        if user.game_in_process:
            game = Game.find_game_by_id(user.current_game_id)

            if update.message.text.lower() == game['answer'].lower():
                user.correct_answers += 1
                user.game_in_process = False
                user.current_game_id = -1
                user.save()
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=f"Да, правильно! Всего угадал правильно: {user.correct_answers}\n\n"
                                              f"Еще одну?",
                                         reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Давай",
                                                                                                  callback_data="yes_"
                                                                                                                "start")
                                                                             ]])
                                         )
            else:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="Не то слово(")

        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Не понимаю тебя( Вызови /start")
