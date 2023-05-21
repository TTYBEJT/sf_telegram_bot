TOKEN = None
# Получаем токен из файла
with open("token.txt") as f:
    TOKEN = f.read().strip()

# обозначаем данные для проверки
four, five, six, seven = 4.0, 5.0, 6.0, 7.0

# ID чатов для рассылки спамера
chat_id = [5874280484, 1605959211, -1001890552513, -1001783154637]

# Профили юзеров калькулятора
users_cal = {}

# Валюты калькулятора
cur_cal = {"₽": "rub",
           "֏": "amd",
           "$": "usd",
           "€": "eur"}

cur_cal_msg = {"рубль": "rub",
               "рубли": "rub",
               "рублей": "rub",
               "драм": "amd",
               "драмм": "amd",
               "драмов": "amd",
               "драма": "amd",
               "доллар": "usd",
               "доллара": "usd",
               "доллары": "usd",
               "долларов": "usd",
               "евро": "eur"}

rub = "rub"
amd = "amd"
usd = "usd"
eur = "eur"

# Валюты калькулятора инвертированные для ответа
cur_cal_invert = {"rub": "₽",
                  "amd": "֏",
                  "usd": "$",
                  "eur": "€"}

# Ссылка на гитхаб
github = "https://github.com/TTYBEJT/sf_telegram_bot"

# мой профиль для связи в телеграмм
dev = "@puvek"
