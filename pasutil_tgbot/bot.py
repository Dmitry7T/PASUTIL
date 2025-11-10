import telebot

from markups import *
from exchange_rate import exchange
from config import *
from telebot import types
from time_teller import time_is_good
from values import *
from subscribe_teller import check_user_subscription
from examination_index import examination
from msg_minutes import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_data[user_id] = {"Time": None, 
                          "index" : None
                          }

    if check_user_subscription(bot, CHANNEL, user_id):
        bot.send_message(message.chat.id, "Hi, {0.first_name}⚡️, We - crypto analysis bot Select the index in which you want to receive information about the course.📈".format(message.from_user), reply_markup=markup_start)
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
        if check_user_subscription(bot, CHANNEL, user_id):
            if time_is_good():
                if call.data == 'yoop':
                    def otvet(message):
                        if examination(message.text):
                            bot.send_message(message.chat.id, exchange(message.text))  #ИСПРАВИТЬ
                        else:
                            bot.send_message(message.chat.id, 'There is no such index.')  #ИСПРАВИТЬ / или не надо
                    bot.send_message(call.message.chat.id, 'Select index')
                    bot.register_next_step_handler(call.message, otvet)

                elif call.data == 'trall':
                    bot.send_message(call.message.chat.id, "Select the time period", reply_markup=markup_time)

                elif call.data == 'gs':
                    bot.send_message(call.message.chat.id, "Please, select mode", reply_markup=markup_menu)

                elif call.data == 'stngs':
                    if check_user_subscription(bot, CHANNEL, user_id):
                        bot.send_message(call.message.chat.id, "Subscription completed.\nRate: ...", reply_markup=markup_back)
                    else:
                        bot.send_message(call.message.chat.id, "You haven't subscribed to the channel, please subscribe.", reply_markup=markup_subscribe)
                
                elif call.data == 'back':
                    bot.send_message(call.message.chat.id, "Please, select mode", reply_markup=markup_menu)

            else:
                bot.send_message(call.message.chat.id, "Sorry, unfortunately the exchange is closed on weekends.")
                bot.answer_callback_query(call.id)

        else:
            bot.send_message(call.message.chat.id, "You are not subscribed", reply_markup=markup_subscribe)
            bot.answer_callback_query(call.id)


    except Exception as a:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        user_data[user_id] = {'index': None}
        bot.answer_callback_query(call.id)

    try:
        if call.data in minutes:
            if time_is_good():
                bot.answer_callback_query(call.id)
                user_data[user_id]["Time"] = call.data    #ЗАПИСЬ В ОПЕРАТИВКЕ, ЖЕЛАТЕЛЬНО ПОМЕНЯТЬ НА БАЗУ ДАННЫХ 
                print(user_data)
                #min60("AUDUSD", call.message.chat.id)
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
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

if __name__ == '__main__':
    bot.polling(none_stop=True)	
