import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table_users = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
create_table_items = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(create_table_users)
cursor.execute(create_table_items)

# create_dummy_items = "INSERT INTO items VALUES (Null, 'testing', 10.99)"
# cursor.execute(create_dummy_items)
# user = (1, 'wilfred', 'password')
# users = [
#     (2, 'yanna', 'password'),
#     (3, 'theudy', 'password')
# ]
# insert_query = "INSERT INTO users VALUES (?,?,?)"
# cursor.execute(insert_query, user)
# cursor.executemany(insert_query, users)

# select_users = 'SELECT * FROM users'

# for row in cursor.execute(select_users):
#     print(row)

connection.commit()
connection.close()
