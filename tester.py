import telebot
import requests
from bs4 import BeautifulSoup

# TOKEN = "6074047522:AAEVGXN4uk7wkgt8PdfPZEjnNT89b-v5tfw"

# bot = telebot.TeleBot(TOKEN)

# def test():
#     base_ = "http://rate.am/informer/rate/script/default.aspx?uid=UI-52497593&width=215&height=132&cb=0&bgcolor=FFFFFF&lang=ru"
#     html = requests.get(base).content
#     soup = BeautifulSoup(html, 'lxml')

rub_s: float = None
rub_b: float = None
usd_s: float = None
usd_b: float = None
eur_s: float = None
eur_b: float = None

'''def test():
    base_ = "http://rate.am/informer/rate/script/default.aspx?uid=UI-52497593&width=215&height=132&cb=0&bgcolor=FFFFFF&lang=ru"
    html = requests.get(base).content
    soup = BeautifulSoup(html, 'lxml')

    #<iframe id="rate-widget" scrolling="no" frameborder="no" src="http://rate.am/informer/rate/iframe/Default.aspx?uid=UI-52497593&width=215&height=132&cb=0&bgcolor=FFFFFF&lang=ru" width="215px" height="135px" ></iframe>
'''


def checker():
    base = 'https://rate.am/ru/armenian-dram-exchange-rates/banks/cash'
    html = requests.get(base).content
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('table', id='rb')
    tr = table.find_all('tr', class_='btm')
    td = tr[1].find_all('td', class_='fhd')
    u_b, u_s, e_b, e_s, r_b, r_s = td[1], td[2], td[3], td[4], td[5], td[6]
    return u_b.getText(), u_s.getText(), e_b.getText(), e_s.getText(), r_b.getText(), r_s.getText()


def update():
    global usd_b, usd_s, eur_b, eur_s, rub_b, rub_s
    usd_b, usd_s, eur_b, eur_s, rub_b, rub_s = checker()
    return


update()
print(usd_b, usd_s, eur_b, eur_s, rub_b, rub_s)

# bot.polling(none_stop=True)
