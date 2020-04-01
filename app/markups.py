from telebot import types

# MENU 
menu_markup = types.ReplyKeyboardMarkup(True,True,None,1)
menu_list = ['Weather by city','Currency','Settings']
for i in menu_list:
    menu_markup.add(i)


# WEATHER MARKUP
weather_markup = types.ReplyKeyboardMarkup(True, True)
b1 = types.KeyboardButton('Send location', request_location=True)
weather_markup.add(b1)

