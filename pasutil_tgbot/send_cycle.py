import threading
from time import sleep
from pasutil_tgbot.values import *
from pasutil_tgbot.tracking_edit_file import get_file_hash
import json

def send_loop(chat_id, bot):
    original_hash = get_file_hash(f"pasutil1/jsons/saves.json")
    while sending_flags.get(chat_id, False):
        sleep(10)
        current_hash = get_file_hash(f"pasutil1/jsons/saves.json")
        if current_hash != original_hash:
            with open(f"pasutil1/jsons/saves.json", 'r') as f:
                data = json.load(f)
                for section_name in ("forex", "index"):
                    section = data.get(section_name, {})

                    for pair, info in section.items():
                        if sending_flags.get(chat_id, False):
                            msg = f"🔗Pair: <strong>{pair}</strong>\n-------------------------------\n🔔Signal: {info['signal']}\n💰Price: {info['price']}\n🔒Close: {info['close']}\n📅Date: {info['date']}\n🔬Accuracy: {info['accuracy']}"
                            bot.send_message(chat_id, msg, parse_mode="HTML")
                            sleep(10)
                        else:
                            break
                    original_hash = get_file_hash(f"pasutil1/jsons/saves.json")

def start_handler(chat_id, bot):
    sending_flags[chat_id] = True
    # Запуск фонового потока
    thread = threading.Thread(target=send_loop, args=(chat_id, bot))
    thread.start()

"""
def stop_handler(chat_id, bot):
    sending_flags[chat_id] = False
    bot.send_message(chat_id, "Stopping shipping.")
"""