import sqlite3
import telebot

from datetime import datetime
from time import sleep
from database_control import File_db
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

def check_subscriptions():
    conn = sqlite3.connect(File_db)
    cursor = conn.cursor()

    while True:
        now = datetime.now()
        cursor.execute("SELECT username_id, date FROM users WHERE date IS NOT NULL")
        rows = cursor.fetchall()

        for username_id, date_str in rows:
            subscription_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

            if now > subscription_date:
                print("ПРОСРОЧЕНО")
                cursor.execute("""
                    UPDATE users
                    SET Subscription = ?, date = ?
                    WHERE username_id = ?
                """, (0, None, username_id))
                bot.send_message(username_id, "Your subscription has expired.")

            else:
                print("НЕ ПРОСРОЧЕНО")

        conn.commit()
        sleep(60)

if __name__ == "__main__":
    check_subscriptions()
