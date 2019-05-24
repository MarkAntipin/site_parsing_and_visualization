'''
интерфейсом для моей визуализации
будет telegram bot
просто потому что я хочу потыкать эту технологию
'''


import telebot
from telebot import apihelper
from site_parsing import save_links_to_file, make_dataframe
from making_dataframes import save_all_to_bigquery, get_site_data, read_data_csv
from visualization import pivot_table, heat_map
from azure_connection import download_to_azure


def get_token(file_path):
    with open(file_path) as file:
        token = file.read()
    return token


apihelper.proxy = {'https': 'socks5://51.38.123.195:1080'}

telegram_token = get_token("tokens/site_parsing_bot_token.txt")

bot = telebot.TeleBot(telegram_token)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "привет":
        bot.send_message(message.from_user.id, "Здорова")
    elif message.text == "скачать_товары":
        save_links_to_file('https://hatewait.ru', 'hatewait.txt')
        bot.send_message(message.from_user.id, "ссылки сохранены в файл 'hatewait.txt'")
    elif message.text == "bigquery":
        # save_links_to_file('https://hatewait.ru', 'hatewait.txt')
        # site_data = make_dataframe('hatewait.txt')
        site_data = read_data_csv("site_data.csv")
        save_all_to_bigquery(site_data)
        bot.send_message(message.from_user.id, "теперь все на BigQuery")
    elif message.text == "azure":
        download_to_azure("site_data.csv")
        bot.send_message(message.from_user.id, "теперь все в Azure")
    elif message.text == "print":
        site_data = get_site_data()
        bot.send_message(message.from_user.id, site_data['brand'])
    elif message.text == "pivot":
        pivot_table()
        photo = open('images/pivot.png', 'rb')
        bot.send_photo(message.chat.id, photo)
        bot.send_message(message.from_user.id, "должна быть диаграмма")
    elif message.text == "heat":
        heat_map()
        photo = open('images/heat_map', 'rb')
        bot.send_photo(message.chat.id, photo)
        bot.send_message(message.from_user.id, "должна быть диаграмма")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "доступные команды: скачать_товары, "
                                               "bigquery, azure, print, pivot, heat, привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)


bot.polling(none_stop=False, interval=0, timeout=3)

