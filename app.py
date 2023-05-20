import telebot  # pytelegrambotapi
import requests
from telebot import types
from config import TOKEN, users_cal, cur_cal_msg, chat_id
from utils import update, rates_, calc_dict, calculator, cur_check, amd_rub, manual_input_cal

# создание экземпляра бота telebot
bot = telebot.TeleBot(TOKEN)

# for chat in chat_id:
#     bot.send_message(chat, "Ебать, я, вроде, живой блять! Так еще и с калькулятором)))")


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
    bot.reply_to(message, f"Саламчик, {username}!")
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


@bot.message_handler(commands=['rate'])
def rate(message):
    bot.reply_to(message, f"""Я че, по твоему банкомат, чтобы знать курс? Иди в обменник и узнавай свой курc!
И вообще, давай гуляй!""")
    update()
    bot.reply_to(message, f"""Хотя ладно, курс сегодня вроде: {round(amd_rub, 2)}
Но ты все равно идешь гулять!""")
    pass


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
    b_other = types.KeyboardButton("❌ Другое")

    menu.add(b_help, b_dram, b_rates, b_calc, b_other)
    bot.reply_to(message, f"""{username_(message)}, меню появилось снизу!""", reply_markup=menu)
    pass


@bot.message_handler(content_types=['text'])
def bot_message(message):
    msg = message.text
    user = username_(message)

    # Меню
    if msg == "❗ Помощь":
        handle_help(message)
    if msg == "💸 Курс драма":
        rate(message)
    if msg == "🧾 Доступные курсы":
        rates(message)
    if msg == "❌ Другое":
        bot.reply_to(message, f"""Тут еще ничего нет""")

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
        bot.reply_to(message, f"""{user}, заставляешь работать меня? Ну допустим! 
Выбирай с чего начнем.""", reply_markup=menu)

    # Выбираем в какую валюту
    if msg == "В какую валюту":
        menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        rub = types.KeyboardButton("В ₽ Рубли")
        amd = types.KeyboardButton("В ֏ Драмы")
        usd = types.KeyboardButton("В $ Доллары")
        eur = types.KeyboardButton("В € Евро")
        back = types.KeyboardButton("🔙 Возврат в меню калькулятора")

        menu.add(rub, amd, usd, eur, back)
        bot.reply_to(message, f"""Окей... 
Выбирай валюту в которую будем переводить!""", reply_markup=menu)

    # Выбираем из какой валюты
    if msg == "Из какой валюты":
        menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        rub = types.KeyboardButton("Из ₽ Рублей")
        amd = types.KeyboardButton("Из ֏ Драмов")
        usd = types.KeyboardButton("Из $ Долларов")
        eur = types.KeyboardButton("Из € Евро")
        back = types.KeyboardButton("🔙 Возврат в меню калькулятора")

        menu.add(rub, amd, usd, eur, back)
        bot.reply_to(message, f"""Окей... 
Выбирай валюту в которую будем переводить!""", reply_markup=menu)

    # Сохранение валюты
    if msg[0:3] == "Из " or msg[0:2] == "В ":
        ret = cur_check(msg, user)
        if ret:
            bot.reply_to(message, "Ага, давай.")
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
Выбирай сумму или вводи нужную тебе!""", reply_markup=menu)

        # самостоятельный ввод

    if msg == "Сам введу...":
        menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("💰 1")
        button2 = types.KeyboardButton("💰 9999")
        button3 = types.KeyboardButton("😁 Да так, просто)0)")
        back = types.KeyboardButton("🔙 Возврат в меню калькулятора")

        menu.add(button1, button2, button3, back)
        bot.reply_to(message, f"""И на кой ляд ты мне это сказал??? 
Вводи тогда сумму в формате сообщения <Сумма 9999> или <💰 9999>!
Напишешь по другому, даже читать не буду! И да, читать прописью числа я тоже не буду!""", reply_markup=menu)

    if msg == "😁 Да так, просто)0)":
        menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("💰 1")
        button2 = types.KeyboardButton("💰 9999")
        back = types.KeyboardButton("🔙 Возврат в меню калькулятора")

        menu.add(button1, button2, back)
        bot.reply_to(message, f"""Ты зачем тратишь мое время??? Лишняя это кнопка! 
Вводи давай сумму в формате сообщения:\n <Сумма 9999> или <💰 9999>!
Напишешь по другому, даже читать не буду! И да, читать прописью числа я тоже не буду!""", reply_markup=menu)

    # Проверка суммы
    if msg[0:2] == "💰 ":
        bot.reply_to(message, "Принял.")
        money = str(msg[2:]).replace(",", ".")
        try:
            money = float(money)
            calc_dict(user, money=money)
            return menu_calc(message)
        except ValueError:
            print("money-", money)
            bot.reply_to(message, "Хотя стой! Угараешь что-ли? Я тебе тут что, шутки шучу???"
                                  "\nСказано было ввести сумму! ЦЫФРАМИ!!!"
                                  "\nНе принимаю, переписывай!")
            return in_in(message)

    if str(msg[0:6]).lower() == "сумма ":
        bot.reply_to(message, "Умеешь пользоваться клавиатурой? Похвально)")
        money = str(msg[6:]).replace(",", ".")
        try:
            money = float(money)
            calc_dict(user, money=money)
            return menu_calc(message)
        except ValueError:
            print("money-", money)
            bot.reply_to(message, "А вот головой видимо - нет! Угараешь что-ли? Я тебе тут что, шутки шучу???"
                                  "\nСказано было ввести сумму! ЦЫФРАМИ!!!"
                                  f"\nНе принимаю, переписывай! {money} - это не число!")
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


def menu_calc(message):
    # Меню калькулятора
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b_to = types.KeyboardButton("В какую валюту")
    b_from = types.KeyboardButton("Из какой валюты")
    b_money = types.KeyboardButton("Сумма")
    b_calc_to = types.KeyboardButton("Счет: сумма требуется")
    b_calc_from = types.KeyboardButton("Счет: сумма имеется")
    back = types.KeyboardButton("🔙 Возврат в меню")
    menu.add(b_to, b_from, b_money, b_calc_to, b_calc_from, back)
    bot.reply_to(message, f"""{username_(message)}, я устал работать, поторапливайся! 
Выбирай действие.""", reply_markup=menu)


# Incorrect input - Неправильный ввод числа
def in_in(message):
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("💰 1")
    button2 = types.KeyboardButton("💰 9999")
    button3 = types.KeyboardButton("😁😁😁")
    back = types.KeyboardButton("🔙 Возврат в меню калькулятора")

    menu.add(button1, button2, button3, back)
    bot.reply_to(message, f"""Повторю, для неугомонных! 
Вводи сумму в формате сообщения <Сумма 9999> или <💰 9999>!
Напишешь по другому, даже читать не буду! И да, читать прописью числа я тоже не буду!""", reply_markup=menu)


try:
    bot.polling(none_stop=True)
except requests.exceptions.ConnectionError:
    pass

# Запуск бота без помех (ну или игнорируем, x3)
