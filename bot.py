import telebot
from telebot import types
import buttons
import database
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

geolocator = Nominatim(user_agent="geo_locator", timeout=10)

bot = telebot.TeleBot('7326578244:AAGWWYsRJ3UwFuyWms7pBLAzrLB2QJjD7yY')
users = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if database.check_user(user_id):
        bot.send_message(user_id, f'Добро пожаловать, @{message.from_user.username}!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(user_id, 'Выберите пункт меню:', reply_markup=buttons.main_menu(database.info()))
    else:
        bot.send_message(user_id, 'Привет! Начнем регистрацию!\nНапишите свое имя',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_name)

@bot.message_handler(commands=['help'])
def help(message):
    user_id = message.from_user.id
    print(message)
    bot.send_message(user_id, 'Справочная информация', reply_markup=buttons.main_menu(database.info()))

def get_name(message):
    user_id = message.from_user.id
    user_name = message.text
    users[user_id] = {'name': user_name}
    bot.send_message(user_id, 'Отлично! Теперь отправьте свой номер!',
                     reply_markup=buttons.num_button())
    bot.register_next_step_handler(message, get_num)

def get_num(message):
    user_id = message.from_user.id
    if message.contact:
        user_num = message.contact.phone_number
        users[user_id]['phone_number'] = user_num
        bot.send_message(user_id, 'Отлично! Теперь отправьте свою локацию!',
                         reply_markup=buttons.loc_button())
        bot.register_next_step_handler(message, get_loc)
    else:
        bot.send_message(user_id, 'Отправьте контакт по кнопке или отправьте контакт через скрепку!')
        bot.register_next_step_handler(message, get_num)


def get_loc(message):
    user_id = message.from_user.id
    if message.location:
        try:
            longitude = message.location.longitude
            latitude = message.location.latitude
            address = geolocator.reverse((latitude, longitude), timeout=10).address
            print(f"Локация пользователя: {address}")

            user_name = users[user_id]['name']
            user_num = users[user_id]['phone_number']

            database.save_user(user_id, user_name, user_num, address)

            bot.send_message(
                user_id,
                'Спасибо за регистрацию!',
                reply_markup=types.ReplyKeyboardRemove()
            )
        except GeocoderTimedOut:
            bot.send_message(user_id, 'Ошибка при определении локации. Пожалуйста, попробуйте снова.')
    else:
        markup = types.ReplyKeyboardMarkup(
            one_time_keyboard=True,
            resize_keyboard=True
        )
        markup.add(types.KeyboardButton("Отправить локацию", request_location=True))

        bot.send_message(
            user_id,
            'Пожалуйста, отправьте свою локацию.',
            reply_markup=markup
        )
        bot.register_next_step_handler(message, get_loc)

bot.infinity_polling()