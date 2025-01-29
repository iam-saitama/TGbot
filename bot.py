# Этот бот сравнивает два списка (регистрация здесь не нужна по идее, но пусть будет).

import telebot
from telebot import types
import buttons
import database
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from buttons import language_selection_buttons, main_menu, compare_lists_buttons, cancel_button

geolocator = Nominatim(user_agent="geo_locator", timeout=10)

bot = telebot.TeleBot('токен')
users = {}

# Команда старт / выбор языка
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    bot.send_message(user_id, '🌍 Выберите язык / Tilni tanlang:', reply_markup=language_selection_buttons())


@bot.callback_query_handler(func=lambda call: call.data in ['language_russian', 'language_uzbek'])
def handle_language_selection(call):
    user_id = call.from_user.id
    new_text = "✅ Вы выбрали русский язык" if call.data == 'language_russian' else "✅ Siz o'zbek tilini tanladingiz"

    if call.message.text != new_text:
        bot.edit_message_text(new_text, call.message.chat.id, call.message.message_id, reply_markup=None)

    handle_registration_or_action(user_id)


# Поменять язык
@bot.callback_query_handler(func=lambda call: call.data == "change_language")
def change_language(call):
    user_id = call.from_user.id
    bot.send_message(user_id, '🌍 Выберите язык / Select a language:', reply_markup=language_selection_buttons())


# Регистрация
def handle_registration_or_action(user_id):
    try:
        is_registered = database.check_user(user_id)
    except Exception as e:
        print(f"Ошибка базы данных: {e}")
        bot.send_message(user_id, "⚠️ Ошибка сервера. Попробуйте позже.")
        return

    if is_registered:
        bot.send_message(user_id, 'Выберите действие:', reply_markup=buttons.main_menu())
    else:
        bot.send_message(user_id, 'Привет! Напишите свое имя:')
        bot.register_next_step_handler_by_chat_id(user_id, get_name)


# Регистрация имени
def get_name(message):
    user_id = message.from_user.id
    user_name = message.text.strip()

    if not user_name:
        bot.send_message(user_id, '❌ Введите корректное имя')
        bot.register_next_step_handler(message, get_name)
        return

    users[user_id] = {'name': user_name}
    bot.send_message(user_id, 'Отправьте свой номер', reply_markup=buttons.num_button())
    bot.register_next_step_handler(message, get_num)


# Регистрация номера
def get_num(message):
    user_id = message.from_user.id
    if message.contact and hasattr(message.contact, 'phone_number'):
        users[user_id]['phone_number'] = message.contact.phone_number
        bot.send_message(user_id, 'Отправьте свою локацию', reply_markup=buttons.loc_button())
        bot.register_next_step_handler(message, get_loc)
    else:
        bot.send_message(user_id, '❌ Отправьте контакт через кнопку.')
        bot.register_next_step_handler(message, get_num)


# Регистрация локации
def get_loc(message):
    user_id = message.from_user.id
    if message.location:
        try:
            longitude, latitude = message.location.longitude, message.location.latitude
            location = geolocator.reverse((latitude, longitude), timeout=10)
            address = location.address if location else "Адрес не найден"
        except GeocoderTimedOut:
            bot.send_message(user_id, 'Ошибка геолокации. Попробуйте снова.')
            bot.register_next_step_handler(message, get_loc)
            return

        users[user_id]['location'] = address
        database.save_user(user_id, users[user_id]['name'], users[user_id]['phone_number'], address)
        bot.send_message(user_id, 'Спасибо за регистрацию!', reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(user_id, 'Выберите действие:', reply_markup=buttons.main_menu())
    else:
        bot.send_message(user_id, '📍 Отправьте локацию через кнопку.', reply_markup=buttons.loc_button())


# Обработка сравнения списков
@bot.callback_query_handler(func=lambda call: call.data == "compare_lists")
def handle_compare_lists(call):
    bot.answer_callback_query(call.id)
    user_id = call.from_user.id
    bot.send_message(user_id, "📝 Введите первый список (через запятую или с новой строки):",
                     reply_markup=cancel_button())
    bot.register_next_step_handler_by_chat_id(user_id, process_first_list)


# Парсинг введенных списков
def parse_list_input(text):
    elements = []
    for line in text.split('\n'):
        elements.extend([item.strip().lower() for item in line.split(',')])
    return [item for item in elements if item]


# Обработка первого списка
def process_first_list(message):
    user_id = message.from_user.id
    if message.text == "❌ Отмена":
        return go_to_main_menu(message)

    try:
        first_list = parse_list_input(message.text)
        if not first_list:
            raise ValueError("Пустой список")

        users.setdefault(user_id, {})['list1'] = first_list
        bot.send_message(user_id, "📝 Отлично! Теперь введите второй список:",
                         reply_markup=cancel_button())
        bot.register_next_step_handler(message, process_second_list)
    except ValueError:
        bot.send_message(user_id, "❌ Некорректный формат. Введите элементы через запятую или с новой строки:",
                         reply_markup=cancel_button())
        bot.register_next_step_handler(message, process_first_list)


# Обработка второго списка
def process_second_list(message):
    user_id = message.from_user.id
    if message.text == "❌ Отмена":
        return go_to_main_menu(message)

    try:
        second_list = parse_list_input(message.text)
        if not second_list:
            raise ValueError("Пустой список")

        users[user_id]['list2'] = second_list
        send_comparison_results(user_id)
    except ValueError:
        bot.send_message(user_id, "❌ Некорректный формат. Введите элементы через запятую или с новой строки:",
                         reply_markup=cancel_button())
        bot.register_next_step_handler(message, process_second_list)


# Отправка результатов сравнения
def send_comparison_results(user_id):
    list1 = {item.lower() for item in users[user_id]['list1']}
    list2 = {item.lower() for item in users[user_id]['list2']}

    common = list1 & list2
    only_in_first = list1 - list2
    only_in_second = list2 - list1

    message = "\n📊 Результаты сравнения:\n"
    message += f"✅ Общие элементы: {', '.join(common) if common else 'Нет'}\n"
    message += f"🔹 Только в первом списке: {', '.join(only_in_first) if only_in_first else 'Нет'}\n"
    message += f"🔸 Только во втором списке: {', '.join(only_in_second) if only_in_second else 'Нет'}"

    bot.send_message(user_id, message, reply_markup=compare_lists_buttons())


# Обработка повторного сравнения
@bot.callback_query_handler(func=lambda call: call.data == "compare_again")
def repeat_comparison(call):
    bot.answer_callback_query(call.id)
    user_id = call.from_user.id
    bot.send_message(user_id, "📝 Введите первый список (через запятую или с новой строки):",
                     reply_markup=cancel_button())
    bot.register_next_step_handler_by_chat_id(user_id, process_first_list)


# Главное меню (клавиатура)
@bot.callback_query_handler(func=lambda call: call.data == "main_menu")
def handle_main_menu(call):
    user_id = call.from_user.id
    bot.send_message(user_id, "🏠 Вернуться в главное меню:", reply_markup=buttons.main_menu())


# Обработка возврата в главное меню
def go_to_main_menu(message):
    bot.send_message(message.from_user.id, "🏠 Вернуться в главное меню", reply_markup=main_menu())



bot.infinity_polling()