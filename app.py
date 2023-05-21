import telebot  # pytelegrambotapi
import requests
from telebot import types
from config import TOKEN, github, dev
from utils import update, rates_, calc_dict, calculator, cur_check, amd_rub, manual_input_cal

# создание экземпляра бота telebot
bot = telebot.TeleBot(TOKEN)


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
    bot.reply_to(message, f"Привет, {username}!"
                          f"\nЕсли ты впервые здесь, то советую ознакомиться с моими возможностями😀 [/help]")
    pass


# help - выдача описания и команд для работы с ботом  ---  <Требуемая валюта> <Сумма наличной> <Наличная валюта>
@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.reply_to(message, """Для вывода кнопочного меню на экран, команда [/menu]
Основная валюта бота - рубль, он умеет:
1) Подсказывать курс драма [/rate]
2) Выводить все доступные валюты, с их курсом относительно рубля [/rates]
3) Рассчитывать стоимость валюты. Пример сообщения: [Калькулятор требуется 1500 долларов из рублей]
4) Взамен 3 функции есть кнопочный калькулятор, ищи его в меню!
Функционал бота ограничен, но весьма полезен! Сайт курса валют: Rate.am""")
    pass


# rates - предоставление всех доступных курсов валют
@bot.message_handler(commands=['rates'])
def rates(message):
    bot.reply_to(message, rates_())
    print(message.chat.id)
    pass


# rate - предоставление курса покупки рубля за драмы
@bot.message_handler(commands=['rate'])
def rate(message):
    update()
    bot.reply_to(message, f"""Обновил данные, курс драма сегодня: {round(amd_rub, 2)}""")
    pass


# Хотел сделать команду для добавления (позже и исключения) чат в список для спамера, необходимый для оповещения о
# повышении/понижении курса драма. Пока оставим на потом, хоть и не составляет проблем, вроде)
# - Думаю использовать файл txt для этого, но это позже
@bot.message_handler(commands=['spam'])  # Не работает
def handle_start(message):
    # bot.reply_to(message, f"""Хорошо, я добавил тебя в список спамера. Буду надеяться, что ты этого и хотел)))""")
    pass


# menu - предоставление всех доступных курсов валют
@bot.message_handler(commands=['menu'])
def give_menu(message):
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b_help = types.KeyboardButton("❗ Помощь")
    b_dram = types.KeyboardButton("💸 Курс драма")
    b_rates = types.KeyboardButton("🧾 Доступные курсы")
    b_calc = types.KeyboardButton("🧮 Валютный калькулятор")
    b_other = types.KeyboardButton("📚 Другое")

    menu.add(b_help, b_dram, b_rates, b_calc, b_other)
    bot.reply_to(message, f"""{username_(message)}, меню появилось снизу!""", reply_markup=menu)
    pass


# Меню и обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def bot_message(message):
    msg = message.text
    user = username_(message)

    # Меню взамен команд
    if msg == "❗ Помощь":
        handle_help(message)
    if msg == "💸 Курс драма":
        rate(message)
    if msg == "🧾 Доступные курсы":
        rates(message)

    # Другое
    if msg == "📚 Другое":
        menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        info = types.KeyboardButton("ℹ Информация о боте")
        dev_ = types.KeyboardButton("🔗 Разработчик")
        code = types.KeyboardButton("🏗 Мой код на GitHub")
        back = types.KeyboardButton("🔙 Возврат в меню")
        menu.add(info, dev_, code, back)
        bot.reply_to(message, f"""{user}, тут вся информация что есть обо мне!""", reply_markup=menu)

    if msg == "ℹ Информация о боте":
        bot.reply_to(message, "Этот бот был разработан по программе обучения на сайте SkillFactory,"
                              "а так же доработан и рассчитан под нужды разработчика. "
                              "\nВсе курсы валют, используемых в боте были взяты с сайта Rate.am, "
                              "для удобства и максимальной приближенности к курсу"
                              "в обменниках. \n Страна, для которой это актуально - Республика Армения"
                              "\nРазработчик - Павел (TTYBEJT), 2023 г.")

    if msg == "🔗 Разработчик":
        bot.reply_to(message, f"Для связи с разработчиком держи ссылку: {dev} \nНаписать можешь в любой момент, "
                              f"но вот ответит он, скорее всего, после 19.00 по будням, выходные - по загруженности")

    if msg == "🏗 Мой код на GitHub":
        bot.reply_to(message, f"Если тебе интересен мой код он загружен на GitHub: {github}")

    # Самостоятельный ввод функции калькулятора
    if str(msg[:11:]).lower() == "калькулятор":
        ans = manual_input_cal(msg, user)
        bot.reply_to(message, ans)

    # Кнопка возврата в меню
    if msg == "🔙 Возврат в меню":
        give_menu(message)

    # Меню калькулятора (Первичное)
    if msg == "🧮 Валютный калькулятор":
        calc_dict(user)
        menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        b_to = types.KeyboardButton("В какую валюту")
        b_from = types.KeyboardButton("Из какой валюты")
        b_money = types.KeyboardButton("Сумма")
        b_calc_to = types.KeyboardButton("Счет: сумма требуется")
        b_calc_from = types.KeyboardButton("Счет: сумма имеется")
        back = types.KeyboardButton("🔙 Возврат в меню")
        menu.add(b_to, b_from, b_money, b_calc_to, b_calc_from, back)
        bot.reply_to(message, f"""{user}, Выбирай с чего начнем!""", reply_markup=menu)

    # Выбираем в какую валюту
    if msg == "В какую валюту":
        menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        rub = types.KeyboardButton("В ₽ Рубли")
        amd = types.KeyboardButton("В ֏ Драмы")
        usd = types.KeyboardButton("В $ Доллары")
        eur = types.KeyboardButton("В € Евро")
        back = types.KeyboardButton("🔙 Возврат в меню калькулятора")

        menu.add(rub, amd, usd, eur, back)
        bot.reply_to(message, f"""Выбирай валюту в которую будем переводить!""", reply_markup=menu)

    # Выбираем из какой валюты
    if msg == "Из какой валюты":
        menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        rub = types.KeyboardButton("Из ₽ Рублей")
        amd = types.KeyboardButton("Из ֏ Драмов")
        usd = types.KeyboardButton("Из $ Долларов")
        eur = types.KeyboardButton("Из € Евро")
        back = types.KeyboardButton("🔙 Возврат в меню калькулятора")

        menu.add(rub, amd, usd, eur, back)
        bot.reply_to(message, f"""Окей, выбирай валюту из которой будем переводить!""", reply_markup=menu)

    # Сохранение валюты
    if msg[0:3] == "Из " or msg[0:2] == "В ":
        ret = cur_check(msg, user)
        if ret:
            menu_calc(message)

    # Выбираем сумму
    if msg == "Сумма":
        menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("💰 1")
        button2 = types.KeyboardButton("💰 5")
        button3 = types.KeyboardButton("💰 10")
        button4 = types.KeyboardButton("💰 50")
        button5 = types.KeyboardButton("💰 100")
        button6 = types.KeyboardButton("💰 500")
        button7 = types.KeyboardButton("💰 1000")
        button8 = types.KeyboardButton("💰 5000")
        button9 = types.KeyboardButton("Сам введу...")
        back = types.KeyboardButton("🔙 Возврат в меню калькулятора")

        menu.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, back)
        bot.reply_to(message, f"""Допустим... 
Выбирай сумму или вводи нужную тебе!
Вводить необходимо сумму в формате сообщения <Сумма 9999> или <💰 9999>!
По другому не понимаю! И да, читать прописью числа я тоже не умею.""", reply_markup=menu)

        # самостоятельный ввод

    if msg == "Сам введу...":
        menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("💰 1")
        button2 = types.KeyboardButton("💰 9999")
        button3 = types.KeyboardButton("😁 Да так, просто)0)")
        back = types.KeyboardButton("🔙 Возврат в меню калькулятора")

        menu.add(button1, button2, button3, back)
        bot.reply_to(message, f"""Говорить мне это не было нужды. 
Вводить необходимо сумму в формате сообщения <Сумма 9999> или <💰 9999>!
По другому не понимаю! И да, читать прописью числа я тоже не умею.""", reply_markup=menu)

    if msg == "😁 Да так, просто)0)":
        menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("💰 1")
        button2 = types.KeyboardButton("💰 9999")
        back = types.KeyboardButton("🔙 Возврат в меню калькулятора")

        menu.add(button1, button2, back)
        bot.reply_to(message, f"""Посмотрите на шутника) Лишняя это кнопка! 
Вводи давай сумму в формате сообщения:\n <Сумма 9999> или <💰 9999>!
По другому не понимаю! И да, читать прописью числа я тоже не умею.""", reply_markup=menu)

    # Проверка суммы
    if msg[0:2] == "💰 ":
        money = str(msg[2:]).replace(",", ".")
        try:
            money = float(money)
            calc_dict(user, money=money)
            return menu_calc(message)
        except ValueError:
            print("money-", money)
            bot.reply_to(message, "Подожди!"
                                  "\nЯ не понимаю, что ты написал, давай снова и цифрами!")
            return in_in(message)

    # Проверка суммы со словом (сумма)
    if str(msg[0:6]).lower() == "сумма ":
        bot.reply_to(message, "А ты не из ленивых)")
        money = str(msg[6:]).replace(",", ".")
        try:
            money = float(money)
            calc_dict(user, money=money)
            return menu_calc(message)
        except ValueError:
            print("money-", money)
            bot.reply_to(message, "Подожди!"
                                  "\nЯ не понимаю, что ты написал, давай снова и цифрами!"
                                  f"\n{money} - это не число!")
            return in_in(message)

    # Запуск просчетов
    # Счет: сумма - требуемая
    if msg == "Счет: сумма требуется":
        s = 0
        ans = calculator(user, s)
        bot.reply_to(message, ans, parse_mode="html")

    # Счет: сумма - в наличии
    if msg == "Счет: сумма имеется":
        s = 1
        ans = calculator(user, s)
        bot.reply_to(message, ans, parse_mode="html")

    # Возврат в меню калькулятора
    if msg == "🔙 Возврат в меню калькулятора":
        menu_calc(message)

    else:
        print(user, "написал", msg)


# Меню калькулятора
def menu_calc(message):
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b_to = types.KeyboardButton("В какую валюту")
    b_from = types.KeyboardButton("Из какой валюты")
    b_money = types.KeyboardButton("Сумма")
    b_calc_to = types.KeyboardButton("Счет: сумма требуется")
    b_calc_from = types.KeyboardButton("Счет: сумма имеется")
    back = types.KeyboardButton("🔙 Возврат в меню")
    menu.add(b_to, b_from, b_money, b_calc_to, b_calc_from, back)
    bot.reply_to(message, f"""{username_(message)}, мы в меню калькулятора.""", reply_markup=menu)


# Incorrect input - Неправильный ввод числа
def in_in(message):
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("💰 1")
    button2 = types.KeyboardButton("💰 9999")
    button3 = types.KeyboardButton("😁😁😁")
    back = types.KeyboardButton("🔙 Возврат в меню калькулятора")

    menu.add(button1, button2, button3, back)
    bot.reply_to(message, f"""Давай снова. 
Вводи сумму в формате сообщения <Сумма 9999> или <💰 9999>!
По другому не понимаю! И да, читать прописью числа я тоже не умею.""", reply_markup=menu)


try:
    bot.polling(none_stop=True)
except requests.exceptions.ConnectionError:
    pass

# Запуск бота без помех (ну или игнорируем, x3)
