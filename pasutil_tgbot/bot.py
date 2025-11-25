import telebot
import requests
import json

from telebot import types
from exchange_rate import exchange
from time_teller import time_is_good
from examination_index import examination
from database_control import check_subscription_active, add_user, activate_subscription
from markups import *
from config import *
from values import *
from time import sleep
from tracking_edit_file import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    add_user(user_id)
    user_data[user_id] = {"Time": None, 
                          "index" : None
                          }

    bot.send_message(message.chat.id, "Hi, {0.first_name}⚡️, We - crypto analysis bot Select the index in which you want to receive information about the course.📈".format(message.from_user), reply_markup=markup_start)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(content_types=['text'])
def answer(message):
    if message.chat.type == 'private':
        if message.text == 'fwsdewsf':   
            pass
            
        else:
            bot.send_message(message.chat.id, "Sorry, I didn't understand.")	


@bot.callback_query_handler(func=lambda call: call.data == "get_0.1")
def get_invoice(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    bot.answer_callback_query(call.id)
    chat_id = call.message.chat.id 
    pay_link, invoice_id = get_pay_link('0.05')
    if pay_link and invoice_id:
        invoices[chat_id] = invoice_id
        markup_pay = types.InlineKeyboardMarkup()
        markup_pay.add(types.InlineKeyboardButton(text='💸Pay 0.05$', url=pay_link))
        markup_pay.add(types.InlineKeyboardButton(text='🔍Check payment', callback_data=f'check_payment_{invoice_id}'))
        bot.send_message(chat_id, "⚡️Payment amount: $0.05", reply_markup=markup_pay)
    else:
        bot.send_message(chat_id, "Failed")

def check_payment_status(invoice_id):
    headers = {"Crypto-Pay-API-Token": API_TOKEN}
    timeout = 10
    try:
        resp = requests.get(
            "https://pay.crypt.bot/api/getInvoices",
            headers=headers,
            params={"invoice_id": invoice_id},
            timeout=timeout
        )
        if resp.ok:
            try:
                return resp.json()
            except ValueError:
                return {"ok": False, "error": "Invalid JSON in GET response"}

    except requests.RequestException as e:
        pass

    try:
        resp = requests.post(
            "https://pay.crypt.bot/api/getInvoices",
            headers=headers,
            json={"invoice_id": invoice_id},
            timeout=timeout
        )
        if resp.ok:
            try:
                return resp.json()
            except ValueError:
                return {"ok": False, "error": "Invalid JSON in POST response"}
        else:
            return {"ok": False, "error": f"HTTP {resp.status_code} - {resp.text}"}
    except requests.RequestException as e:
        return {"ok": False, "error": str(e)}

@bot.callback_query_handler(func=lambda call: call.data.startswith('check_payment_'))
def check_payment(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    invoice_id = call.data.split("check_payment_")[1]
    payment_status = check_payment_status(invoice_id)
    if payment_status and payment_status.get('ok'): 
        if 'items' in payment_status['result']:
            invoice = next((inv for inv in payment_status['result']['items'] if str(inv['invoice_id']) == invoice_id), None)
            if invoice:
                status = invoice['status']
                if status == 'paid':
                    bot.send_message(chat_id, "Payment completed!💸")
                    del invoices[chat_id]
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    activate_subscription(user_id)
                    bot.answer_callback_query(call.id)
                else:
                    bot.answer_callback_query(call.id, "Payment not found", show_alert=True)
            else:
                bot.answer_callback_query(call.id, "Check not found", show_alert=True)
        else:
            bot.answer_callback_query(call.id, "Error receiving payment status", show_alert=True)
    else:
        bot.answer_callback_query(call.id, "Error receiving payment status", show_alert=True)

def get_pay_link(amount):
    headerss = {"Crypto-Pay-API-Token": API_TOKEN}
    data = {"asset": "USDT", "amount": amount}
    response = requests.post('https://pay.crypt.bot/api/createInvoice', headers=headerss, json=data)
    if response.ok:
        response_data = response.json()
        return response_data['result']['pay_url'], response_data['result']['invoice_id']
    return None, None

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call: types.CallbackQuery) -> None:
    user_id = call.from_user.id
    try:
        if check_subscription_active(user_id):
            if time_is_good():
                if call.data == 'yoop':
                    def otvet(message):
                        if examination(message.text):
                            bot.send_message(message.chat.id, exchange(message.text))  #ИСПРАВИТЬ
                        else:
                            bot.send_message(message.chat.id, "There is no such index.")  #ИСПРАВИТЬ / или не надо
                    bot.send_message(call.message.chat.id, 'Select index')
                    bot.register_next_step_handler(call.message, otvet)

                elif call.data == 'trall':
                    bot.send_message(call.message.chat.id, "Select the time period", reply_markup=markup_time)

                elif call.data == 'gs':
                    bot.send_message(call.message.chat.id, "Please, select mode", reply_markup=markup_menu)

                elif call.data == 'stngs':
                    bot.send_message(call.message.chat.id, "Subscription completed.\nRate: ...", reply_markup=markup_back)
                
                elif call.data == 'back':
                    bot.send_message(call.message.chat.id, "Please, select mode", reply_markup=markup_menu)

            else:
                bot.send_message(call.message.chat.id, "🔒Sorry, unfortunately the exchange is closed on weekends.📅")
                bot.answer_callback_query(call.id)

        else:
            bot.send_message(call.message.chat.id, "🤓To use our bot, you need a subscription. Please pay for it to continue.", reply_markup=markup_payment)
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
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(call.message.chat.id, "You are select time period.")
                sleep(3)
                bot.send_message(call.message.chat.id, "Wait...")
                original_hash = get_file_hash(f"pasutil1/jsons/{call.data}.json")
                while True:
                    sleep(10)
                    current_hash = get_file_hash(f"pasutil1/jsons/{call.data}.json")
                    if current_hash != original_hash:
                        with open(f"pasutil1/jsons/{call.data}.json", 'r') as f:
                            data = json.load(f)['forex']

                        # 2. Итерация и вывод данных
                        for pair, info in data.items():
                            msg = f"🔗Pair: <strong>{pair}</strong>\n-------------------------------\n🔔Signal: {info['signal']}\n💰Price: {info['price']}\n🔒Close: {info['close']}\n📅Date: {info['date']}\n🔬Accuracy: {info['accuracy']}"
                            sleep(1)
                            bot.send_message(call.message.chat.id, msg, parse_mode="HTML")
                        original_hash = get_file_hash(f"pasutil1/jsons/{call.data}.json")
                #min60("AUDUSD", call.message.chat.id)
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
