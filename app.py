import telebot
import requests
import sched
import time
from bs4 import BeautifulSoup
import random
import asyncio

# TOKEN = "6074047522:AAEVGXN4uk7wkgt8PdfPZEjnNT89b-v5tfw"


TOKEN = "6016539624:AAFVQDjxs1Ig1uOgQT7Skrb4VT14rHFgkgc"

bot = telebot.TeleBot(TOKEN)

four, five, six, seven = 4.0, 5.0, 6.0, 7.0

rub_s: float = 0.0
rub_b: float = 0.0
usd_s: float = 0.0
usd_b: float = 0.0
eur_s: float = 0.0
eur_b: float = 0.0


def username_(message):
    username = message.from_user.username
    username = message.from_user.first_name if not username else username
    return username


def mailing(sms):
    chats = bot.get_updates()
    for chat in chats:
        chat_id = chat.message.chat.id
        bot.send_message(chat_id, sms)


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


def bad(rate):  # События со снижением курса
    n = random.randint(1, 3)
    variants = {
        1: f"Новости ухудшаются, пора доставать перчатки для проверки мусорок, ведь курс упал и он теперь ниже {rate}... Точнее: {rub_b}",
        2: f"Ну что же, друзья, мы медленно катимся ко дну... Курс опустился ниже {rate}. Точнее: {rub_b}",
        3: f"Этот мир на нас обижен... Курс опустился ниже {rate}. Точнее: {rub_b}"
        }
    return variants.get(n)


def good(rate):  # События с повышением курса
    n = random.randint(1, 4)
    variants = {
        1: f"Ого, пойдемте покупать продукты, с этих пор мы сможем не лазить в мусорках, ведь курс поднялся выше {rate}, сейчас он {rub_b}",
        2: f"Мы можем выходить в город, курс поднялся выше {rate}, сейчас он колеблется в районе {rub_b}",
        3: f"Ура, пора гулять, ведь курс поднялся выше {rate}, если быть точнее, то он {rub_b}",
        4: f"Время исполнения желаний, ну почти... Курс поднялся выше {rate}! Сейчас он колеблется в районе {rub_b}"
        }
    return variants.get(n)


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
        if rub_check < six < rub_b:
            print(good(six))
        if rub_check < seven < rub_b:
            print(good(seven))
        if rub_check > four > rub_b:
            print(bad(four))
        if rub_check > five > rub_b:
            print(bad(five))
        if rub_check > six > rub_b:
            print(bad(six))
        if rub_check > seven > rub_b:
            print(bad(seven))
        print("Проверку провел!")
    return


async def check_every_3_minutes():
    while True:
        update()  # Функция проверки
        await asyncio.sleep(180)  # 180 секунд = 3 минуты


async def main():
    # Запуск функции проверки
    await check_every_3_minutes()


@bot.message_handler(commands=['start', 'hello'])
def handle_start(message):
    username = username_(message)
    bot.reply_to(message, f"Привет, {username}! Давай начнем!")
    pass


asyncio.run(main())

bot.polling(none_stop=True)
