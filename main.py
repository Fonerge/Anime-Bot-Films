import telebot
from telebot import types
import re

bot = telebot.TeleBot("YOUR BOTFATHER TOKEN")

def start_markup():
    markup = types.InlineKeyboardMarkup(row_width=True)
    link_keyboard_1 = types.InlineKeyboardButton(text="Grand Anime Films", url="https://t.me/+TmV-wgYCIhE4ZjVi")
    check_keyboard = types.InlineKeyboardButton(text="Проверить подписку ✅", callback_data="check")
    markup.add(link_keyboard_1, check_keyboard)
    return markup

# Функция для проверки подписки пользователя на канал
def check_subscription(chat_id):
    status = ['creator', 'administrator', 'member']
    for i in status:
        if i == bot.get_chat_member(chat_id='TELEGARM CHANNEL ID', user_id=chat_id).status: #Здесь необходимо указать id канала, предворительно добавив бота в него.
            return True
    return False

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    first_name = message.chat.first_name
    bot.send_message(chat_id, f"{first_name}, Вас приветствует Grand Anime Bot!\nЧтобы воспользоваться ботом подпишитесь на каналы!", reply_markup=start_markup())

@bot.callback_query_handler(func=lambda message: True)
def callback(call):
    if call.data == 'check':
        chat_id = call.message.chat.id
        if check_subscription(chat_id):
            bot.send_message(chat_id, "Спасибо, что подписались на канал!\nТеперь вы можете воспользоваться ботом.", reply_markup=start_markup())
        else:
            bot.send_message(chat_id, "Подпишитесь на каналы!", reply_markup=start_markup())

@bot.message_handler(func=lambda message: True)
def check_movie(message):
    chat_id = message.chat.id
    user_text = message.text

    movie_code = re.findall(r'#(\d+)', user_text)
    if movie_code:
        movie_code = int(movie_code[0])
        if check_subscription(chat_id):
            movie_name = get_movie_name_by_code(movie_code)  # Функция для получения названия фильма по коду
            if movie_name:
                bot.send_message(chat_id, f"Название аниме: {movie_name}")
            else:
                bot.send_message(chat_id, 'Фильм не найден')
        else:
            bot.send_message(chat_id, 'Подпишитесь на телеграм каналы.')

# Заглушка для функции получения названия фильма по коду
def get_movie_name_by_code(code):
    movies = {
        1111: "Тетрадь смерти",
        2222: "Токийский гуль"
    }
    return movies.get(code)

bot.polling(non_stop=True)
