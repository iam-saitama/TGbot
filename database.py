import sqlite3


connection = sqlite3.connect('shop.db', check_same_thread=False)
sql = connection.cursor()


sql.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT, number TEXT UNIQUE, location TEXT);')
sql.execute('CREATE TABLE IF NOT EXISTS products (pr_id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'pr_name TEXT, pr_des TEXT, pr_price REAL, pr_count INTEGER, pr_photo TEXT);')
sql.execute('CREATE TABLE IF NOT EXISTS cart(user_id INTEGER, user_product TEXT, pr_amount INTEGER);')


def register(tg_id, name, num, loc):
    sql.execute('INSERT INTO users VALUES (?, ?, ?, ?);', (tg_id, name, num, loc))
    connection.commit()


def check_user(tg_id):
    if sql.execute('SELECT * FROM users WHERE id=?;', (tg_id,)).fetchone():
        return True
    else:
        return False


# def get_all_pr():
#     return sql.execute('SELECT * FROM products;').fetchall()
#
#
# def get_pr_buttons():
#     all_products = sql.execute('SELECT pr_id, pr_name, pr_count FROM products;').fetchall()
#     in_stock = [n for n in all_products if n[2] > 0]
#     return in_stock