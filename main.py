import os
import telebot
import string
import sqlite3

with open(".env") as env_file:
    for line in env_file:
        key, value = line.strip().split("=")
        os.environ[key] = value
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_message(message):
    print(message)
    print_all_items_from_database()

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)



@bot.message_handler(content_types=['document'])
def addfile(message):
    if os.path.isfile("./db/bookshelf.db"):
        pass
    else:
        make_db()
    file_name = message.document.file_name
    file_info = bot.get_file(message.document.file_id)
    file_path = "./books/"+file_name
    tags = message.caption
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)
        add_file_to_db(file_name,file_path,tags)

def make_db():
    con = sqlite3.connect("./db/bookshelf.db")
    cursor = con.cursor()
    cursor.execute("""CREATE TABLE bookshelf
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Name TEXT,
                    Path TEXT,
                    Tags TEXT) """)
    con.commit()
    con.close()

def add_file_to_db(name, path, tags):
    con = sqlite3.connect("./db/bookshelf.db")
    cursor = con.cursor()
    res = (name,path,tags)
    cursor.execute("""INSERT INTO bookshelf (Name, Path, Tags) VALUES (?, ?, ?)""",res)
    con.commit()
    cursor.close()
    con.close()

def print_all_items_from_database():
    con = sqlite3.connect("./db/bookshelf.db")
    cursor = con.cursor()
    select_query = "SELECT * FROM bookshelf"
    cursor.execute(select_query)
    items = cursor.fetchall()

    if items:
        print("Items in the database:")
        for item in items:
            print("ID:", item[0])
            print("Name:", item[1])
            print("Path:", item[2])
            print("Tags:", item[3])
            print("----------------------")
    else:
        print("No items found in the database.")
    cursor.close()
    con.close()


bot.infinity_polling()