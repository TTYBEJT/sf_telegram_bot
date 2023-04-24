import telebot
# import aiogram
import requests
import sched
import time
from bs4 import BeautifulSoup
import random
import asyncio
import logging
import threading

# TOKEN = "6074047522:AAEVGXN4uk7wkgt8PdfPZEjnNT89b-v5tfw"

TOKEN = "6016539624:AAFVQDjxs1Ig1uOgQT7Skrb4VT14rHFgkgc"

# настройки логгера
logging.basicConfig(level=logging.INFO)

# создание экземпляра бота telebot
bot = telebot.TeleBot(TOKEN)
# создание экземпляра бота aiogram
# bot = aiogram.Bot(token=TOKEN)

# обозначаем данные для проверки
four, five, six, seven = 4.0, 5.0, 6.0, 7.0

# Создаем переменные для хранения курсов валют
rub_s: float = 0.0
rub_b: float = 0.0
usd_s: float = 0.0
usd_b: float = 0.0
eur_s: float = 0.0
eur_b: float = 0.0

# создание экземпляра класса Dispatcher, который управляет обработкой сообщений
# dp = aiogram.Dispatcher(bot)


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


# Обновление курса
def checker():
    base = 'https://rate.am/ru/armenian-dram-exchange-rates/banks/cash'
    html = requests.get(base).content
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('table', id='rb')
    tr = table.find_all('tr', class_='btm')
    td = tr[1].find_all('td', class_='fhd')
    u_b, u_s, e_b = float(td[1].getText()), float(td[2].getText()), float(td[3].getText())
    e_s, r_b, r_s = float(td[4].getText()), float(td[5].getText()), float(td[6].getText())
    return u_b, u_s, e_b, e_s, r_b, r_s


# События со снижением курса
def bad(rate):
    n = random.randint(1, 3)
    variants = {
        1: f"Новости ухудшаются, пора доставать перчатки для проверки мусорок, ведь курс упал и он теперь ниже {rate}... Точнее: {rub_b}",
        2: f"Ну что же, друзья, мы медленно катимся ко дну... Курс опустился ниже {rate}. Точнее: {rub_b}",
        3: f"Этот мир на нас обижен... Курс опустился ниже {rate}. Точнее: {rub_b}"
    }
    return variants.get(n)


# События с повышением курса
def good(rate):
    n = random.randint(1, 4)
    variants = {
        1: f"Ого, пойдемте покупать продукты, с этих пор мы сможем не лазить в мусорках, ведь курс поднялся выше {rate}, сейчас он {rub_b}",
        2: f"Мы можем выходить в город, курс поднялся выше {rate}, сейчас он колеблется в районе {rub_b}",
        3: f"Ура, пора гулять, ведь курс поднялся выше {rate}, если быть точнее, то он {rub_b}",
        4: f"Время исполнения желаний, ну почти... Курс поднялся выше {rate}! Сейчас он колеблется в районе {rub_b}"
    }
    return variants.get(n)


# Апдейтор и проверятор курса :D
def update():
    global usd_b, usd_s, eur_b, eur_s, rub_b, rub_s
    rub_check = rub_b
    usd_b, usd_s, eur_b, eur_s, rub_b, rub_s = checker()
    if rub_check != rub_b:
        if rub_check < four < rub_b:
            print(good(four))
            mailing(good(four))
        if rub_check < five < rub_b:
            print(good(five))
            mailing(good(five))
        if rub_check < six < rub_b:
            print(good(six))
            mailing(good(six))
        if rub_check < seven < rub_b:
            print(good(seven))
            mailing(good(seven))
        if rub_check > four > rub_b:
            print(bad(four))
            mailing(bad(four))
        if rub_check > five > rub_b:
            print(bad(five))
            mailing(bad(five))
        if rub_check > six > rub_b:
            print(bad(six))
            mailing(bad(six))
        if rub_check > seven > rub_b:
            print(bad(seven))
            mailing(bad(seven))
        print("Курс изменился!")
    return


# Асинхронный запуск функции проверки курса и таймер на 3 минуты
async def check_every_3_minutes():
    while True:
        update()  # Функция проверки
        await asyncio.sleep(180)  # 180 секунд = 3 минуты


# Стартер циклического двигателя проверятора
async def main():
    # Запуск функции проверки
    await check_every_3_minutes()


# Команды бота
# обработчик команд для aiogram
'''
@dp.message_handler(commands=['test'])
async def process_start_command(message: aiogram.types.Message):
    await message.reply("Test!")


# start and hello - Запуск и приветствие (банально))
@dp.message_handler(commands=['start', 'hello'])
async def handle_start(message):
    username = username_(message)
    await message.reply(message, f"Привет, {username}! Давай начнем!")


# help - выдача описания и команд для работы с ботом
@dp.message_handler(commands=['help'])
async def handle_help(message):
    await message.reply(message, "Основная валюта бота - рубль, он умеет:"
                          "1) Подсказывать курс драма [/rate]"
                          "2) Выводить все доступные валюты, с их курсом относительно рубля [/rates]"
                          "3) Рассчитывать стоимость валюты [<Требуемая валюта> <Сумма> <Наличная валюта>]"
                          "Функционал бота ограничен, но весьма полезен! Сайт курса валют: Rate.am")


# rates - предоставление всех доступных курсов валют
@dp.message_handler(commands=['rates'])
async def handle_help(message):
    await message.reply(message, "Ты думаешь я такой умный?!")
'''


# обработчик команд для telebot

# start and hello - Запуск и приветствие (банально))
@bot.message_handler(commands=['start', 'hello'])
async def handle_start(message):
    username = username_(message)
    bot.reply_to(message, f"Привет, {username}! Давай начнем!")
    pass


# help - выдача описания и команд для работы с ботом
@bot.message_handler(commands=['help'])
async def handle_help(message):
    await bot.reply_to(message, "Основная валюта бота - рубль, он умеет:"
                          "1) Подсказывать курс драма [/rate]"
                          "2) Выводить все доступные валюты, с их курсом относительно рубля [/rates]"
                          "3) Рассчитывать стоимость валюты [<Требуемая валюта> <Сумма> <Наличная валюта>]"
                          "Функционал бота ограничен, но весьма полезен! Сайт курса валют: Rate.am")


# rates - предоставление всех доступных курсов валют
@bot.message_handler(commands=['rates'])
async def handle_help(message):
    bot.reply_to(message, "Ты думаешь я такой умный?!")
    pass


# запуск бота
'''if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling())
    loop.run_forever()
'''

thread = threading.Thread(target=asyncio.run(main()))
thread.start()


async def bot_polling():
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(e)
            await asyncio.sleep(15)


async def main():
    asyncio.create_task(bot_polling())

if __name__ == '__main__':
    asyncio.run(main())
