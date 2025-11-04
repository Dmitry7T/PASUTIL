import telebot

from exchange_rate import *
from config import *
from telebot import types
from time_teller import time_is_good

bot = telebot.TeleBot(TOKEN)

markup = types.InlineKeyboardMarkup()
button1 = types.InlineKeyboardButton(text='XAUUSD💲', callback_data='XAUUSD')
markup.add(button1)

markup_time = types.InlineKeyboardMarkup()
button1 = types.InlineKeyboardButton(text='5️⃣ min', callback_data='5min')
button2 = types.InlineKeyboardButton(text='1️⃣0️⃣ min', callback_data='10min')
button3 = types.InlineKeyboardButton(text='1️⃣5️⃣ min', callback_data='15min')
button4 = types.InlineKeyboardButton(text='3️⃣0️⃣ min', callback_data='30min')
markup_time.add(button1,button2,button3,button4)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_data[user_id] = {'index': None}
    bot.send_message(message.chat.id, "Hi, {0.first_name}⚡️, Crypto analysis bot Select the index in which you want to receive information about the course.📈".format(message.from_user), reply_markup=markup)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Help")

@bot.message_handler(content_types=['text'])
def answer(message):
    if message.chat.type == 'private':
        if message.text == 'fwsdewsf':   
            pass
            
        else:
            bot.send_message(message.chat.id, 'Извините, я не понял☹️')	

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call: types.CallbackQuery) -> None:
    user_id = call.from_user.id

    if call.data == 'XAUUSD':
        if time_is_good():
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            user_data[user_id]['index'] = 'XAUUSD'  
            bot.send_message(call.message.chat.id, 'Please, select a time period', reply_markup=markup_time)
            bot.answer_callback_query(call.id)
        else:
            bot.send_message(call.message.chat.id, "Sorry, unfortunately the exchange is closed on weekends.")
            bot.answer_callback_query(call.id)

    elif call.data == '5min':
        if time_is_good():
            bot.send_message(call.message.chat.id, "Timer started") 
            msg = exchange(user_data[user_id]['index'])
            bot.send_message(call.message.chat.id, f'{msg}')
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            #print(user_data[user_id]['index'])
            bot.answer_callback_query(call.id) 
        else:
            bot.send_message(call.message.chat.id, "Sorry, unfortunately the exchange is closed on weekends.")
            bot.answer_callback_query(call.id)
    else:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.answer_callback_query(call.id)

bot.polling(none_stop=True)	
