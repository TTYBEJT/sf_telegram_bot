from config import TOKEN, chat_id
from utils_spammer import update

import telebot
import time

# создание экземпляра бота telebot
bot = telebot.TeleBot(TOKEN)


# Рассылка сообщений
def mailing(sms):
    print("Изменения прошли)))")
    for chat in chat_id:
        bot.send_message(chat, sms)


att = 0
# Запуск функции проверки
while True:
    att += 1
    msg = update()
    if msg is not False:
        mailing(msg)
    time.sleep(180)  # 180 секунд = 3 минуты
    if att == 20:
        print("Прошел еще час моей работы, а изменений нет")
        att -= 20

bot.polling(none_stop=True)

