import sqlite3
from datetime import datetime
from dateutil.relativedelta import relativedelta

File_db = 'telegram_users.db'

def create_table():
    conn = sqlite3.connect(File_db)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username_id TEXT UNIQUE NOT NULL,
            Subscription BOOLEAN DEFAULT 0,
            date TEXT UNIQUE,
            try BOOLEAN DEFAULT 1
        )
    """)
    conn.commit()
    conn.close()


def add_user(username_id):
    conn = sqlite3.connect(File_db)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username_id) VALUES (?)", (username_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False
    

def activate_subscription(username_id):
    conn = sqlite3.connect(File_db)
    cursor = conn.cursor() 
    now = datetime.now()
    future_date = now + relativedelta(months=+1)
    try:
        cursor.execute("""
            UPDATE users
            SET Subscription = ?,
            date = ?
            WHERE username_id = ?
        """, (1, future_date.strftime("%Y-%m-%d %H:%M:%S"), username_id)) 
        rows_affected = cursor.rowcount
        
        conn.commit()
        conn.close()
        return rows_affected > 0
        
    except sqlite3.Error as e:
        print(e)
        conn.close()
        return False
    
def check_subscription_active(username_id):
    conn = sqlite3.connect(File_db)
    cursor = conn.cursor()  
    cursor.execute("""
        SELECT Subscription 
        FROM users 
        WHERE username_id = ? AND Subscription = 1
    """, (username_id,))
    user = cursor.fetchone()  
    conn.close()
    return user is not None

def get_date_by_username_id(username_id: str) -> str | None:
    conn = None
    try:
        conn = sqlite3.connect(File_db)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT date FROM users WHERE username_id = ?",
            (username_id,)
        )
        result = cursor.fetchone() 

        if result:
            return result[0] 
        else:
            return None 

    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")
        return None
    finally:
        if conn:
            conn.close()

def check_try_active(username_id):
    conn = sqlite3.connect(File_db)
    cursor = conn.cursor()  
    cursor.execute("""
        SELECT Subscription 
        FROM users 
        WHERE username_id = ? AND try = 1
    """, (username_id,))
    user = cursor.fetchone()  
    conn.close()
    return user is not None

def activate_try(username_id):
    conn = sqlite3.connect(File_db)
    cursor = conn.cursor() 
    now = datetime.now()
    future_date = now + relativedelta(weeks=1)
    try:
        cursor.execute("""
            UPDATE users
            SET 
                try = ?,
                Subscription = ?,
                date = ?
            WHERE username_id = ?
        """, (0, 1, future_date.strftime("%Y-%m-%d %H:%M:%S"), username_id)) 
        # Обратите внимание на порядок значений в кортеже: (try, Subscription, date, username_id)
        
        rows_affected = cursor.rowcount
        
        conn.commit()
        conn.close()
        return rows_affected > 0
        
    except sqlite3.Error as e:
        print(f"Ошибка при активации 'try' для {username_id}: {e}")
        conn.close()
        return False
