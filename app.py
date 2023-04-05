import telebot


TOKEN = "6016539624:AAFVQDjxs1Ig1uOgQT7Skrb4VT14rHFgkgc"


bot = telebot.TeleBot(TOKEN)


def username_(message):
    username = message.from_user.username
    username = message.from_user.first_name if not username else username
    return username



bot.polling(none_stop=True)

