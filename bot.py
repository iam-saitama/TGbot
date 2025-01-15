import telebot
import buttons
import database
from geopy import Nominatim

geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                  "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

bot = telebot.TeleBot('7326578244:AAGWWYsRJ3UwFuyWms7pBLAzrLB2QJjD7yY')
users = {}


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if database.check_user(user_id):
        bot.send_message(user_id, f'Добро пожаловать, @{message.from_user.username}!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(user_id, 'Выберите пункт меню:', reply_markup=buttons.main_menu(database.get_all_pr()))
    else:
        bot.send_message(user_id, 'Привет! Начнем регистрацию!\nНапишите свое имя',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_name)


# @bot.message_handler(commands=['help'])
# def help(message):
#     user_id = message.from_user.id
#     print(message)
#     bot.send_message(user_id, 'Справочная информация', reply_markup=buttons.main_menu(database.get_all_pr()))


def get_name(message):
    user_id = message.from_user.id
    user_name = message.text
    bot.send_message(user_id, 'Отлично! Теперь отправьте свой номер!',
                     reply_markup=buttons.num_button())
    bot.register_next_step_handler(message, get_num)


def get_num(message):
    user_id = message.from_user.id
    if message.contact:
        user_num = message.contact.phone_number
        bot.send_message(user_id, 'Отлично! Теперь отправьте свою локацию!',
                         reply_markup=buttons.loc_button())
        bot.register_next_step_handler(message, get_loc)
    else:
        bot.send_message(user_id, 'Отправьте контакт по кнопке или отправьте контакт через скрепку!')
        bot.register_next_step_handler(message, get_num)


def get_loc(message):
    user_id = message.from_user.id
    if message.location:
        print(message.location)
        longitude = message.location.longitude
        print(longitude)
        latitude = message.location.latitude
        print(latitude)
        address = geolocator.reverse((longitude, latitude)).address
        print(address)


bot.infinity_polling()