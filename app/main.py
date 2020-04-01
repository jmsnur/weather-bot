import telebot
import requests
import json
from telebot import types
from app.config import *
from app.functions import *
from app.markups import *


bot = telebot.TeleBot(TOKEN)
# bot = telebot.TeleBot(TEST_TOKEN)


# ERROR MESSAGE
def error_message(message):
    chat_id = message.chat.id
    msg = 'Incorrect message, please write correct responce.'
    m = bot.send_message(chat_id, msg)
    bot.register_next_step_handler(m, menu)
    return


# MAIN MENU
@bot.message_handler(content_types=['text'])
def menu(message):
    chat_id = message.chat.id
    msg = 'Main menu'
    m = bot.send_message(chat_id, msg, reply_markup=menu_markup)
    bot.register_next_step_handler(m, menu_proc)
    return

def menu_proc(message):
    chat_id = message.chat.id
    txt = message.text

    if txt not in menu_list:
        msg = 'Error Command'
        bot.send_message(chat_id, msg)
        menu(message)
        return 
    elif txt == menu_list[0]:
        weather_start(message)
        return 
    elif txt == menu_list[1]:
        currency(message)
        return 
    elif txt == menu_list[2]:
        msg = 'On development stage'
        bot.send_message(chat_id,msg)
        menu(message)
        return 


# WEATHER PART
@bot.message_handler(commands=['weather'])
def weather_start(message):
    chat_id = message.chat.id
    msg = 'Hi! Send me your location or type in the city'
    m = bot.send_message(chat_id, msg, reply_markup=weather_markup)
    bot.register_next_step_handler(m, weather_proc)    
    return

def weather_proc(message):
    t = message.content_type
    if t == 'location':
        proc_by_loc(message)
        return
    elif t == 'text':
        proc_by_name(message)
        return
    else:
        error_message(message)
        return

def proc_by_loc(message):
    chat_id = message.chat.id
    lon = message.location.longitude
    lat = message.location.latitude
    request = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OW_APIKEY}'
    req = requests.get(request)
    city1 = extract_values(req.json(), 'name')
    city = city1[0].upper()
    temper = extract_values(req.json(), 'temp')
    temp = float(str(temper[0]))-273.15
    tem = round(temp, 2)
    msg = f'City: {city} \nTemperature: {tem}'
    bot.send_message(chat_id, msg)
    menu(message)
    return

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
        tem = round(temp, 2)
        cty = city.upper()
        msg = f'City: {cty} \nTemperature: {tem} Cel'
        bot.send_message(chat_id, msg)
        menu(message)
        return


# CURRENCY PART
@bot.message_handler(commands=['currency'])
def currency(message):
    chat_id = message.chat.id
    req = 'https://nbu.uz/en/exchange-rates/json/'
    re = requests.get(req)
    r = re.json()

    curr_markup = types.ReplyKeyboardMarkup(True,True,None,1)
    butn_text = []
    for i in range(len(r)):
        tit = r[-i]['title']
        cod = r[-i]['code']
        txt = f'{tit} - {cod}\n'
        butn_text.append(txt)    

    for i in butn_text:
        curr_markup.add(i)

    m = bot.send_message(chat_id,'Currency cost in Soms. Choose one' , reply_markup=curr_markup)
    bot.register_next_step_handler(m,curr)
    return

def curr(message):
    chat_id = message.chat.id
    repl_text = message.text
    code = repl_text[-3:]

    req = 'https://nbu.uz/en/exchange-rates/json/'
    re = requests.get(req)
    r = re.json()

    msg = ''
    for i in range(len(r)):
        if r[i]['code'] == code:
            msg = r[i]['cb_price']+' soms'
        else:
            msg = 'Doesn\'t exist'
    m = bot.send_message(chat_id,msg)
    menu(message)


if __name__ == "__main__":
    bot.polling(none_stop=None)