# Importing the sqlite3 libraries to allow creation of a database
import sqlite3

# Opening a connection to the database
conn = sqlite3.connect('database2.db')

# Allows SQL statements like 'SELECT' to be executed on the database
c = conn.cursor()

# Specifying the column names and datatype of the database. 'primary key' indicates that the column is the unique identifier for row entries and 'autoincrement' ensures that each new row is incremented by 1. 'NOT NULL' specifies that the particular field may not be empty.
sql = """
DROP TABLE IF EXISTS users;
CREATE TABLE users (
	ID integer unique primary key autoincrement,
	Name TEXT NOT NULL,
	Drink_Preference TEXT NOT NULL,
	Four_Digit_Identifier INTEGER

);"""

c.executescript(sql)  # Create the database
conn.commit()  # Commit changes to the database
conn.close()  # Close the database after use