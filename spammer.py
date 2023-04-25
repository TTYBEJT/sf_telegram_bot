from config import TOKEN, chat_id
from utils import update

import telebot
import time

# создание экземпляра бота telebot
bot = telebot.TeleBot(TOKEN)


# Рассылка сообщений
def mailing(sms):
    print("Попытка")
    for chat in chat_id:
        bot.send_message(chat, sms)


# Запуск функции проверки
while True:
    msg = update()
    if msg is not False:
        mailing(msg)
    time.sleep(180)  # 180 секунд = 3 минуты

bot.polling(none_stop=True)

