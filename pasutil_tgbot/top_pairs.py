import json
import threading
from pasutil_tgbot.values import *
from pasutil_tgbot.tracking_edit_file import get_file_hash
from time import sleep

file = f"pasutil1/jsons/top_pairs.json"

def top_pairs(chat_id, bot):
    original_hash = get_file_hash(file)
    while sending_flags1.get(chat_id, False): 
        current_hash = get_file_hash(file)
        if current_hash != original_hash:
            with open(file, "r") as file_open:
                data = json.load(file_open)
 
                for pair, info in data.items():
                    if sending_flags1.get(chat_id, False):
                        msg = f"🔗Pair: <strong>{pair}</strong>\n-------------------------------\n🔔Signal: {info['signal']}\n💰Price: {info['price']}\n🔒Close: {info['close']}\n📅Date: {info['date']}\n🔬Accuracy: {info['accuracy']}"
                        bot.send_message(chat_id, msg, parse_mode="HTML")
                        sleep(10)
                    else:
                        break

                original_hash = get_file_hash(file)

def start_top_pairs(chat_id, bot):
    sending_flags1[chat_id] = True
    thread = threading.Thread(target=top_pairs, args=(chat_id, bot))
    thread.start()