import sqlite3

# Connect to the SQLite database
connection = sqlite3.connect('shop.db', check_same_thread=False)
sql = connection.cursor()

# Create tables if they don't exist
sql.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER,
        name TEXT,
        number TEXT UNIQUE,
        location TEXT
    );
''')

sql.execute('''
    CREATE TABLE IF NOT EXISTS info (
        event TEXT
    );
''')

# Commit the table creation
connection.commit()


# Регистрация нового юзера
def register(tg_id, name, num, loc):
    try:
        sql.execute('INSERT INTO users VALUES (?, ?, ?, ?);', (tg_id, name, num, loc))
        connection.commit()
        return True  # Registration successful
    except sqlite3.IntegrityError:
        print(f"User with number {num} already exists.")
        return False  # Registration failed (e.g., duplicate number)
    except Exception as e:
        print(f"An error occurred: {e}")
        return False  # Registration failed


# Проверяем, существует ли юзер
def check_user(tg_id):
    try:
        user = sql.execute('SELECT * FROM users WHERE id=?;', (tg_id,)).fetchone()
        return bool(user)  # Return True if user exists, False otherwise
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


# Сохраняем инфу о юзере
def save_user(tg_id, name, num, loc):
    try:
        sql.execute('INSERT INTO users (id, name, number, location) VALUES (?, ?, ?, ?);', (tg_id, name, num, loc))
        connection.commit()
        return True  # User saved successfully
    except sqlite3.IntegrityError:
        print(f"User with ID {tg_id} or number {num} already exists.")
        return False  # User already exists
    except Exception as e:
        print(f"An error occurred while saving user: {e}")
        return False  # Save failed