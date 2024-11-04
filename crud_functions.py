import sqlite3


def initiate_db():
    connection = sqlite3.connect('Users.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
        )
        ''')

    connection.commit()
    connection.close()


def get_all_products():
    connection = sqlite3.connect('Products.db')
    cursor = connection.cursor()

    cursor.execute('SELECT title, description, price FROM Products')
    all_products = cursor.fetchall()

    connection.close()

    return all_products


def insert_products(products):
    connection = sqlite3.connect('Products.db')
    cursor = connection.cursor()

    cursor.executemany('''
    INSERT INTO Products (title, description, price)
    VALUES (?, ?, ?)
    ''', products)

    connection.commit()
    connection.close()


def add_user(username, email, age):
    connection = sqlite3.connect('Users.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
                   (username, email, age, 1000))

    connection.commit()


def is_included(username):
    connection = sqlite3.connect('Users.db')
    cursor = connection.cursor()

    cursor.execute('SELECT COUNT(*) FROM Users WHERE username = ?', (username,))
    count = cursor.fetchone()[0]
    return count > 0


initiate_db()

products_table = []
for i in range(1, 5):
    title = f'Product{i}'
    description = f'Капуста{i}'
    price = i * 100
    products_table.append((title, description, price))

# insert_products(products_table)
