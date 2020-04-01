import requests 
from telebot import types
import telebot 
from app.config import TEST_TOKEN
import logging


test = telebot.TeleBot(TEST_TOKEN)



@test.message_handler(content_types=['text', 'location'])
def test_str(message):
    return tst(message)

def tst(message):
    return pt(message)


def pt(message):
    print(message.content_type)












@test.message_handler(commands=['test'])
def test_cur(message):
    chat_id = message.chat.id
    req = 'https://nbu.uz/en/exchange-rates/json/'
    re = requests.get(req)
    r = re.json()

    test_markup = types.ReplyKeyboardMarkup(True,True,None,1)
    butn_text = []
    for i in range(len(r)):
        tit = r[-i]['title']
        cod = r[-i]['code']
        txt = f'{tit} - {cod}\n'
        butn_text.append(txt)    

    for i in butn_text:
        test_markup.add(i)

    m = test.send_message(chat_id,'Currency cost in Soms. Choose one' , reply_markup=test_markup)
    test.register_next_step_handler(m,curr)
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
    test.send_message(chat_id,msg)
    return




    # if r[-i]['code'] == 'USD':
    #     print('True')
    # else:
    #     print('False')



test.polling(none_stop=None)
