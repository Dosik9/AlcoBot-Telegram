import telebot
from telebot import types
import sqlite3
import os

bot = telebot.TeleBot('TOKEN')

# Подключение к базе данных
conn = sqlite3.connect('alcohol_database.db', check_same_thread=False)
cursor = conn.cursor()

# Определение глобальных переменных
status = 'start'
name = ''
structure = ''


def is_status_start():
    global status
    return status == 'start'

# Приветсвие!
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Напиши название алкоголя, и я отправлю тебе его химическую структуру.')
    global status
    status = 'start'


# Вывод структуры алкоголя
@bot.message_handler(func=lambda message: is_status_start())
def get_structure(message):
    global status
    alcohol_name = message.text.lower()
    query = f"SELECT structure FROM alcohols WHERE name = '{alcohol_name}'"
    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        structure = result[0]
        bot.send_message(message.chat.id, f'Химическая структура {alcohol_name}: <<{structure}>>')

        photo_url = f'img/{alcohol_name}.jpeg'

        if os.path.isfile(photo_url):
            with open(photo_url, 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
        else:
            bot.send_message(message.chat.id, 'К сожалению, у нас нет изобраэжение структуры этого алкоголя :(')
    else:
        if alcohol_name == '/menu':
            status = 'menu'
            menu(message)
        else: bot.send_message(message.chat.id, 'Извините, не могу найти информацию по этому алкоголю.')

# Меню кнопок CRUD
@bot.message_handler(commands=['menu'])
def menu(message):
    global status
    status = 'menu'
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("Добавить", callback_data='add'),
        types.InlineKeyboardButton("Удалить", callback_data='delete'),
        types.InlineKeyboardButton("Обновить", callback_data='update'),
        types.InlineKeyboardButton("Весь список алкоголей", callback_data='display')
    ]
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, 'Добро пожаловать в мой мир, ағашка! \nВыбирай:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def button_handler(call):
    query_data = call.data

    if query_data == 'add':
        intro_add_element(call.message)
    elif query_data == 'delete':
        intro_delete_element(call.message)
    elif query_data == 'update':
        intro_update_element(call.message)
    elif query_data == 'display':
        display_elements(call.message)
    elif query_data == 'name':
        intro_update_name(call.message)
    elif query_data == 'structure':
        intro_update_structure(call.message)
        

# Добавления элемента в базу данных
def intro_add_element(message):
    bot.send_message(message.chat.id, f'Вы хотите добавить новый элемент в базу данных\nВведите названия алкоголя:')
    bot.register_next_step_handler(message, get_add_name)

def get_add_name(message):
    global name
    name = message.text.lower()
    bot.send_message(message.from_user.id, 'Какая у нее структура?')
    bot.register_next_step_handler(message, add_element)

def add_element(message):
    global name, structure
    structure = message.text.upper()
    query = f"INSERT INTO alcohols (name, structure) VALUES ('{name}', '{structure}')"
    bot.send_message(message.chat.id, f'Добавлен новый элемент')
    cursor.execute(query)
    conn.commit()


# Удаления элемента из базы данных
def intro_delete_element(message):
    bot.send_message(message.chat.id, f'Вы хотите удалить элемент из базы данных\nВведите названия алкоголя:')
    bot.register_next_step_handler(message, delete_element)

def delete_element(message):
    name = message.text.lower()
    query = f"DELETE FROM alcohols WHERE name = '{name}'"
    cursor.execute(query)
    conn.commit()
    bot.send_message(message.chat.id, f'Алкоголь был удален')


# Обновление элемента
def intro_update_element(message):
    bot.send_message(message.chat.id, 'Вы нажали на кнопку "Обновить", \nВведите названия алкоголя:')
    bot.register_next_step_handler(message, get_edit_name)
    
def get_edit_name(message):
    global name
    name = message.text.lower()
    query = f"SELECT structure FROM alcohols WHERE name = '{name}'"
    cursor.execute(query)
    result = cursor.fetchone()

    if result:
    
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        buttons = [
            types.InlineKeyboardButton("Название", callback_data='name'),
            types.InlineKeyboardButton("Структуру", callback_data='structure')
        ]
        keyboard.add(*buttons)

        bot.send_message(message.chat.id,'Выбери что хочешь изменить:',reply_markup=keyboard)
        
    else: bot.send_message(message.chat.id, f'К сожалению у нас нет алкоголя с таким названием: {name}!')
    

def intro_update_name(message):
    bot.send_message(message.chat.id, 'Введите новое название алкоголя:')
    bot.register_next_step_handler(message, update_name)

def intro_update_structure(message):
    bot.send_message(message.chat.id, 'Новая структура алкоголя:')
    bot.register_next_step_handler(message, update_structure)

def update_name(message):
    alcohol_name = message.text.lower()
    global name
    query = f"UPDATE alcohols SET name = '{alcohol_name}' WHERE name = '{name}'"
    cursor.execute(query)
    conn.commit()
    bot.send_message(message.chat.id, f'Название алкоголя было изменено!')

def update_structure(message):
    global name
    new_structure = message.text.upper()
    query = f"UPDATE alcohols SET structure = '{new_structure}' WHERE name = '{name}'"
    cursor.execute(query)
    conn.commit()
    bot.send_message(message.chat.id, f'Структура алкоголя была изменена!')
    

# Вывод всех элементов
def display_elements(message):
    query = "SELECT * FROM alcohols"
    cursor.execute(query)
    results = cursor.fetchall()

    if results:
        message_text = "Все элементы:\n"
        n = 1
        for result in results:
            message_text += f"{n}. {result[1]}: {result[2]}\n"
            n += 1
    else:
        message_text = "Элементов нет."

    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=message_text)


bot.polling(none_stop=True, interval=0)