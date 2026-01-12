import asyncio
import json
from values import *
from tracking_edit_file import get_file_hash

FILE_PATH = "top_pairs.json"

async def top_pairs(chat_id: int, bot):
    original_hash = get_file_hash(FILE_PATH)

    while sending_flags1.get(chat_id, False):
        await asyncio.sleep(2)  # небольшая пауза, чтобы не грузить CPU

        current_hash = get_file_hash(FILE_PATH)
        if current_hash != original_hash:
            with open(FILE_PATH, "r", encoding="utf-8") as file_open:
                data = json.load(file_open)

            for pair, info in data.items():
                if not sending_flags1.get(chat_id, False):
                    return

                msg = (
                    f"🔗Pair: <strong>{pair}</strong>\n"
                    f"-------------------------------\n"
                    f"🔔Signal: {info['signal']}\n"
                    f"💰Price: {info['price']}\n"
                    f"🔒Close: {info['close']}\n"
                    f"📅Date: {info['date']}\n"
                    f"🔬Accuracy: {info['accuracy']}"
                )

                await bot.send_message(
                    chat_id=chat_id,
                    text=msg,
                    parse_mode="HTML"
                )

                await asyncio.sleep(10)

            original_hash = current_hash
def start_top_pairs(chat_id: int, bot):
    sending_flags1[chat_id] = True
    asyncio.create_task(top_pairs(chat_id, bot))