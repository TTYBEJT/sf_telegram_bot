import telebot
import time
from config import TOKEN
from utils import update, usd_b, usd_s, eur_b, eur_s, rub_b, rub_s

# создание экземпляра бота telebot
bot = telebot.TeleBot(TOKEN)

# chats = bot.get_updates()
# print(chats)


# Определение Username
def username_(message):
    username = message.from_user.username
    username = message.from_user.first_name if not username else username
    return username


# Команды бота
# обработчик команд для telebot

# start and hello - Запуск и приветствие
@bot.message_handler(commands=['start', 'hello'])
def handle_start(message):
    username = username_(message)
    bot.reply_to(message, f"Привет, {username}! Давай начнем!")
    pass


# help - выдача описания и команд для работы с ботом
@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.reply_to(message, """Основная валюта бота - рубль, он умеет:
1) Подсказывать курс драма [/rate]
2) Выводить все доступные валюты, с их курсом относительно рубля [/rates]
3) Рассчитывать стоимость валюты [<Требуемая валюта> <Сумма наличной> <Наличная валюта>]
Функционал бота ограничен, но весьма полезен! Сайт курса валют: Rate.am""")
    pass


# rates - предоставление всех доступных курсов валют
@bot.message_handler(commands=['rates'])
def handle_help(message):
    mailing("k")
    bot.reply_to(message, "Ты думаешь я такой умный?!")
        # print(bot.get_updates().chat.id)
    pass


@bot.message_handler(commands=['rate'])
def handle_start(message):
    bot.reply_to(message, f"""Курс драма сегодня примерно: {rub_b}
Не забывай, что курс в обменнике и в интернете разнится в плоть до ± 0,1!
Хотя обычно разница не превышает 0,02-0,03""")
    pass


# Запуск бота без помех (ну или игнорируем, x3)
bot.polling(none_stop=True)


