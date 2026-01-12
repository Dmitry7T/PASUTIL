import asyncio
import json
from values import *
from tracking_edit_file import get_file_hash

async def send_loop(chat_id: int, bot):
    original_hash = get_file_hash("saves.json")

    while sending_flags.get(chat_id, False):
        await asyncio.sleep(10)

        current_hash = get_file_hash("saves.json")
        if current_hash != original_hash:
            with open("saves.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            for section_name in ("forex", "index"):
                section = data.get(section_name, {})

                for pair, info in section.items():
                    if not sending_flags.get(chat_id, False):
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
            
def start_handler(chat_id: int, bot):
    sending_flags[chat_id] = True
    asyncio.create_task(send_loop(chat_id, bot))