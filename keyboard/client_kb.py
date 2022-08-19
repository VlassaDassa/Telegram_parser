from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


b1 = KeyboardButton('Помощь 🔎')
b2 = KeyboardButton('Начать парсинг 🚀')
b3 = KeyboardButton('Запланировать парсинг 🕛')
cancel = KeyboardButton('Отменить парсинг')
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.row(b1, b2).row(b3, cancel)


menu = 'Меню 💤'

bt1 = KeyboardButton('Удалить таблицу ❌')
exist_spreadsheet = ReplyKeyboardMarkup(resize_keyboard=True)
exist_spreadsheet.row(bt1, menu)



clothes = KeyboardButton('Одежда 👗')
books = KeyboardButton('Книги 📚')
phone = KeyboardButton('Смартфоны 📱')
category = ReplyKeyboardMarkup(resize_keyboard=True)
category.row(clothes, books).row(phone, menu)


kb_remove = ReplyKeyboardRemove()


excel = KeyboardButton('Excel')
google_sheet = KeyboardButton('Google sheet')
method_unload = ReplyKeyboardMarkup(resize_keyboard=True)
method_unload.row(excel, google_sheet).add(menu)


but1 = KeyboardButton('Поиск минимальной цены')
but2 = KeyboardButton('Интервальный парсинг')
time_parsing = ReplyKeyboardMarkup(resize_keyboard=True)
time_parsing.row(but1, but2).add(menu)



time1 = KeyboardButton('В определённое время')
time2 = KeyboardButton('Интервал')
find_time_range = ReplyKeyboardMarkup(resize_keyboard=True)
find_time_range.row(time1, time2).add(menu)













