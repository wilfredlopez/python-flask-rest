import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()


create_table = "CREATE TABLE IF NOT EXISTS users (id int, username text, password text)"
cursor.execute(create_table)

user = (1, 'wilfred', 'password')
users = [
    (2, 'yanna', 'password'),
    (3, 'theudy', 'password')
]
insert_query = "INSERT INTO users VALUES (?,?,?)"
cursor.execute(insert_query, user)
cursor.executemany(insert_query, users)

select_users = 'SELECT * FROM users'

for row in cursor.execute(select_users):
    print(row)

connection.commit()
connection.close()
