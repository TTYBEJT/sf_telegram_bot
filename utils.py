from config import four, five, six, seven, usd_b, usd_s, eur_b, eur_s, rub_b, rub_s

from app import bot  # Что с тобой не так?

from bs4 import BeautifulSoup
import random
import requests
import time


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


while True:
    update()  # Функция проверки
    time.sleep(180)  # 180 секунд = 3 минуты
