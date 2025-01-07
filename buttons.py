from telebot import types


# Кнопка для отправки номера
def num_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    num = types.KeyboardButton('Отправить номер📞', request_contact=True)
    kb.add(num)

    return kb


# Кнопки главного меню
def main_menu(products):
    kb = types.InlineKeyboardMarkup(row_width=2)
    info = types.InlineKeyboardButton(text='Справочная информация', callback_data='info')
    all_products = [types.InlineKeyboardButton(text=f'{i[1]}', callback_data=i[0]) for i in products]
    kb.add(*all_products)
    kb.row(info)

    return kb


# Кнопка отправки локации
def loc_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton('Отправить локацию📌', request_location=True)
    kb.add(but1)

    return kb