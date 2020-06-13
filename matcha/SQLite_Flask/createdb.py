import sqlite3

conn = sqlite3.connect('database.db')
print ("Opened database successfully")

conn.execute("""CREATE TABLE students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            addr TEXT,
            city TEXT,
            pin TEXT,
            image_file TEXT DEFAULT "default.jpg" NOT NULL
            )""")

print ("Table created successfully")
conn.close()