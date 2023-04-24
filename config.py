TOKEN = None
with open("token.txt") as f:
    TOKEN = f.read().strip()

# обозначаем данные для проверки
four, five, six, seven = 4.0, 5.0, 6.0, 7.0

# Создаем переменные для хранения курсов валют
rub_s: float = 0.0
rub_b: float = 0.0
usd_s: float = 0.0
usd_b: float = 0.0
eur_s: float = 0.0
eur_b: float = 0.0
