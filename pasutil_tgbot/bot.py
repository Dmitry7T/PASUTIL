import telebot

from markups import *
from exchange_rate import exchange
from config import *
from telebot import types
from time_teller import time_is_good
from values import *
from subscribe_teller import check_user_subscription
from examination_index import examination

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_data[user_id] = {'index': None}

    if check_user_subscription(bot, CHANNEL, user_id):
        bot.send_message(message.chat.id, "Hi, {0.first_name}⚡️, Crypto analysis bot Select the index in which you want to receive information about the course.📈".format(message.from_user), reply_markup=markup_start)
    else:
        bot.send_message(chat_id, "You are not subscribed", reply_markup=markup_subscribe)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(content_types=['text'])
def answer(message):
    if message.chat.type == 'private':
        if message.text == 'fwsdewsf':   
            pass
            
        else:
            bot.send_message(message.chat.id, 'sorry, ya ne ponyal')	

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call: types.CallbackQuery) -> None:
    user_id = call.from_user.id
    try:
        if call.data == 'yoop':
            if check_user_subscription(bot, CHANNEL, user_id):
                if time_is_good():
                    def process_reply(message):
                        if examination(message.text):
                            bot.send_message(message.chat.id, exchange(message.text))  #ИСПРАВИТЬ 
                        else:
                            bot.send_message(message.chat.id, 'There is no such index.')  #ИСПРАВИТЬ 
                    bot.send_message(call.message.chat.id, 'Select index')
                    bot.register_next_step_handler(call.message, process_reply)
                else:
                    bot.send_message(call.message.chat.id, "Sorry, unfortunately the exchange is closed on weekends.")
                    bot.answer_callback_query(call.id)
            else:
                bot.send_message(call.message.chat.id, f"{ysina}\nTo buy it, click /subscribe")
        elif call.data == 'stngs':
            bot.send_message(call.message.chat.id, "Select the time period", reply_markup=markup_time)

        elif call.data == 'ps':
            if check_user_subscription(bot, CHANNEL, user_id):
                bot.send_message(call.message.chat.id, "The subscription is complete, you can use the bot")
            else:
                bot.send_message(call.message.chat.id, "You are not subscribed", reply_markup=markup_subscribe)


    except Exception as a:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        user_data[user_id] = {'index': None}
        bot.answer_callback_query(call.id)

    try:
        if call.data in minutes:
            if time_is_good():
                msg = exchange(user_data[user_id]['index'])
                bot.send_message(call.message.chat.id, f'{msg}')
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.answer_callback_query(call.id) 
                bot.send_message(call.message.chat.id, "Timer started") 
            else:
                bot.send_message(call.message.chat.id, "Sorry, unfortunately the exchange is closed on weekends.")
                bot.answer_callback_query(call.id)
        else:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.answer_callback_query(call.id)

    except Exception as b:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, "Please, select index")
        user_data[user_id] = {'index': None}
        bot.answer_callback_query(call.id)

bot.polling(none_stop=True)	
