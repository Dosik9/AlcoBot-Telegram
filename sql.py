import sqlite3

# Подключение к базе данных (если базы нет, она будет создана)
conn = sqlite3.connect('alcohol_database.db')
cursor = conn.cursor()

# Создание таблицы, если её нет
cursor.execute('''
    CREATE TABLE IF NOT EXISTS alcohols (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        structure TEXT NOT NULL
    )
''')

# Вставка данных в таблицу (пример данных, замените их своими)
cursor.execute('INSERT INTO alcohols (name, structure) VALUES (?, ?)', ('ethanol', 'C2H5OH'))
cursor.execute('INSERT INTO alcohols (name, structure) VALUES (?, ?)', ('propanol', 'C3H7OH'))
cursor.execute('INSERT INTO alcohols (name, structure) VALUES (?, ?)', ('butanol', 'C4H9OH'))
cursor.execute('INSERT INTO alcohols (name, structure) VALUES (?, ?)', ('pentanol', 'C5H11OH'))
cursor.execute('INSERT INTO alcohols (name, structure) VALUES (?, ?)', ('hexanol', 'C6H13OH'))

# Сохранение изменений и закрытие подключения
conn.commit()
conn.close()