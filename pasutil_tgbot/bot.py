import telebot
import requests
#ну импорт
from telebot import types
from pasutil_tgbot.exchange_rate import exchange
from pasutil_tgbot.examination_index import examination
from pasutil_tgbot.database_control import *
from pasutil_tgbot.markups import *
from pasutil_tgbot.config import *
from pasutil_tgbot.values import *
from pasutil_tgbot.tracking_edit_file import *
from pasutil_tgbot.send_cycle import start_handler
from pasutil_tgbot.top_pairs import start_top_pairs, top_pairs
from time import sleep

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    add_user(user_id)
    bot.send_message(message.chat.id, "Hi, {0.first_name}⚡️, We - crypto analysis bot Select the index in which you want to receive information about the course.📈".format(message.from_user), reply_markup=markup_start)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, help_text)

@bot.callback_query_handler(func=lambda call: call.data == "get_0.1")
def get_invoice(call):
    user_id = call.from_user.id
    def L():
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.answer_callback_query(call.id)
        chat_id = call.message.chat.id 
        pay_link, invoice_id = get_pay_link(price)
        if pay_link and invoice_id:
            invoices[chat_id] = invoice_id
            markup_pay = types.InlineKeyboardMarkup()
            markup_pay.add(types.InlineKeyboardButton(text=f'💸Pay {price}$', url=pay_link))
            markup_pay.add(types.InlineKeyboardButton(text='🔍Check payment', callback_data=f'check_payment_{invoice_id}'))
            bot.send_message(chat_id, f"⚡️Payment amount: ${price} \n<strong>Please do not submit anonymously.</strong>", reply_markup=markup_pay, parse_mode="HTML")
        else:
            bot.send_message(chat_id, "Failed")
    if check_subscription_active(user_id):
        L()
    else:
        add_user(user_id)
        L()

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
                    activate_subscription(user_id)
                    bot.send_message(chat_id, "Payment completed!💸", reply_markup=markup_back)
                    del invoices[chat_id]
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
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

def start_message(chat_id, message_id):
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="⚙️Please, select mode", reply_markup=markup_menu)
    #bot.send_message(chat_id, "⚙️Please, select mode", reply_markup=markup_menu)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call: types.CallbackQuery) -> None:
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    message_id=call.message.message_id
    try:
        if check_subscription_active(user_id):
            if call.data:
                bot.answer_callback_query(call.id)

            if call.data == 'yoop':
                bot.delete_message(chat_id, message_id)
                def otvet(message):
                    if examination(message.text):
                        bot.send_message(message.chat.id, exchange(message.text), reply_markup=markup_back)  #ИСПРАВИТЬ
                    else:
                        bot.send_message(message.chat.id, "There is no such index.")  #ИСПРАВИТЬ / или не надо
                        
                bot.send_message(chat_id, 'Select index', reply_markup=markup_back)
                bot.register_next_step_handler(call.message, otvet)

            elif call.data == 'user_agreement':
                with open('pasutil_tgbot/sogl.txt', 'r', encoding='utf-8') as f:
                    content = f.read()
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=content, reply_markup=markup_back)

            elif call.data == 'trall':
                if sending_flags1.get(chat_id, False):
                    sending_flags1[chat_id] = False
                    bot.send_message(chat_id, "Tracking 10pp is finished")
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Start all shipping...", reply_markup=markup_back)
                    sleep(2)
                    start_handler(chat_id, bot)
                else:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Start all shipping...", reply_markup=markup_back)
                    sleep(2)
                    start_handler(chat_id, bot)

            elif call.data == '10pp':
                if sending_flags.get(chat_id, False):
                    sending_flags[chat_id] = False
                    bot.send_message(chat_id, "Tracking everything is finished")
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Start 10pp shipping...", reply_markup=markup_back)
                    sleep(2)
                    start_top_pairs(chat_id, bot)
                else:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Start 10pp shipping...", reply_markup=markup_back)
                    sleep(2)
                    start_top_pairs(chat_id, bot)

            elif call.data == 'gs':
                start_message(chat_id,message_id)

            elif call.data == 'sp':
                if sending_flags1.get(chat_id, False) or sending_flags.get(chat_id, False):
                    sending_flags[chat_id] = False
                    sending_flags1[chat_id] = False
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="The process is stopped", reply_markup=markup_back)
                else:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="The process is not active", reply_markup=markup_back)
                    #bot.send_message(chat_id, "The process is not active")

            elif call.data == 'stngs':
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Here you can set the operating mode", reply_markup=markup_settings)

            elif call.data == 'back':
                #bot.delete_message(chat_id, message_id)
                start_message(chat_id,message_id)

            elif call.data == "account":
                date = get_date_by_username_id(user_id)
                msg = f"<strong>Account information:</strong>\n\n👤<strong>ID</strong>: {user_id}\n💰<strong>Rate</strong>: {price}$\n🔑<strong>End date:</strong> {date}"
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=msg, reply_markup=markup_back, parse_mode="HTML")
                
        else:
            bot.delete_message(chat_id, message_id)
            bot.send_message(call.message.chat.id, "🤓To use our bot, you need a subscription. Please pay for it to continue.", reply_markup=markup_payment)

    except Exception as a:
        bot.delete_message(chat_id, message_id)
        bot.answer_callback_query(call.id)
        bot.send_message(teterev_admin, a)  #отправка тетереву SOS

bot.infinity_polling()
