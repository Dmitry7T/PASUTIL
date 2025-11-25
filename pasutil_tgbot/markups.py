from telebot import types

markup_menu = types.InlineKeyboardMarkup()
button1 = types.InlineKeyboardButton(text='Settings⚙️', callback_data='stngs')
button2 = types.InlineKeyboardButton(text='10 popular pairs🔝', callback_data='10pp')
button3 = types.InlineKeyboardButton(text='Track everything🔍', callback_data='trall')
button4 = types.InlineKeyboardButton(text='Your own option🎯', callback_data='yoop')
markup_menu.add(button1,button2,button3,button4)

markup_stop = types.InlineKeyboardMarkup()
button1 = types.InlineKeyboardButton(text='Stop', callback_data='stop')
markup_stop.add(button1) 

markup_start = types.InlineKeyboardMarkup()
button1 = types.InlineKeyboardButton(text='Get started🚀', callback_data='gs')
markup_start.add(button1)

markup_time = types.InlineKeyboardMarkup()
button1 = types.InlineKeyboardButton(text='1️⃣5️⃣ min', callback_data='saves15')
button2 = types.InlineKeyboardButton(text='3️⃣0️⃣ min', callback_data='saves30')
button3 = types.InlineKeyboardButton(text='6️⃣0️⃣ min', callback_data='saves60')

markup_time.add(button1,button2,button3)

markup_subscribe = types.InlineKeyboardMarkup()
button1 = types.InlineKeyboardButton(text='Pay for a subscription💳', url="https://t.me/pasutilchannel")
button2 = types.InlineKeyboardButton(text='Check subscription✅', callback_data='ps')
markup_subscribe.add(button1, button2)

markup_pp = types.InlineKeyboardMarkup()
button1 = types.InlineKeyboardButton(text='XAUUSD💲', callback_data='XAUUSD')
markup_pp.add(button1)

markup_back = types.InlineKeyboardMarkup()
button1 = types.InlineKeyboardButton(text='Back', callback_data='back')
markup_back.add(button1)

markup_payment = types.InlineKeyboardMarkup()
button1 = types.InlineKeyboardButton(text='Pay💵', callback_data='get_0.1')
markup_payment.add(button1)