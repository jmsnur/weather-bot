import telebot
import requests
import json
from telebot import types 
from app.config import *
from app.functions import *


bot = telebot.TeleBot(TOKEN)


start_markup = types.ReplyKeyboardMarkup(True,True)
b1 = types.KeyboardButton('Send location', request_location=True)
start_markup.add(b1)


@bot.message_handler(commands=['start', 'go'])
def start(message):
    chat_id = message.chat.id
    msg = 'Hi! Send me your location or type in the city'
    bot.send_message(chat_id, msg, reply_markup=start_markup)
    return


@bot.message_handler(content_types=['location'] )
def proc_by_loc(message):
    chat_id = message.chat.id
    lon = message.location.longitude
    lat = message.location.latitude
    request = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OW_APIKEY}' 
    req = requests.get(request)
    city1 = extract_values(req.json(),'name')
    city = city1[0].upper()
    temper = extract_values(req.json(), 'temp')
    temp = float(str(temper[0]))-273.15
    msg = f'City: {city} \nTemperature: {temp}'
    bot.send_message(chat_id, msg)
    return



@bot.message_handler(content_types=['text'])
def proc_by_name(message):
    chat_id = message.chat.id
    city = (message.text).lower()
    request = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OW_APIKEY}'
    r = requests.get(request)
    if r.status_code != 200:
        msg = 'Incorrect city, please write valid one...'
        bot.send_message(chat_id, msg)
        return
    else:
        temper = extract_values(r.json(), 'temp')
        temp = float(str(temper[0])) - 273.15
        cty = city.upper()
        msg = f'City: {cty} \nTemperature: {temp} Cel'
        bot.send_message(chat_id, msg)
        return 
    





if __name__ == "__main__":
    bot.polling(none_stop=None)

