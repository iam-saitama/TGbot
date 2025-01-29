import sqlite3
import json

# Создание таблиц
def initialize_db():
    with sqlite3.connect('data.db') as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                number TEXT UNIQUE NOT NULL,
                location TEXT NOT NULL,
                registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS comparisons (
                comparison_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                list1 TEXT NOT NULL,
                list2 TEXT NOT NULL,
                comparison_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
        ''')
        conn.commit()


# Сохранение пользователя
def save_user(tg_id, name, num, loc):
    try:
        with sqlite3.connect('data.db') as conn:
            cur = conn.cursor()
            cur.execute('''
                INSERT OR IGNORE INTO users (id, name, number, location)
                VALUES (?, ?, ?, ?);
            ''', (tg_id, name, num, loc))
            conn.commit()
        return True
    except Exception as e:
        print(f"Ошибка при сохранении пользователя: {str(e)}")
        return False


# Проверка, зарегистрирован ли пользователь
def check_user(tg_id):
    try:
        with sqlite3.connect('data.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT 1 FROM users WHERE id = ?;', (tg_id,))
            return cur.fetchone() is not None
    except Exception as e:
        print(f"Ошибка при проверке пользователя: {str(e)}")
        return False


# Сохранение истории сравнений
def save_comparison(user_id, list1, list2):
    try:
        if not isinstance(list1, list) or not isinstance(list2, list):
            raise ValueError("Оба списка должны быть списками")

        with sqlite3.connect('data.db') as conn:
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO comparisons (user_id, list1, list2)
                VALUES (?, ?, ?);
            ''', (user_id, json.dumps(list1), json.dumps(list2)))
            conn.commit()
        return True
    except Exception as e:
        print(f"Ошибка при сохранении сравнения: {str(e)}")
        return False


# Возвращает последние сравнения пользователя
def get_user_comparisons(tg_id, limit=5):
    try:
        with sqlite3.connect('data.db') as conn:
            cur = conn.cursor()
            cur.execute('''
                SELECT list1, list2, comparison_date 
                FROM comparisons 
                WHERE user_id = ?
                ORDER BY comparison_date DESC
                LIMIT ?;
            ''', (tg_id, limit))
            rows = cur.fetchall()

            return [ {
                'list1': json.loads(row[0]),
                'list2': json.loads(row[1]),
                'date': row[2]
            } for row in rows]

    except Exception as e:
        print(f"Ошибка при получении сравнений: {str(e)}")
        return []


initialize_db()