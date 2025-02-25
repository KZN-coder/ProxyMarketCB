import threading
import time

import telebot
import api_hand
import config

API_TOKEN = f'{config.bot_TOKEN}'
bot = telebot.TeleBot(API_TOKEN)

actual_speeds = ""

@bot.message_handler(commands=['start'])
def start_answer(message):
    bot.send_message(message.chat.id, "I'm the bot to get actual proxy data from proxy.market")


@bot.message_handler(commands=['proxies'])
def send_list(message):
    output = api_hand.get_list()
    bot.send_message(message.chat.id, output, parse_mode='Markdown')


@bot.message_handler(commands=['image'])
def send_image(message):
    api_hand.get_image()
    with open('./data/proxy_traffic.png', 'rb') as photo:
        bot.send_photo(message.chat.id, photo=photo)


@bot.message_handler(commands=['getlist'])
def handle_command(message):
    text = message.text
    parts = text.split(' ', 1)
    command, params = parts
    bot.send_message(message.chat.id, api_hand.formating_proxy_lists(params))

@bot.message_handler(commands=['getspeed'])
def handle_command(message):
    bot.send_message(message.chat.id, actual_speeds, parse_mode='Markdown')

def checking_speed():
    global actual_speeds
    actual_speeds=api_hand.get_speed(30)
    time.sleep(5)

threading.Thread(target=checking_speed()).start()

bot.infinity_polling()