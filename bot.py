import telebot
import pymysql
import configsql

# Подключение к базе данных
mydb = pymysql.connect(
    host = configsql.host,
    user = configsql.user,
    password = configsql.password
)
mycursor = mydb.cursor()

# Токен вашего телеграм бота
TOKEN = configsql.TOKEN
# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Идентификаторы пользователей, которым разрешено использовать бота
allowedchatids = configsql.admin

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handlestart(message):
    if message.chat.id not in allowedchatids:
        bot.send_message(message.chat.id, "Прошу прощения но я не могу вам позволить вводить комманы, так как вы не указаны в моем коде как управляющее лицо.")
    else:
        bot.send_message(message.chat.id, "Привет! Я бот для управления базой данных MySQL разработанный Web Arxem.\nВот мои комманды:\n/create_db - Создать базу данных\n/delete_db - Удалить базу данных\n/create_table - Создать таблицу\n/delete_table - удалить таблицу\nНо также комманды можно посмотреть во вкладке 'Меню'")

# Обработчик команды /create_db
@bot.message_handler(commands=['create_db'])
def handle_create_db(message):
    if message.chat.id not in allowedchatids:
        bot.send_message(message.chat.id, "Прошу прсчения но я не могу вам позволить вводить комманы, так как вы не указаны в моем коде как управляющее лицо.")
    else:
        bot.send_message(message.chat.id, "Введите название базы данных:")
        bot.register_next_step_handler(message, create_db_command)

def create_db_command(message):
    try:
        mycursor.execute(f"CREATE DATABASE {message.text}")
        bot.send_message(message.chat.id, f"База данных '{message.text}' успешно создана.")
    except pymysql.Error as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при создании базы данных: {e}")

# Обработчик команды /delete_db
@bot.message_handler(commands=['delete_db'])
def handle_delete_db(message):
    if message.chat.id not in allowedchatids:
        bot.send_message(message.chat.id, "Прошу прсчения но я не могу вам позволить вводить комманы, так как вы не указаны в моем коде как управляющее лицо.")
    else:
        bot.send_message(message.chat.id, "Введите название базы данных для удаления:")
        bot.register_next_step_handler(message, delete_db_command)

def delete_db_command(message):
    try:
        mycursor.execute(f"DROP DATABASE {message.text}")
        bot.send_message(message.chat.id, f"База данных '{message.text}' успешно удалена.")
    except pymysql.Error as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при удалении базы данных: {e}")

# Обработчик команды /create_table
@bot.message_handler(commands=['create_table'])
def handle_create_table(message):
    if message.chat.id not in allowedchatids:
        bot.send_message(message.chat.id, "Прошу прсчения но я не могу вам позволить вводить комманы, так как вы не указаны в моем коде как управляющее лицо.")
    else:
        bot.send_message(message.chat.id, "Введите название базы данных:")
        bot.register_next_step_handler(message, create_table_database)

def create_table_database(message):
    try:
        mycursor.execute(f"USE {message.text}")
        bot.send_message(message.chat.id, "Введите название таблицы:")
        bot.register_next_step_handler(message, create_table_name, message.text)
    except pymysql.Error as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при подключении к базе данных: {e}")

def create_table_name(message, database_name):
    try:
        table_name = message.text
        mycursor.execute(f"CREATE TABLE {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))")
        bot.send_message(message.chat.id, f"Таблица '{table_name}' успешно создана в базе данных '{database_name}'.")
    except pymysql.Error as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при создании таблицы: {e}")

# Обработчик команды /delete_table
@bot.message_handler(commands=['delete_table'])
def handle_delete_table(message):
    if message.chat.id not in allowedchatids:
        bot.send_message(message.chat.id, "Прошу прсчения но я не могу вам позволить вводить комманы, так как вы не указаны в моем коде как управляющее лицо.")
    else:
        bot.send_message(message.chat.id, "Введите название базы данных:")
        bot.register_next_step_handler(message, delete_table_database)

def delete_table_database(message):
    try:
        mycursor.execute(f"USE {message.text}")
        bot.send_message(message.chat.id, "Введите название таблицы для удаления:")
        bot.register_next_step_handler(message, delete_table_name, message.text)
    except pymysql.Error as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при подключении к базе данных: {e}")

def delete_table_name(message, database_name):
    try:
        table_name = message.text
        mycursor.execute(f"DROP TABLE {table_name}")
        bot.send_message(message.chat.id, f"Таблица '{table_name}' успешно удалена из базы данных '{database_name}'.")
    except pymysql.Error as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при удалении таблицы: {e}")

# Запуск бота
bot.polling()
