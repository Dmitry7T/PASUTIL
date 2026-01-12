from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Get Started
callback_button = InlineKeyboardButton(text="Get started🚀", callback_data="gs")
start_keyboard = InlineKeyboardMarkup(inline_keyboard=[[callback_button]])

# Menu
markup_menu = InlineKeyboardMarkup(row_width=1)
button1 = InlineKeyboardButton(text="👤Account", callback_data="account")
button2 = InlineKeyboardButton(text="⚙️Settings", callback_data="sb")
button3 = InlineKeyboardButton(text="🔍Track everything", callback_data="trall")
button4 = InlineKeyboardButton(text="🌊10 popular pairs", callback_data="10pp")
button5 = InlineKeyboardButton(text="🎯Your own option", callback_data="yoop")
button6 = InlineKeyboardButton(text="📑User agreement", callback_data="user_agreement")
markup_menu.row(button1, button2)
markup_menu.add(button3, button4, button5, button6)

# Back
callback_button = InlineKeyboardButton(text="⬅️Back", callback_data="back")
markup_back = InlineKeyboardMarkup(inline_keyboard=[[callback_button]])

# Pay Button
callback_button = InlineKeyboardButton(text="Pay💵", callback_data="get_0.1")
markup_payment = InlineKeyboardMarkup(inline_keyboard=[[callback_button]])