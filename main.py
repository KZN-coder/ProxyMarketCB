import telebot
import api_hand
from datetime import datetime

API_TOKEN = ''
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start_answer(message):
    bot.send_message(message.chat.id, "I'm the bot to get actual proxy data from proxy.market")

@bot.message_handler(commands=['proxies'])
def send_welcome(message):
    output = "Available proxy list: \n\n"
    data = api_hand.get_data()
    for item in data["data"]:
        used = round(((int(item["used"])) / (1024 * 1024)), 2)
        total = round((int(item["total"])) / (1024 * 1024), 2)
        lasts = round(total - used, 2)
        if lasts>0:
            output += "List: " + item["name"] + '\n'
            output += "Lasts: " + str(lasts) + "Mb" + '\n'
            output += "Used: " + str(used) + "Mb" + " from " + str(total) + "Mb \n"
            output+= "Expires at: " + convert_timestamp_to_date(int(item["expires_at"])) + '\n\n'
    bot.send_message(message.chat.id, output)

def convert_timestamp_to_date(timestamp):
    date_object = datetime.fromtimestamp(timestamp)
    formatted_date = date_object.strftime('%d %B %H:%M:%S')
    return formatted_date

bot.infinity_polling()