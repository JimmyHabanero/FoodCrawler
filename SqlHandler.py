import sqlite3

conn = sqlite3.connect('food_database.db')
c = conn.cursor()

c.execute("""CREATE TABLE food_database (
            name text,
            protein real,
            fat real,
            carbs real,
            kcal int
            )""")

conn.commit()

conn.close()
