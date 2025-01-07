import telebot
import buttons
import database

bot = telebot.TeleBot('7826154830:AAHNPIx0leCLYLvlEgX1xmZIOSSxQyrDxDE')
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


@bot.message_handler(commands=['help'])
def help(message):
    user_id = message.from_user.id
    print(message)
    bot.send_message(user_id, 'Справочная информация', reply_markup=buttons.main_menu(database.get_all_pr()))


def get_name(message):
    user_id = message.from_user.id
    user_name = message.text
    bot.send_message(user_id, 'Отлично! Теперь отправьте свой номер!',
                     reply_markup=buttons.num_button())
    bot.register_next_step_handler(message, get_num, user_name)



def get_num(message, user_name):
    user_id = message.from_user.id
    if message.contact:
        user_num = message.contact.phone_number
        bot.send_message(user_id, 'Отлично! Теперь отправьте свою локацию!',
                         reply_markup=buttons.loc_button())
        bot.register_next_step_handler(message, user_name, get_loc, user_num)
    else:
        bot.send_message(user_id, 'Отправьте контакт по кнопке или отправьте контакт через скрепку!')
        bot.register_next_step_handler(message, get_num, user_name)


def get_loc(message, text, user_name, user_num):
    user_id = message.from_user.id
    if message.location:
        user_loc = message.text
        text += f'Клиент: @{message.from_user.username}'
        bot.send_message(43331040, text)
        bot.send_location(43331040, latitude=message.location.latitude, longitude=message.location.longitude)
        database.register(user_id, user_name, user_num, user_loc)
        bot.send_message(user_id, 'Регистрация прошла успешно!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(user_id, 'Выберите пункт меню:', reply_markup=buttons.main_menu(database.get_pr_buttons()))
    else:
        bot.send_message(user_id, 'Отправьте локацию по кнопке или через скрепку!')
        bot.register_next_step_handler(message, get_loc, text)



bot.polling(non_stop=True)