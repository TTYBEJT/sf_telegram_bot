# Асинхронный запуск функции проверки курса и таймер на 3 минуты
# async def updater():
#     while True:
#         update()  # Функция проверки
#         await asyncio.sleep(180)  # 180 секунд = 3 минуты


# Стартер циклического двигателя проверятора
# async def main():
#     # Запуск функции проверки
#     await updater()

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


# запуск бота
'''if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling())
    loop.run_forever()
'''
# thread = threading.Thread(target=asyncio.run(main()))
# thread.start()
# loop = asyncio.get_event_loop()
# loop.create_task(checker())

# async def bot_polling():
#     while True:
#         try:
#             bot.polling(none_stop=True, interval=0, timeout=20)
#         except Exception as e:
#             print(e)
#             await asyncio.sleep(15)


# async def main():
#     asyncio.create_task(bot_polling())

# if __name__ == '__main__':
#     asyncio.run(main())
