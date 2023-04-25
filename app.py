import telebot
import time
from config import TOKEN, four, five, six, seven, usd_b, usd_s, eur_b, eur_s, rub_b, rub_s
from utils import update

# создание экземпляра бота telebot
bot = telebot.TeleBot(TOKEN)


# Определение Username
def username_(message):
    username = message.from_user.username
    username = message.from_user.first_name if not username else username
    return username


# Рассылка сообщений
def mailing(sms):
    chats = bot.get_updates()
    print(chats)
    for chat in chats:
        chat_id = chat.message.chat.id
        bot.send_message(chat_id, sms)


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
    bot.reply_to(message, "Основная валюта бота - рубль, он умеет:"
                          "1) Подсказывать курс драма [/rate]"
                          "2) Выводить все доступные валюты, с их курсом относительно рубля [/rates]"
                          "3) Рассчитывать стоимость валюты [<Требуемая валюта> <Сумма> <Наличная валюта>]"
                          "Функционал бота ограничен, но весьма полезен! Сайт курса валют: Rate.am")
    pass


# rates - предоставление всех доступных курсов валют
@bot.message_handler(commands=['rates'])
def handle_help(message):
    bot.reply_to(message, "Ты думаешь я такой умный?!")
    pass


# Запуск бота без помех (ну или игнорируем, x3)
bot.polling(none_stop=True)

# Запуск функции проверки
while True:
    sms = update()
    if sms is not False:
        mailing(sms)
    time.sleep(180)  # 180 секунд = 3 минуты


