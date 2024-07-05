from create_google_parser_bot import bot, dp
from aiogram import Dispatcher, types

#FSM
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

#FILTERS
from aiogram.dispatcher.filters import Text

# PATH
from pathlib import Path

# DATABASE
from database.sqlite_db import Database

# Time
import datetime

# Keyboard
from keyboard import client_kb as cl_kb

# Spreadsheet
from google_sheet.create_start_sheet import create_start_sheet
from google_sheet.insert_data import insert_values

# Config
import config as cfg

# Thread
from threading import Thread

# Asyncio
import asyncio

# Excel
from excel.excel_create_doc import create_excel_book, insert_to_excel

# OS
import os

# Parser
from handlers import time_pars

# APScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler



dir_path = str(Path.cwd())
path_to_db = str(Path(dir_path, 'google_parser.db'))
db = Database(path_to_db)




# Start
async def start(message: types.Message):
    welcome_text = '<b>Привет! ✋</b>\n' \
                   'Это бот-парсер, с его помощью вы можете автоматизировать сбор данных с Wildberries'
    dir_path = str(Path.cwd())
    path_to_logo_wb = str(Path(dir_path, 'assets', 'logo_wildberries.jpg'))
    logo_wb = open(path_to_logo_wb, 'rb')
    await message.answer(welcome_text, parse_mode='HTML', reply_markup=cl_kb.main_menu)
    await bot.send_photo(message.from_user.id, logo_wb)

    # Registration
    cur_date = datetime.datetime.now().strftime('%d-%m-%Y')
    if message.from_user.username is None:
        user_name = message.from_user.full_name
    else:
        user_name = message.from_user.username
    tgid = message.from_user.id
    await db.reg_user(user_name, tgid, cur_date)
    await db.set_status_errors(message.from_user.id)
    await db.set_parsing_status(message.from_user.id)
    await db.set_schedule_status(message.from_user.id)

    if not os.path.exists(str(Path(str(Path.cwd()), 'data', f'{message.from_user.id}.xlsx'))):
        create_excel_book(message.from_user.id)





# Help
async def help(message: types.Message):
    help_message = '<b>Как пользоваться этим ботом?</b>\n' \
                   'Чтобы начать пользоваться ботом вам необходимо создать <a href="https://www.google.ru/intl/ru/sheets/about/">Google таблицу</a>\n' \
                   'Затем выдать разрешение на редактирование нашему боту'

    bot_gmail = 'Почта, который нужно выдать разрешение:\n `test-336@nimble-petal-354410.iam.gserviceaccount.com`\n' \
                'После этого пришлите ссылку на эту таблицу:\n `/set_table __ссылка на таблицу__`'


    img1 = open(str(Path(str(Path.cwd()), 'assets', 'inst_1.JPG')), 'rb')
    img2 = open(str(Path(str(Path.cwd()), 'assets', 'inst_2.JPG')), 'rb')

    await message.answer(help_message, parse_mode='HTML', disable_web_page_preview=True)
    await bot.send_photo(message.from_user.id, img1)
    await bot.send_photo(message.from_user.id, img2)
    await message.answer(bot_gmail, parse_mode='MARKDOWN')



async def set_table(message: types.Message):
    if not await db.check_exist_spreadsheet(message.from_user.id):
        try:
            message.text.split(' ')[1]
        except IndexError:
            await message.answer('Неверная команда. Правильно - `/set_table ссылка на таблицу)`', parse_mode='MARKDOWN')
        else:
            link_to_spreadsheet = message.text.split(' ')[1]
            if len(link_to_spreadsheet) > 39:
                if 'https://docs.google.com/spreadsheets/d/' in link_to_spreadsheet[:39]:
                    await db.add_spreadsheet(message.from_user.id, message.text.split(' ')[1])
                    link_to_spreadsheet = await db.get_spreadsheetid(message.from_user.id)
                    spreadsheet_id = link_to_spreadsheet[0].split('/')[5]

                    start_sheet = Thread(target=create_start_sheet, args=(cfg.CREDENTIALS, spreadsheet_id, message.from_user.id))
                    start_sheet.start()
                    collapse_message = await bot.send_sticker(message.from_user.id, 'CAACAgIAAxkBAAIHvGLD7IfmXUxoiO9RnLPhOSSZy1f2AAIjAAMoD2oUJ1El54wgpAYpBA')
                    await asyncio.sleep(5)
                    await bot.delete_message(message.from_user.id, collapse_message.message_id)
                    if await db.get_status_errors(message.from_user.id):
                        await message.answer('Таблица успешно построена ✔', reply_markup=cl_kb.main_menu)
                    else:
                        await message.answer('<b>Ошибка!</b>\nВозможно вы не выдали разрешение на редактирование боту.\n<i>См. "Помощь 🔎"</i>', parse_mode='HTML', reply_markup=cl_kb.main_menu)
                        await db.delete_spreadsheet(message.from_user.id)
                else:
                    await message.answer('Ссылка введена неверно')
            else:
                await message.answer('Ссылка введена неверно')
    else:
        await message.answer('У вас уже есть таблица', reply_markup=cl_kb.exist_spreadsheet)



async def delete_spreadsheet(message: types.Message):
    await db.delete_spreadsheet(message.from_user.id)
    await message.answer('Таблицу успешно удалена ✔', reply_markup=cl_kb.main_menu)



async def menu(message: types.Message, state: FSMContext):
    await message.answer('Меню 💤', reply_markup=cl_kb.main_menu)
    await message.delete()
    await state.finish()






class FSMstart_parsing(StatesGroup):
    category = State()
    count_pages = State()
    choice = State()



async def start_parsing(message: types.Message):
    if not bool(await db.get_parsing_status(message.from_user.id)):
        await message.answer('Выберите категорию:', reply_markup=cl_kb.category)
        await FSMstart_parsing.category.set()
    else:
        await message.answer('<b>Ошибка</b>\n'
                             'Вы уже начали парсинг, дождитесь его окончания',
                             parse_mode='HTML')

async def choice_category(message: types.Message,  state: FSMContext):
    if message.text in cfg.CATEGORY.keys():
        async with state.proxy() as data:
            data['category'] = message.text
            await message.answer('Выберите кол-во страниц\n<b>Диапазон 1-100</b>', reply_markup=cl_kb.kb_remove, parse_mode='HTML')
        await FSMstart_parsing.next()
    else:
        await message.answer('Такой категории нет', reply_markup=cl_kb.main_menu)
        await state.finish()



async def choice_count_pages(message: types.Message, state: FSMContext):
    try:
        int(message.text)
    except ValueError:
        await message.answer('Введите целое число', reply_markup=cl_kb.main_menu)
        await state.finish()
    else:
        if int(message.text) in range(1, 101):

            async with state.proxy() as data:
                data['count_pages'] = message.text
            await message.answer('<b>Выберите способ выгрузки</b>\n'
                                 'Excel - быстро, локально, неудобно\n'
                                 'Google sheet - очень долго, удобно',
                                 reply_markup=cl_kb.method_unload, parse_mode='HTML')
            await FSMstart_parsing.next()
        else:
            await message.answer('Введите число в диапазоне от 1 до 100', reply_markup=cl_kb.main_menu)
            await state.finish()


async def pars_google_sheet(message: types.Message, state: FSMContext):
    if await db.check_exist_spreadsheet(message.from_user.id):
        async with state.proxy() as data:
            link_to_spreadsheet = await db.get_spreadsheetid(message.from_user.id)
            spreadsheet_id = link_to_spreadsheet[0].split('/')[5]
            working_hours = ((int(data['count_pages']) * 30) * 25) / 60
            await message.answer(f'Парсинг по категории: <b>{data["category"]}</b>\n'
                                 f'С количеством страниц: <b>{data["count_pages"]}</b>\n'
                                 f'<b>Начался</b> 🚀\n\n'
                                 f'Примерное время ожидания: <b>{working_hours} минут</b>\n'
                                 f'<b>Метод:</b> Google sheet',
                                 parse_mode='HTML', reply_markup=cl_kb.main_menu)
            start_pars = Thread(target=insert_values, args=(cfg.CREDENTIALS, spreadsheet_id, data['count_pages'],
                                                            data['category'], message.from_user.id))
            start_pars.start()
            collapse_sticker = await bot.send_sticker(message.from_user.id,'CAACAgIAAxkBAAIHvGLD7IfmXUxoiO9RnLPhOSSZy1f2AAIjAAMoD2oUJ1El54wgpAYpBA')
            await state.finish()
            time_work = (int(data['count_pages']) * 100 * 20)
            for i in range(time_work):
                if start_pars.is_alive():
                    await asyncio.sleep(0.5)
                else:
                    await bot.delete_message(message.from_user.id, collapse_sticker.message_id)
                    await message.answer(f'Парсинг по категории: <b>{data["category"]}</b>\n'
                                         f'С количеством страниц: <b>{data["count_pages"]}</b>\n'
                                         f'<b>Окончился</b> 🚀\n\n'
                                         f'Примерное время ожидания: <b>{working_hours} минут</b>\n'
                                         f'<b>Метод:</b> Google sheet',
                                         parse_mode='HTML', reply_markup=cl_kb.main_menu)
                    break
    else:
        await message.answer('<b>Ошибка</b>\n'
                             'У вас ещё нет Google sheet\n'
                             'см. "Помощь 🔎"',
                             reply_markup=cl_kb.main_menu, parse_mode='HTML')
        await state.finish()



async def pars_excel(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        working_hours = (int(data['count_pages']) * 30) / 60
        await message.answer(f'Парсинг по категории: <b>{data["category"]}</b>\n'
                             f'С количеством страниц: <b>{data["count_pages"]}</b>\n'
                             f'<b>Начался</b> 🚀\n\n'
                             f'Примерное время ожидания: <b>{working_hours} минут</b>\n'
                             f'<b>Метод:</b> Excel',
                             parse_mode='HTML', reply_markup=cl_kb.main_menu)
        start_write_excel = Thread(target=insert_to_excel, args=(data['count_pages'], data['category'], message.from_user.id))
        start_write_excel.start()
        collapse_sticker = await bot.send_sticker(message.from_user.id, 'CAACAgIAAxkBAAIHvGLD7IfmXUxoiO9RnLPhOSSZy1f2AAIjAAMoD2oUJ1El54wgpAYpBA')
        await state.finish()
        time_work = (int(data['count_pages']) * 100)
        for i in range(time_work):
            print(start_write_excel.is_alive())
            if start_write_excel.is_alive():
                await asyncio.sleep(0.5)
            else:
                await state.finish()
                await bot.delete_message(message.from_user.id, collapse_sticker.message_id)
                await message.answer(f'Парсинг по категории: <b>{data["category"]}</b>\n'
                                     f'С количеством страниц: <b>{data["count_pages"]}</b>\n'
                                     f'<b>Окончился</b> 🚀\n\n'
                                     f'Примерное время ожидания: <b>{working_hours} минут</b>\n'
                                     f'<b>Метод:</b> Excel',
                                     parse_mode='HTML', reply_markup=cl_kb.main_menu)
                await message.answer_document(open(str(Path(str(Path.cwd()), 'data', f'{message.from_user.id}.xlsx')), "rb"))
                break



async def schedule_parsing(message: types.Message):
    inst = '<b>Есть два варианта поиска данных:</b>\n' \
           '<b>1. </b><i>Поиск минимальной цены</i> - вполне понятно из названия, вы ищите минимальную цену определённого товара\n\n' \
           '<b>2. </b><i>Интервальный парсинг</i> - иначе можно назвать парсинг по времени, здесь можно задать интервал времени, в котором будет происходить парсинг' \
           ' к примеру, можно задать парсинг каждые 5 минут, задать опции поиска и ждать, когда на сайте появится нужная вам вещь,' \
           ' как только она появится вам придёт уведомление. Или же можно задать точное время, когда будет происходить парсинг'
    await message.answer(inst, reply_markup=cl_kb.time_parsing, parse_mode='HTML')



class FSMfind_min_price(StatesGroup):
    product_name = State()

async def start_find_min_price(message: types.Message):
    if not bool(await db.get_parsing_status(message.from_user.id)):
        await message.answer('Введите имя товара:', reply_markup=cl_kb.kb_remove)
        await FSMfind_min_price.product_name.set()
    else:
        await message.answer('<b>Ошибка</b>\n'
                             'Вы уже начали парсинг, дождитесь его окончания',
                             parse_mode='HTML')


async def next_find_min_price(message: types.Message, state: FSMContext):
    product_name = message.text
    start_finding = Thread(target=time_pars.find_min_price, args=(product_name, message.from_user.id))
    start_finding.start()
    await state.finish()
    collapse_sticker = await bot.send_sticker(message.from_user.id, 'CAACAgIAAxkBAAIHvGLD7IfmXUxoiO9RnLPhOSSZy1f2AAIjAAMoD2oUJ1El54wgpAYpBA')
    for i in range(1000):
        if start_finding.is_alive():
            await asyncio.sleep(0.5)
        else:
            await bot.delete_message(message.from_user.id, collapse_sticker.message_id)
            min_price = await time_pars.return_min_price()
            if min_price[0]:
                mes_text = f'<b>Товар:</b> "{product_name}"\n' \
                           f'<b>Цена:</b> {min_price[1]} ₽\n' \
                           f'<a href="{min_price[2]}">КЛИК!</a>'
                await message.answer(mes_text, reply_markup=cl_kb.main_menu, parse_mode='HTML')
                await time_pars.clear_min_price()
            else:
                await message.answer('<b>Неверное имя товара</b>\n'
                                     'Убедитесь, что имя товара набрано верно\n'
                                     'Возможно, товар отсутствует на сайте',
                                     reply_markup=cl_kb.main_menu, parse_mode='HTML')
            break



async def time_parsing(message: types.Message):
    mes_text = '<b>"В определённое время"</b>\n' \
               'Для этого способа необходимо указать:\n<i>1. Наименование товара\n2. Ценовой диапазон\n3. Время</i>\n' \
               'Каждый день в указанное время будет происходить парсинг и если будут найдены подходящие товары, вам придёт уведомление' \
               ' и ссылки на них\n\n' \
               '<b>"Интервал"</b>\n' \
               'Для этого способа необходимо указать:\n' \
               '<i>1. Интервал времени (5 минут)\n' \
               '2. Наименование товара\n' \
               '3. Ценовой диапазон</i>\n' \
               'Каждые несколько минут будет проходить анализ и при успешном поиске товаров, подпадающих под ваши предпочтения' \
               'вам будет приходить уведомление'
    await message.answer(mes_text, parse_mode='HTML', reply_markup=cl_kb.find_time_range)






class FSMcertain_time_pars(StatesGroup):
    product_name = State()
    price = State()
    time = State()

async def certain_time_pars(message: types.Message):
    status = await db.get_schedule_status(message.from_user.id)
    if status[0] == 'inactive':
        if not bool(await db.get_parsing_status(message.from_user.id)):
            await message.answer('Введите название продукта:', reply_markup=cl_kb.kb_remove)
            await FSMcertain_time_pars.product_name.set()
        else:
            await message.answer('Вы уже начали парсинг, дождитесь его окончания')
    else:
        await message.answer('Вы уже запланировали парсинг, отмените или дождитесь его кончания')

async def cert_time_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_name'] = message.text
    await message.answer('Введите ценовой диапазон\n'
                         '<i>Пример: 100-150</i>',
                         reply_markup=cl_kb.kb_remove, parse_mode='HTML')
    await FSMcertain_time_pars.next()

async def cert_time_time(message: types.Message, state: FSMContext):
    if '-' not in message.text:
        await message.answer('Вы неверно ввели цену', reply_markup=cl_kb.main_menu)
        await state.finish()
    else:
        try:
            int(message.text.split('-')[0])
            int(message.text.split('-')[1])
        except ValueError:
            await message.answer('Вы неверно ввели цену', reply_markup=cl_kb.main_menu)
            await state.finish()
        else:
            if len(message.text.split('-')) > 2:
                await message.answer('Вы неверно ввели цену', reply_markup=cl_kb.main_menu)
                await state.finish()
            else:
                if int(message.text.split('-')[0]) > int(message.text.split('-')[1]):
                    await message.answer('Вы неверно ввели цену', reply_markup=cl_kb.main_menu)
                    await state.finish()
                else:
                    async with state.proxy() as data:
                        data['price'] = message.text
                    await message.answer('Введите время:\n'
                                         '<i>Пример: 21:00</i>',
                                         reply_markup=cl_kb.kb_remove, parse_mode='HTML')
                    await FSMcertain_time_pars.next()



async def start_schedule_time_parsing(prod_name, price, tgid):
    await db.update_schedule_status(tgid, 'active')
    await time_pars.clear_links_time_pars()
    start_pars = Thread(target=time_pars.find_user_opt_time, args=(prod_name, price, tgid))
    start_pars.start()
    for i in range(1000):
        if start_pars.is_alive():
            await asyncio.sleep(0.5)
        else:
            links = await time_pars.return_links_time_pars()
            if links[0]:
                await bot.send_message(tgid, '<b>Вы запланировали парсинг, вот его результаты:</b>', parse_mode='HTML')
                for link in links:
                    await bot.send_message(tgid, f'Найден подходящий товар: <b><a href="{link}">ссылка</a></b>\n',
                                           parse_mode='HTML', reply_markup=cl_kb.main_menu)
            else:
                await bot.send_message(tgid, '<b>Вы запланировали парсинг, вот его результаты:</b>\n'
                                             'Подходящих товаров не найдено',
                                       reply_markup=cl_kb.main_menu, parse_mode='HTML')
            break


async def cert_time_pars_finish(message: types.Message, state: FSMContext):
    if ':' not in message.text:
        await message.answer('Вы неверно ввели время', reply_markup=cl_kb.main_menu)
        await state.finish()
    else:
        try:
            int(message.text.split(':')[0])
            int(message.text.split(':')[1])
        except ValueError:
            await message.answer('Вы неверно ввели время', reply_markup=cl_kb.main_menu)
            await state.finish()
        else:
            if len(message.text.split(':')) > 2:
                await message.answer('Вы неверно ввели время', reply_markup=cl_kb.main_menu)
                await state.finish()
            else:
                if (len(message.text.split(':')[0]) < 2 or len(message.text.split(':')[0]) > 2) or (len(message.text.split(':')[0]) < 2 or len(message.text.split(':')[1]) > 2):
                    await message.answer('Вы неверно ввели время', reply_markup=cl_kb.main_menu)
                    await state.finish()
                else:
                    if ((int(message.text.split(':')[0]) > 23) or (int(message.text.split(':')[1]) > 59)) or ((int(message.text.split(':')[0]) < 0) or (int(message.text.split(':')[1]) < 0)):
                        await message.answer('Вы неверно ввели время', reply_markup=cl_kb.main_menu)
                        await state.finish()
                    else:

                        async with state.proxy() as data:
                            data['time'] = message.text
                        hour = data['time'].split(':')
                        scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
                        scheduler.add_job(start_schedule_time_parsing, args=(data['product_name'], data['price'], message.from_user.id),
                                          trigger='cron', hour=int(hour[0]), minute=int(hour[1]))
                        scheduler.start()



                        await message.answer('<b>Анализ начался</b>\n'
                                             'Мы вам сообщим если найдётся нужный вам товар',
                                             reply_markup=cl_kb.main_menu, parse_mode='HTML')

                        await state.finish()





class FSMinterval_time_pars(StatesGroup):
    product_name = State()
    price = State()
    interval = State()


async def interval_time_pars(message: types.Message):
    status = await db.get_schedule_status(message.from_user.id)
    if status[0] == 'inactive':
        if not bool(await db.get_parsing_status(message.from_user.id)):
            await message.answer('Введите название продукта:', reply_markup=cl_kb.kb_remove)
            await FSMinterval_time_pars.product_name.set()
        else:
            await message.answer('Вы уже начали парсинг, дождитесь его окончания')
    else:
        await message.answer('Вы уже запланировали парсинг, отмените его')


async def interval_time_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_name'] = message.text
    await message.answer('Введите ценовой диапазон\n'
                         '<i>Пример: 100-150</i>',
                         reply_markup=cl_kb.kb_remove, parse_mode='HTML')
    await FSMinterval_time_pars.next()


async def interval_time_parsing(message: types.Message, state: FSMContext):
    if '-' not in message.text:
        await message.answer('Вы неверно ввели цену', reply_markup=cl_kb.main_menu)
        await state.finish()
    else:
        try:
            int(message.text.split('-')[0])
            int(message.text.split('-')[1])
        except ValueError:
            await message.answer('Вы неверно ввели цену', reply_markup=cl_kb.main_menu)
            await state.finish()
        else:
            if len(message.text.split('-')) > 2:
                await message.answer('Вы неверно ввели цену', reply_markup=cl_kb.main_menu)
                await state.finish()
            else:
                if int(message.text.split('-')[0]) > int(message.text.split('-')[1]):
                    await message.answer('Вы неверно ввели цену', reply_markup=cl_kb.main_menu)
                    await state.finish()
                else:
                    async with state.proxy() as data:
                        data['price'] = message.text
                    await message.answer('Введите интервал времени в минутах:\n'
                                         '<i>Каждые 5 минут будет происходить парсинг</i>'
                                         'Пример: <i>5</i>',
                                         reply_markup=cl_kb.kb_remove, parse_mode='HTML')
                    await FSMinterval_time_pars.next()



async def interval_pars_finish(message: types.Message, state: FSMContext):
    try:
        int(message.text)
    except ValueError:
        await message.answer('Введите целое число')
    else:
        if len(message.text) > 2:
            await message.answer('Введите целое число')
        else:
            if (int(message.text) > 60) or (int(message.text) <= 0):
                await message.answer('Введите целое число в минутах')
            else:
                async with state.proxy() as data:
                    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
                    scheduler.add_job(start_schedule_time_parsing,
                                      args=(data['product_name'], data['price'], message.from_user.id),
                                      trigger='interval', minutes=int(message.text))
                    scheduler.start()
                    await message.answer('<b>Анализ начался</b>\n'
                                         'Мы вам сообщим если найдётся нужный вам товар',
                                         reply_markup=cl_kb.main_menu, parse_mode='HTML')
                await state.finish()



async def cancel_schedule_parsing(message: types.Message):
    status = await db.get_schedule_status(message.from_user.id)
    if status[0] == 'active':
        await db.update_schedule_status(message.from_user.id, 'inactive')
        await message.answer('Парсинг успешно отменён')
    else:
        await message.answer('У вас нет запущенного парсинга')










#REGISTRATION
def register_handlers_clients(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'], chat_type='private')
    dp.register_message_handler(help, Text(equals='Помощь 🔎'), chat_type='private')
    dp.register_message_handler(set_table, Text(contains='/set_table'), chat_type='private')
    dp.register_message_handler(menu, Text(equals='Меню 💤'), chat_type='private', state='*')
    dp.register_message_handler(delete_spreadsheet, Text(equals='Удалить таблицу ❌'), chat_type='private')

    # Start parsing
    dp.register_message_handler(start_parsing, Text(equals='Начать парсинг 🚀'), chat_type='private', state=None)
    dp.register_message_handler(choice_category, state=FSMstart_parsing.category)
    dp.register_message_handler(choice_count_pages, state=FSMstart_parsing.count_pages)

    # Parsing to Google sheet
    dp.register_message_handler(pars_google_sheet, Text(equals='Google sheet'), chat_type='private', state=FSMstart_parsing.choice)
    dp.register_message_handler(pars_excel, Text(equals='Excel'), chat_type='private', state=FSMstart_parsing.choice)

    # Schedule pars
    dp.register_message_handler(schedule_parsing, Text(equals='Запланировать парсинг 🕛'), chat_type='private')

    # Finding minimum price
    dp.register_message_handler(start_find_min_price, Text(equals='Поиск минимальной цены'), chat_type='private', state=None)
    dp.register_message_handler(next_find_min_price, chat_type='private', state=FSMfind_min_price.product_name)

    # Time parsing
    dp.register_message_handler(time_parsing, Text(equals='Интервальный парсинг'), chat_type='private')
    dp.register_message_handler(certain_time_pars, Text(equals='В определённое время'), chat_type='private', state=None)
    dp.register_message_handler(cert_time_price, chat_type='private', state=FSMcertain_time_pars.product_name)
    dp.register_message_handler(cert_time_time, chat_type='private', state=FSMcertain_time_pars.price)
    dp.register_message_handler(cert_time_pars_finish, chat_type='private', state=FSMcertain_time_pars.time)

    # Interval parsing
    dp.register_message_handler(interval_time_pars, Text(equals='Интервал'), chat_type='private', state=None)
    dp.register_message_handler(interval_time_price, chat_type='private', state=FSMinterval_time_pars.product_name)
    dp.register_message_handler(interval_time_parsing, chat_type='private', state=FSMinterval_time_pars.price)
    dp.register_message_handler(interval_pars_finish, chat_type='private', state=FSMinterval_time_pars.interval)
    dp.register_message_handler(cancel_schedule_parsing, Text(equals='Отменить парсинг'), chat_type='private')


