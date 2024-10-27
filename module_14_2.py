import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

# users_data = []
# for i in range(1, 11):
#     username = f'User{i}'
#     email = f'example{i}@gmail.com'
#     age = i * 10
#     balance = 1000
#     users_data.append((username, email, age, balance))

# cursor.executemany('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)', users_data)
# cursor.execute('UPDATE Users SET balance = 500 WHERE id % 2 = 1')
cursor.execute('DELETE FROM Users WHERE id = 6')
cursor.execute('SELECT COUNT(*) FROM Users')
total_users = cursor.fetchone()[0]
cursor.execute('SELECT SUM(balance) FROM Users')
all_balances = cursor.fetchone()[0]
print(all_balances / total_users)

# results = cursor.fetchall()

# for row in results:
#     username, email, age, balance = row
#     print(f'Имя: {username} | Почта: {email} | Возраст: {age} | Баланс: {balance}')
connection.commit()
connection.close()
