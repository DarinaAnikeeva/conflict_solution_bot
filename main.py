import time
import os
import random
from telegram import (Update, Bot, ReplyKeyboardMarkup,
                      InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (CommandHandler, Filters,
                          MessageHandler, Updater, ConversationHandler,
                          CallbackContext, CallbackQueryHandler)
from dotenv import load_dotenv
from enum import Enum, auto
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conflict_solution.settings")
django.setup()

from project.models import Situation, Feedback, Advice


class States(Enum):
    MENU = auto()
    SITUATION = auto()
    ANSWERS = auto()
    FEEDBACK = auto()



def start(update, context) -> States:
    user_name = str(update.message.from_user['first_name'])

    message_keyboard = [
        ['Ситуации', "Советы"],
        ['Обратная связь']
                        ]
    markup = ReplyKeyboardMarkup(message_keyboard,
                                 resize_keyboard=True,
                                 one_time_keyboard=True)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
f"""
Привет, {user_name}!

\033[1m{"Путь к согласию"}\033[0m - это бот-психолог, который бесплатно поддержит вас, даст варианты решения выхода из конфликтных ситуаций.

Вот, что у меня есть:
\033[1m{"Ситуации"}\033[0m - здесь вы получите практику выхода из конфликтных ситуаций
\033[1m{"Советы"}\033[0m - вы сможете узнать некоторую информацию по конфликтам
\033[1m{"Обратная связь"}\033[0m - можете оставить отзыв о боте, предложить улучшения или, если что-то пойдет не так, то опишитн проблемы
""",
        reply_markup=markup
    )
    return States.MENU


def situations(update, context) -> States:
    global situation
    situations = Situation.objects.all()
    count = situations.count()
    random_number = random.randint(1, count)
    situation = situations.get(id=random_number)

    rivalry = situation.rivalry
    device = situation.device
    avoidance = situation.avoidance
    compromise = situation.compromise
    cooperation = situation.cooperation

    keyboard = [
        [
            InlineKeyboardButton(rivalry, callback_data="rivalry"),
            InlineKeyboardButton(device, callback_data="device"),
        ],
        [
            InlineKeyboardButton(avoidance, callback_data="avoidance"),
            InlineKeyboardButton(compromise, callback_data="compromise")
        ],
        [
            InlineKeyboardButton(cooperation, callback_data='cooperation')
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        text=situation.situation,
        reply_markup=markup
    )

    return States.SITUATION



def answers(update, context):
    callback_query = update.callback_query
    callback_query.answer()

    rivalry_answer = situation.rivalry_answer
    device_answer = situation.device_answer
    avoidance_answer = situation.avoidance_answer
    compromise_answer = situation.compromise_answer
    cooperation_answer = situation.cooperation_answer

    if callback_query['data'] == "rivalry":
        callback_query.message.reply_text(
            rivalry_answer
        )
    elif callback_query['data'] == "device":
        callback_query.message.reply_text(
            device_answer
        )
    elif callback_query['data'] == "avoidance":
        callback_query.message.reply_text(
            avoidance_answer
        )
    elif callback_query['data'] == "compromise":
        callback_query.message.reply_text(
            compromise_answer
        )
    elif callback_query['data'] == "cooperation":
        callback_query.message.reply_text(
            cooperation_answer
        )

    time.sleep(3)

    keyboard = [
        ['Ещё ситуации', "Главное меню"]
    ]
    markup = ReplyKeyboardMarkup(keyboard,
                                 resize_keyboard=True,
                                 one_time_keyboard=True)
    callback_query.message.reply_text(
        text='Желаете продолжить?',
        reply_markup=markup
    )

    return States.ANSWERS



def advices(update, context) -> States:
    advices = Advice.objects.all()
    count = advices.count()
    random_number = random.randint(1, count)
    advice = advices.get(id=random_number)

    keyboard = [
        ['Ещё совет', "Главное меню"]
    ]
    markup = ReplyKeyboardMarkup(keyboard,
                                 resize_keyboard=True,
                                 one_time_keyboard=True)

    update.message.reply_text(
        text=advice,
        reply_markup=markup
    )

    return States.ANSWERS


def feedback_message(update, context) -> States:
    update.message.reply_text(text="""
Здравствуйте! Здесь можете написать преложения по улучшению работы бота или другие отзывы.

Если возникли какие-то проблемы - пожалуйста, максимально подробно опишите ошибку.
Напишите, что вы делаете, чего ожидаете и что происходит не так.
""")

    return States.FEEDBACK


def feedback_add_to_model(update, context) -> States:
    feedback = update.message.text

    add_feedback = Feedback.objects.create(
        feedback=feedback
    )

    keyboard = [
        ["Главное меню"]
    ]
    markup = ReplyKeyboardMarkup(keyboard,
                                 resize_keyboard=True,
                                 one_time_keyboard=True)

    update.message.reply_text(
        text='Спасибо за ответ, записали!',
        reply_markup=markup
    )

    return States.ANSWERS



if __name__=='__main__':
    load_dotenv()
    tg_bot_token = os.getenv("TG_BOT_TOKEN")

    bot = Bot(token=tg_bot_token)
    updater = Updater(token=tg_bot_token, use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            States.MENU: [
                MessageHandler(
                    Filters.text('Ситуации'), situations
                ),
                MessageHandler(
                    Filters.text("Советы"), advices
                ),
                MessageHandler(
                    Filters.text("Обратная связь"), feedback_message
                ),
            ],
            States.SITUATION: [
                CallbackQueryHandler(
                    answers, pattern='rivalry'
                ),
                CallbackQueryHandler(
                    answers, pattern='device'
                ),
                CallbackQueryHandler(
                    answers, pattern='avoidance'
                ),
                CallbackQueryHandler(
                    answers, pattern='compromise'
                ),
                CallbackQueryHandler(
                    answers, pattern='cooperation'
                ),
            ],
            States.ANSWERS: [
                MessageHandler(
                    Filters.text('Ещё ситуации'), situations
                ),
                MessageHandler(
                    Filters.text('Главное меню'), start
                ),
                MessageHandler(
                    Filters.text('Ещё совет'), advices
                )
            ],
            States.FEEDBACK: [
                MessageHandler(
                    Filters.text, feedback_add_to_model
                )
            ]
        },
        fallbacks=[],
        allow_reentry=True,
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()
