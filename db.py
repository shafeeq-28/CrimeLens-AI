import sqlite3

def create_table():

    conn = sqlite3.connect("complaints.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaints(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        name TEXT,
        incident TEXT,
        location TEXT,
        date TEXT,
        crime_type TEXT,
        status TEXT,
        formal_complaint TEXT
    )
    """)

    conn.commit()

    conn.close()


create_table()