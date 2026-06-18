import sqlite3

conn = sqlite3.connect(
    "complaints.db"
)

cursor = conn.cursor()

try:

    cursor.execute(
        """
        ALTER TABLE complaints
        ADD COLUMN email TEXT
        """
    )

    print(
        "Email column added."
    )

except Exception as e:

    print(
        "Column may already exist:"
    )

    print(e)

conn.commit()
conn.close()