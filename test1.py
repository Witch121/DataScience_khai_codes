import sqlite3
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
user_input = input("Enter your name: ")
query = "SELECT * FROM users WHERE name = '" + user_input + "'"
cursor.execute(query)
