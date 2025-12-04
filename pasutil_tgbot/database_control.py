import sqlite3

File_db = 'telegram_users.db'

def create_table():
    conn = sqlite3.connect(File_db)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username_id TEXT UNIQUE NOT NULL,
            Subscription BOOLEAN DEFAULT 0
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
    try:
        cursor.execute("""
            UPDATE users 
            SET Subscription = 1 
            WHERE username_id = ?
        """, (username_id,))
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
