from unittest.mock import call
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from values import *
from config import *
from markups import *
from database_control import *
from send_cycle import start_handler
from top_pairs import start_top_pairs, top_pairs
import requests
from exchange_rate import exchange
from examination_index import examination

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class Form(StatesGroup):
    waiting_for_message = State()

@dp.message_handler(state=Form.waiting_for_message)
async def process_message(message: types.Message, state: FSMContext):
    if examination(message.text):
        await message.answer(exchange(message.text))
    else:
        await message.answer("There is no such index.")
    await state.finish()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    add_user(user_id)
    await message.answer(f"Hi, {message.from_user.full_name}⚡️, We - crypto analysis bot Select the index in which you want to receive information about the course.📈", reply_markup=start_keyboard)

@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.answer(help_text, parse_mode="HTML")

@dp.callback_query_handler(lambda c: c.data == "free")
async def get_invoice(callback: CallbackQuery):
    user_id = callback.from_user.id
    if check_try_active(user_id):
        activate_try(user_id)
        await callback.message.edit_text("A seven-day trial period has been activated!", reply_markup=markup_welcome)
    else:
        await callback.message.edit_text("The trial period is already activated.")

@dp.callback_query_handler(lambda c: c.data == "get_0.1")
async def get_invoice(callback: CallbackQuery):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    async def send_invoice():
        await callback.message.delete()
        await callback.answer()

        pay_link, invoice_id = get_pay_link(price)

        if pay_link and invoice_id:
            invoices[chat_id] = invoice_id

            markup_pay = InlineKeyboardMarkup()
            markup_pay.add(InlineKeyboardButton(text=f'💸Pay {price}$',url=pay_link))
            markup_pay.add(InlineKeyboardButton(text='🔍Check payment',callback_data=f'check_payment_{invoice_id}'))

            await callback.message.answer(f"⚡️Payment amount: ${price}\n"f"<strong>Please do not submit anonymously.</strong>",reply_markup=markup_pay,parse_mode="HTML")
        else:
            await callback.message.answer("Failed")

    if check_subscription_active(user_id):
        await send_invoice()
    else:
        add_user(user_id)
        await send_invoice()

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
            return resp.json()
    except requests.RequestException:
        pass

    try:
        resp = requests.post(
            "https://pay.crypt.bot/api/getInvoices",
            headers=headers,
            json={"invoice_id": invoice_id},
            timeout=timeout
        )
        if resp.ok:
            return resp.json()
        return {"ok": False}
    except requests.RequestException as e:
        return {"ok": False, "error": str(e)}

@dp.callback_query_handler(lambda c: c.data.startswith('check_payment_'))
async def check_payment(callback: CallbackQuery):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    invoice_id = callback.data.replace('check_payment_', '')

    payment_status = check_payment_status(invoice_id)

    if payment_status and payment_status.get('ok'):
        items = payment_status.get('result', {}).get('items')
        if items:
            invoice = next(
                (inv for inv in items if str(inv.get('invoice_id')) == invoice_id),
                None
            )

            if invoice:
                if invoice.get('status') == 'paid':
                    activate_subscription(user_id)

                    await callback.message.answer(
                        "Payment completed!💸",
                        reply_markup=markup_welcome
                    )

                    invoices.pop(chat_id, None)
                    await callback.message.delete()
                    await callback.answer()
                else:
                    await callback.answer(
                        "Payment not found",
                        show_alert=True
                    )
            else:
                await callback.answer(
                    "Check not found",
                    show_alert=True
                )
        else:
            await callback.answer(
                "Error receiving payment status",
                show_alert=True
            )
    else:
        await callback.answer(
            "Error receiving payment status",
            show_alert=True
        )

def get_pay_link(amount):
    headers = {"Crypto-Pay-API-Token": API_TOKEN}
    data = {
        "asset": "USDT",
        "amount": amount
    }
    response = requests.post(
        "https://pay.crypt.bot/api/createInvoice",
        headers=headers,
        json=data
    )
    if response.ok:
        result = response.json().get('result', {})
        return result.get('pay_url'), result.get('invoice_id')

    return None, None

@dp.callback_query_handler(state="*")
async def process_any_button_click(callback_query: types.CallbackQuery, state: FSMContext):
    callback_data = callback_query.data
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    chat_id = callback_query.message.chat.id
    try:
        if check_subscription_active(user_id):
            if await state.get_state() == Form.waiting_for_message.state:
                await state.finish()
            if callback_data:
                await callback_query.answer()
            if callback_query.data == "yoop":
                await Form.waiting_for_message.set()
                await callback_query.message.answer("Please, select index")
            if callback_data == "gs":
                await callback_query.message.edit_text("📋Please, select mode", reply_markup=markup_menu)
            if callback_data == "back":
                await callback_query.message.edit_text("📋Please, select mode", reply_markup=markup_menu)
            if callback_data == "account":
                date = get_date_by_username_id(user_id)
                msg = f"<strong>Account information:</strong>\n\n👤<strong>ID</strong>: {user_id}\n💰<strong>Rate</strong>: {price}$\n🔑<strong>End date:</strong> {date}"
                await callback_query.message.edit_text(msg, reply_markup=markup_back, parse_mode="HTML")
            if callback_data == "user_agreement":
                with open('sogl.txt', 'r', encoding='utf-8') as f:
                    content = f.read()
                await callback_query.message.edit_text(content, reply_markup=markup_back, parse_mode="HTML")
            if callback_data == "sb":
                markup_settings = InlineKeyboardMarkup()
                button1 = InlineKeyboardButton(text='⛔️Stop processing', callback_data='sp')
                button2 = InlineKeyboardButton(text='🛡️Change mod', callback_data='change_mod')
                button3 = InlineKeyboardButton(text='⬅️Back', callback_data='back')

                if sending_flags1.get(chat_id, False) or sending_flags.get(chat_id, False):
                    markup_settings.row(button1)
                    markup_settings.row(button2)
                    markup_settings.row(button3)

                else:
                    markup_settings.row(button2)
                    markup_settings.row(button3)
                await callback_query.message.edit_text("🛠️Here you can set the operating mode", reply_markup=markup_settings)
            if callback_data == 'sp':
                if sending_flags1.get(chat_id, False) or sending_flags.get(chat_id, False):
                    sending_flags[chat_id] = False
                    sending_flags1[chat_id] = False
                    await callback_query.message.edit_text("📋Please, select mode", reply_markup=markup_menu)
                    await callback_query.message.answer("The process is stopped")
                else:
                    await callback_query.message.edit_text("The process is not active", reply_markup=markup_back)
            if callback_data == 'trall':
                if sending_flags1.get(chat_id, False):
                    sending_flags1[chat_id] = False
                    await callback_query.message.answer("🏁Tracking 10pp is finished")
                    await callback_query.message.answer("▶️Start all shipping...")
                    start_handler(chat_id, bot)
                else:
                    await callback_query.message.answer("▶️Start all shipping...")
                    start_handler(chat_id, bot)
            if callback_data == '10pp':
                if sending_flags.get(chat_id, False):
                    sending_flags[chat_id] = False
                    await callback_query.message.answer("🏁Tracking everything is finished")
                    await callback_query.message.answer("▶️Start 10pp shipping...")
                    start_top_pairs(chat_id, bot)
                else:
                    await callback_query.message.answer("▶️Start 10pp shipping...")
                    start_top_pairs(chat_id, bot)

        else:
            await callback_query.message.delete()
            markup_payment = InlineKeyboardMarkup(row_width=1)
            if check_try_active(user_id):
                button1 = InlineKeyboardButton(text="Pay💵", callback_data="get_0.1")
                button2 = InlineKeyboardButton(text="FREE", callback_data="free")
                markup_payment.add(button1, button2)
            else:
                button1 = InlineKeyboardButton(text="Pay💵", callback_data="get_0.1")
                markup_payment.add(button1)
            await callback_query.message.answer("🤓To use our bot, you need a subscription. Please pay for it to continue.", reply_markup=markup_payment)
    except Exception as a:
        await callback_query.message.delete()
        await bot.send_message(chat_id=teterev_admin, text=a)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)