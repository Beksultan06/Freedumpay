import sqlite3
from config import DB_FILE

def create_table():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS subscribers (
                        id INTEGER PRIMARY KEY,
                        chat_id INTEGER UNIQUE NOT NULL,
                        status TEXT NOT NULL,
                        last_payment_date TEXT,
                        remaining_downloads INTEGER DEFAULT 3
                    )''')
    conn.commit()
    conn.close()

def add_subscriber(chat_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO subscribers (chat_id, status) VALUES (?, ?)", (chat_id, "pending_payment"))
    conn.commit()
    conn.close()

def is_subscriber(chat_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM subscribers WHERE chat_id=?", (chat_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def update_remaining_downloads(chat_id, remaining_downloads):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE subscribers SET remaining_downloads=? WHERE chat_id=?", (remaining_downloads, chat_id))
    conn.commit()
    conn.close()

def get_remaining_downloads(chat_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT remaining_downloads FROM subscribers WHERE chat_id=?", (chat_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

create_table()
