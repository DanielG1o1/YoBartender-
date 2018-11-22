import sqlite3
conn = sqlite3.connect('database2.db')
c = conn.cursor()
sql = """
DROP TABLE IF EXISTS users;
CREATE TABLE users (
	ID integer unique primary key autoincrement,
	Name TEXT NOT NULL,
	Drink_Preference TEXT NOT NULL,
	Shot_Preference TEXT,
	Four_Digit_Identifier INTEGER

);
"""
c.executescript(sql)
conn.commit()
conn.close()