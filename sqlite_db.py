import sqlite3
import os


def sql_start():
    """Подключение/создание БД."""
    global base, cursor
    if os.path.exists('shop.db'):
        base = sqlite3.connect('shop.db')
        cursor = base.cursor()
        base.execute('PRAGMA foreign_keys = ON;')
        print('Соединение с БД установлено.')
    else:
        base = sqlite3.connect('shop.db')
        cursor = base.cursor()
        base.execute('PRAGMA foreign_keys = ON;')
        base.execute('CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY '
                     'KEY AUTOINCREMENT, img TEXT, name TEXT UNIQUE NOT NULL, '
                     'description TEXT, price TEXT NOT NULL)')
        base.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY '
                     'AUTOINCREMENT, user_id INTEGER UNIQUE NOT NULL, '
                     'name TEXT)')
        base.execute('CREATE TABLE IF NOT EXISTS cart(id INTEGER PRIMARY KEY '
                     'AUTOINCREMENT, user_id INTEGER NOT NULL, product_id '
                     'INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES '
                     'users(user_id), FOREIGN KEY (product_id) REFERENCES '
                     'products(id) ON DELETE CASCADE)')
        base.execute('CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY '
                     'KEY AUTOINCREMENT, user_id INTEGER NOT NULL, order_id '
                     'INTEGER UNIQUE NOT NULL, order_info TEXT NOT NULL, '
                     'FOREIGN KEY (user_id) REFERENCES users(user_id))')
        base.commit()


async def sql_add_user(data):
    """Принимает кортеж из id и имени. Проверяет наличие id в БД и в случае
    отсутствия добавление клиента(from_user.id) в таблицу "users"
    (список клиентов по id тг)."""
    in_user_id = cursor.execute('SELECT user_id FROM users WHERE user_id == ?',
                                (data[0],)).fetchall()
    if not in_user_id:
        cursor.execute('INSERT INTO users (user_id, name) VALUES (?, ?)', data)
        base.commit()


async def sql_add_product(data):
    """Принимает словарь из идентификатора изображения, имени, описания и цены.
    Добавляет продукт в таблицу "products"."""
    cursor.execute(
        'INSERT INTO products (img, name, description, price) '
        'VALUES (?, ?, ?, ?)',
        tuple(data.values())
    )
    base.commit()


async def sql_read_products():
    """Чтение всей таблицы "products". Возвращает список кортежей."""
    return cursor.execute('SELECT * FROM products').fetchall()


async def sql_delete_product(data):
    """Принимает значение id продукта. Выполняет удаление продукта из таблицы
    "products"."""
    cursor.execute('DELETE FROM products WHERE id = ?', (data,))
    base.commit()


async def sql_add_cart(data):
    """Принимает кортеж из id пользователя (id берётся из тг) и id товара.
    Выполняет добавление товара в таблицу "cart"."""
    cursor.execute('INSERT INTO cart (user_id, product_id) VALUES (?, ?)',
                   data)
    base.commit()


async def sql_select_cart_user(data):
    """Принимает id пользователя (id берётся из тг). Осуществляет выборку по
    user_id из таблицы "cart". Возвращает список кортежей."""
    return cursor.execute(
        'SELECT id, product_id FROM cart WHERE user_id = ?',
        (data,)
    ).fetchall()


async def sql_select_products_id(data):
    """Принимает id продукта в таблице "products". Осуществляет выборку по id
    из таблицы "products". Возвращает результат в форме строки."""
    return cursor.execute('SELECT * FROM products WHERE id = ?',
                          (data,)).fetchone()


async def sql_delete_cart(data):
    """Принимает id продукта. Удаление строки(продукта) из таблицы "cart"."""
    cursor.execute('DELETE FROM cart WHERE id == ?', (data,))
    base.commit()


async def sql_delete_all_cart(data):
    """Принимает id пользователя (id из тг). Удаление всех строк (очистка
    корзины) из таблицы "cart"."""
    cursor.execute('DELETE FROM cart WHERE user_id == ?', (data,))
    base.commit()


async def sql_add_order(data):
    """Принимает кортеж содержащий id клиента, id заказа и информацию по
    заказу. Добавление заказа в таблицу "orders"."""
    cursor.execute(
        'INSERT INTO orders (user_id, order_id, order_info) VALUES (?, ?, ?)',
        data
    )
    base.commit()
