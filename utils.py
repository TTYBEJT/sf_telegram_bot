from config import four, five, six, seven, users_cal, cur_cal, usd, eur, rub, amd, cur_cal_invert, cur_cal_msg

from bs4 import BeautifulSoup
import random
import requests

# Создаем переменные для хранения курсов валют
# (курсы инвертированные из-за сайта - поздно заметил, теперь исправлять тяжело)
amd_rub: float = 0.00  # Покупаем рубль
rub_amd: float = 0.00  # Продаем рубль
usd_s: float = 0.00  # Покупаем доллар
usd_b: float = 0.00  # Продаем доллар
eur_s: float = 0.00  # Покупаем евро
eur_b: float = 0.00  # Продаем евро
amd_s: float = 0.00  # Покупаем драм
amd_b: float = 0.00  # Продаем драм

# Словари для хранения курсов валют (Покупка и продажа)
cal_s = {
    "usd": 0.00,
    "eur": 0.00,
    "amd": 0.00
}
cal_b = {
    "usd": 0.00,
    "eur": 0.00,
    "amd": 0.00
}


# Обновление курса
def checker():
    base = 'https://rate.am/ru/armenian-dram-exchange-rates/banks/cash'
    html = requests.get(base).content
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('table', id='rb')
    tr = table.find_all('tr', class_='btm')
    td = tr[1].find_all('td', class_='fhd')
    u_b, u_s, e_b = float(td[1].getText()), float(td[2].getText()), float(td[3].getText())
    e_s, ar_b, ar_s = float(td[4].getText()), float(td[5].getText()), float(td[6].getText())
    # Переводим курс с драма на рубли (опорная валюта)
    u_b = u_b / ar_s  # Продажа доллара
    u_s = u_s / ar_b  # Покупка доллара
    e_b = e_b / ar_s  # Продажа евро
    e_s = e_s / ar_b  # Покупка евро
    a_b = 1 / ar_s  # Продажа драма
    a_s = 1 / ar_b  # Покупка драма
    return u_b, u_s, e_b, e_s, ar_s, ar_b, a_b, a_s  # Здесь я меняю местами покупку и продажу рубля, чтобы обратить
    # значение покупки/продажи с рубля на драм (аля мы не рубль теперь покупаем, а драм)


# События со снижением курса
def bad(rate):
    n = random.randint(1, 3)
    variants = {
        1: f"Новости ухудшаются, пора доставать перчатки для проверки мусорок, ведь курс упал и он теперь ниже {rate}... Точнее: {amd_rub}",
        2: f"Ну что же, друзья, мы медленно катимся ко дну... Курс опустился ниже {rate}. Точнее: {amd_rub}",
        3: f"Этот мир на нас обижен... Курс опустился ниже {rate}. Точнее: {amd_rub}"
    }
    return variants.get(n)


# События с повышением курса
def good(rate):
    n = random.randint(1, 4)
    variants = {
        1: f"Ого, пойдемте покупать продукты, с этих пор мы сможем не лазить в мусорках, ведь курс поднялся выше {rate}, сейчас он {amd_rub}",
        2: f"Мы можем выходить в город, курс поднялся выше {rate}, сейчас он колеблется в районе {amd_rub}",
        3: f"Ура, пора гулять, ведь курс поднялся выше {rate}, если быть точнее, то он {amd_rub}",
        4: f"Время исполнения желаний, ну почти... Курс поднялся выше {rate}! Сейчас он колеблется в районе {amd_rub}"
    }
    return variants.get(n)


# Апдейтор и проверка курса :D
def update():
    global usd_b, usd_s, eur_b, eur_s, rub_amd, amd_rub, amd_b, amd_s, cal_b, cal_s
    rub_check = amd_rub
    usd_b, usd_s, eur_b, eur_s, rub_amd, amd_rub, amd_b, amd_s = checker()
    up_b = {"usd": usd_b, "eur": eur_b, "amd": amd_b}
    up_s = {"usd": usd_s, "eur": eur_s, "amd": amd_b}
    cal_b.update(up_b)
    cal_s.update(up_s)
    if rub_check != amd_rub:
        print("Курс изменился!")
        if rub_check < four < amd_rub:
            print(good(four))
            return good(four)
        if rub_check < five < amd_rub:
            print(good(five))
            return good(five)
        if rub_check < six < amd_rub:
            print(good(six))
            return good(six)
        if rub_check < seven < amd_rub:
            print(good(seven))
            return good(seven)
        if rub_check > four > amd_rub:
            print(bad(four))
            return bad(four)
        if rub_check > five > amd_rub:
            print(bad(five))
            return bad(five)
        if rub_check > six > amd_rub:
            print(bad(six))
            return bad(six)
        if rub_check > seven > amd_rub:
            print(bad(seven))
            return bad(seven)
    return False


# Доступные курсы валют
def rates_():
    update()
    text = f"""rub: 
при покупке ₽- {round(amd_rub, 2)}֏; при продаже ₽- {round(rub_amd, 2)}֏
usd: 
при покупке $- {round(usd_s, 2)}₽; при продаже $- {round(usd_b, 2)}₽
eur: 
при покупке €- {round(eur_s, 2)}₽; при продаже €- {round(eur_b, 2)}₽
amd: 
при покупке ֏- {round(amd_s, 2)}₽; при продаже ֏- {round(amd_b, 2)}₽
"""
    return text


# Добавление в память калькулятора данные пользователя
def calc_dict(user, from_=None, to_=None, money: float = None):
    user_d = {}
    if user not in users_cal.keys():
        user_d = {"from_": from_, "to_": to_, "money": money}
        d_user = {f"{user}": user_d}
        users_cal.update(d_user)
    else:
        user_d = users_cal.get(user)
    if from_ is not None:
        from_cur = from_
        upd = {"from_": from_cur}
        user_d.update(upd)
        d_user = {f"{user}": user_d}
        users_cal.update(d_user)
    if to_ is not None:
        to_cur = to_
        upd = {"to_": to_cur}
        user_d.update(upd)
        d_user = {f"{user}": user_d}
        users_cal.update(d_user)
    if money is not None:
        money_cur = money
        upd = {"money": money_cur}
        user_d.update(upd)
        d_user = {f"{user}": user_d}
        users_cal.update(d_user)


# Постановка на учет валют (Названия)
def cur_check(msg, user):
    prepos = None  # preposition - Предлог (из/в)
    cur_ = None  # Валюта
    if msg[0:3] == "Из ":
        prepos = 1
    elif msg[0:2:] == "В ":
        prepos = 2
    if prepos == 1:
        cur_ = msg[3]
    elif prepos == 2:
        cur_ = msg[2]
    if cur_ in cur_cal:
        for a in cur_cal.keys():
            if cur_ == a:
                cur_ = cur_cal.get(a)
        if prepos == 1:
            calc_dict(user, cur_)
            return True
        elif prepos == 2:
            calc_dict(user, to_=cur_)
            return True
    return False


def calculator(user, side_sum):
    if user not in users_cal.keys():
        return "Данных маловато, может ты удосужишься мне их предоставить???"

    user_d = users_cal.get(user)

    if user_d.get("money") == 0:
        return "Данных маловато, может ты удосужишься мне сказать мне <b>сумму</b>???"
    elif user_d.get("from_") is None:
        return "Данных маловато, может ты удосужишься мне сказать из [какой валюты]???"
    elif user_d.get("to_") is None:
        return "Данных маловато, может ты удосужишься мне сказать в [какую валюту]???"

    money = user_d.get("money")
    from_ = user_d.get("from_")
    to_ = user_d.get("to_")
    to_cur = cur_cal_invert.get(to_)
    from_cur = cur_cal_invert.get(from_)

    if from_ == to_:
        return f"Ну ты и зануда, {user}, кончено. Ну ок! Даже не буду смотреть нужно или требуется!" \
                     f" Просто: {round(money, 2)} {to_cur} {to_}. Будешь смотреть какие валюты вводишь!"

    elif side_sum == 0:  # Требуется
        if from_ == rub:
            ans = money * cal_s.get(to_)
        elif to_ == rub:
            ans = money / cal_b.get(from_)
        else:
            ans = money * cal_s.get(to_) / cal_b.get(from_)
        ans = f"""Блин, это было слишком сложно, больше так не делай! Но я не такой тупой!
Если тебе нужно {round(money, 2)} {to_cur} {to_}, то придется отдать {round(ans, 2)} {from_cur} {from_}!"""
        return ans

    elif side_sum == 1:  # Имеется
        if from_ == rub:
            ans = money / cal_b.get(to_)
        elif to_ == rub:
            ans = money * cal_s.get(from_)
        else:
            ans = money * cal_b.get(to_) / cal_s.get(from_)
        ans = f"""Блин, это было слишком сложно, больше так не делай! Но я не такой тупой!
Отдав {round(money, 2)} {from_cur} {from_}, ты получишь {round(ans, 2)} {to_cur} {to_}!"""
        return ans

    else:
        print(f"У {user}, случилась ошибка")
        return "Что-то пошло не так, ты данные все дал?"


def manual_input_cal(msg, user):
    msg_l = str(msg).split()
    try:
        if str(msg_l[1]).lower() == "требуется":
            side_sum = 0
        elif str(msg_l[1]).lower() == "имеется":
            side_sum = 1
        else:
            ans = "Не могу тебя понять, вторым словом должны быть или [требуется], или [имеется]! Повтори запрос)"
            return ans
        money = str(msg_l[2]).replace(",", ".")
        try:
            money = float(money)
        except ValueError:
            ans = "Третье значение - должно быть числом, попробуй снова!"
            return ans
        first_cur = str(msg_l[3]).lower()
        two_cur = str(msg_l[5]).lower()
        if first_cur in cur_cal_msg.keys():
            if two_cur in cur_cal_msg.keys():
                if side_sum == 0:
                    from_ = cur_cal_msg.get(two_cur)
                    to_ = cur_cal_msg.get(first_cur)
                elif side_sum == 1:
                    to_ = cur_cal_msg.get(two_cur)
                    from_ = cur_cal_msg.get(first_cur)
            else:
                ans = "Не понимаю вторую валюту которая тебе нужна! Напоминаю, что я умею работать только с рублями," \
                      " драмами, долларами и евро. Выбери одну из них или напиши корректнее (Я понимаю валюты только " \
                      "полным названием, например: калькулятор требуется 1500 [рублей] в [доллар])"
                return ans
        else:
            ans = "Не понимаю первую валюту которая тебе нужна! Напоминаю, что я умею работать только с рублями, " \
                  "драмами, долларами и евро. Выбери одну из них или напиши корректнее (Я понимаю валюты только " \
                  "полным названием, например: калькулятор требуется 1500 [рублей] в [доллар])"
            return ans
    except IndexError:
        ans = "Ты ввел слишком мало значений, вводи по примеру: калькулятор требуется 1500 рублей в доллар"
        return ans

    calc_dict(user, from_, to_, money)
    ans = calculator(user, side_sum)
    return ans


update()
