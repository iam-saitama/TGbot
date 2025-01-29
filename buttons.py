from telebot import types


# Кнопки для выбора языка
def language_selection_buttons():
    kb = types.InlineKeyboardMarkup()
    btn_ru = types.InlineKeyboardButton("🇷🇺 Русский", callback_data="language_russian")
    btn_uz = types.InlineKeyboardButton("🇺🇿 O'zbek", callback_data="language_uzbek")
    kb.add(btn_ru, btn_uz)
    return kb


# Кнопки главного меню
def main_menu():
    kb = types.InlineKeyboardMarkup()
    btn_change_lang = types.InlineKeyboardButton("🔄 Сменить язык", callback_data="change_language")
    btn_compare = types.InlineKeyboardButton("📊 Сравнить списки", callback_data="compare_lists")
    kb.add(btn_compare)
    kb.add(btn_change_lang)
    return kb


# Кнопка для отправки номера
def num_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    num = types.KeyboardButton('Отправить номер📞', request_contact=True)
    kb.add(num)
    return kb


# Кнопка отправки локации
def loc_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    but1 = types.KeyboardButton('Отправить локацию📌', request_location=True)
    kb.add(but1)
    return kb


# Кнопки после сравнения списков
def compare_lists_buttons():
    kb = types.InlineKeyboardMarkup()
    btn_again = types.InlineKeyboardButton("🔄 Сравнить заново", callback_data="compare_again")
    btn_main = types.InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")
    kb.add(btn_again)
    kb.add(btn_main)
    return kb


# Кнопка отмены
def cancel_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(types.KeyboardButton("❌ Отмена"))
    return kb