import asyncio
import datetime
import random
import string
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, BotCommand, \
    ReplyKeyboardMarkup, KeyboardButton
from file2 import check_password
import xlwings as xw
from datetime import datetime
from xlwt import Workbook


#adfs
a = 1
bot = Bot(token='7875381627:AAFM7Oq6qqY1HLmTTa-nBR83g35V85Si-4U')
days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
wb = Workbook()
sheet1 = wb.add_sheet('запись')
dp = Dispatcher()
users = {}
log_pass = open('logs_and_passes.txt', 'r').read().split('\n')
ws = xw.Book("запись.xls").sheets['запись']
v1 = ws.range("A1:C" + str(days[datetime.datetime.now().month - 1])).value
print(v1)
logs = []
log_pass1 = []
for el in log_pass:
    log_pass1.append(el.split())
    logs.append(el.split()[0])
log_pass = log_pass1

button_1 = KeyboardButton(
    text='Регистрация'
)

button_2 = KeyboardButton(
    text='Авторизация'
)

# Создаем объект инлайн-клавиатуры
keyboard = ReplyKeyboardMarkup(keyboard=[[button_1, button_2]], resize_keyboard=True)

url_button = InlineKeyboardButton(
    text='Аккаунт в тг',
    url=''
)

url_keyboard = InlineKeyboardMarkup(inline_keyboard=[[url_button]])


@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer(text='Добро пожаловать в программу!')
    await message.answer('Выберите:\nРегистрация\nАвторизация', reply_markup=keyboard)


@dp.message(Command('help'))
async def cmd_help(message: types.Message):
    await message.answer('/start - Начало работы с ботом\n/about - информация про создателя\n/contacts - сюда надо будет'
                         ' соцсети заказчика \n/payments - номер куда деньги переводить')


@dp.message(Command('about'))
async def cmd_about(message: types.Message):
    await message.answer('Инфа про меня')


@dp.message(Command('contacts'))
async def cmd_contacts(message: types.Message):
    await message.answer('номер телефона заказчика')


@dp.message(Command('payments'))
async def cmd_payments(message: types.Message):
    await message.answer('номер счета')


async def set_main_menu(bot: bot):
    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/start', description='Начать работу с ботом'),
        BotCommand(command='/help', description='Справка'),
        BotCommand(command='/about',  description='О программе'),
        BotCommand(command='/contacts', description='Позвонить заказчику'),
        BotCommand(command='/payments', description='Оплата за ноготочки')
    ]
    await bot.set_my_commands(main_menu_commands)


@dp.message(F.text == 'Регистрация')
async def registration(message: types.Message):
    global users
    id = message.from_user.id
    if id not in users:
        users[id] = [True, False]
    if len(users[id]) < 4:
        await message.answer('Введите, пожалуйста, логин')
    else:
        await message.answer('Вы уже авторизованы')


@dp.message(F.text == 'Авторизация')
async def autorisation(message: types.Message):
    global users
    id = message.from_user.id
    if id not in users:
        users[id] = [False, True]
    if len(users[id]) < 4:
        await message.answer('Введите, пожалуйста, логин')
    else:
        await message.answer('Вы уже авторизованы')


@dp.message()
async def work(message: types.Message):
    print(message.text)
    global users, time
    id = message.from_user.id
    if len(users[id]) == 4:
        await message.answer('Теперь выберите дату и месяц и отправьте их в формате ДД.ММ')
        users[id].append(True)
        ws = xw.Book("запись.xls").sheets['запись']
        v1 = ws.range("A1:D" + str(days[datetime.datetime.now().month - 1])).value
        a = True
        for i in range(len(v1)):
            for j in range(len(v1[i])):
                if v1[i][j] is None:
                    if j == 0:
                        await message.answer('Ближайшая свободная дата - ' + str(i + 1) + ', в 11:00')
                        a = False
                    if j == 1:
                        await message.answer('Ближайшая свободная дата - ' + str(i + 1) + ', в 14:00')
                        a = False
                    if j == 2:
                        await message.answer('Ближайшая свободная дата - ' + str(i + 1) + ', в 17:00')
                        a = False
                if not a:
                    break
            if not a:
                break
    if len(users[id]) == 5:
        a = True
        for el in message.text:
            if el not in nums and el != '.':
                a = False
        if not a:
            await message.answer('Мы не смогли распознать вашу дату')
        if a:
            if int(message.text.split('.')[0]) > days[datetime.datetime.now().month - 1]:
                a = False
                await message.answer('Мы не смогли распознать вашу дату')
            if int(message.text.split('.')[1]) > 12:
                a = False
                await message.answer('Мы не смогли распознать вашу дату')
            msg = message.text.split('.')
            b, c = msg[0], msg[1]
            cur_dt = datetime.now()
            date1 = datetime.strptime(cur_dt.year + '-' + cur_dt.month + '-' + cur_dt.day, '%Y-%m-%d')
            date2 = datetime.strptime(cur_dt.year + '-' + c + '-' + b, '%Y-%m-%d')
            if date1 > date2:
                a = False
                await message.answer('Введенная вами дата раньше нынешней даты!')
        if a:
            ws = xw.Book("запись.xls").sheets['запись']
            v1 = ws.range("A1:D" + str(days[datetime.datetime.now().month - 1])).value
            date = 0
            for i in range(len(v1)):
                for el in i:
                    if el is None and b - 1 == i:
                        await message.answer('Данная дата свободна')
                        date = b
            if date == b:
                await message.answer('Свободное время:')
                time = []
                for i in range(len(v1[date - 1])):
                    if v1[date - 1][i] is None:
                        if i == 0:
                            await message.answer('11:00')
                            time.append('11:00')
                        if i == 1:
                            await message.answer('14:00')
                            time.append('14:00')
                        if i == 2:
                            await message.answer('17:00')
                            time.append('17:00')
                await message.answer('Выберите нужное время, написав его')
                users[id].append(date)
            else:
                await message.answer('Данная дата занята')
    if len(users[id]) == 6:
        if message.text not in time:
            await message.answer('Вы не можете выбрать данное время')
        else:
            if message.text == '11:00':

            if message.text == '14:00':

            if message.text == '17:00':
    else:
        if id not in users:
            await message.answer('Простите, но вы еще не авторизованы')
        else:
            if len(users[id]) < 4:
                print(users[id])
                if users[id][0] and not users[id][1]:
                    users[id].append(message.text)
                    await message.answer('Теперь введите пароль')
                    users[id][1] = True
                    logs.append(message.text)
                    users[id][1], users[id][0] = True, True
                elif users[id][1] and users[id][0]:
                    if not await check_password(message.text):
                        await message.answer('Пароль недостаточно надежный')
                    else:
                        users[id].append(message.text)
                        log_pass.append((users[id][2] + ' ' + message.text).split())
                        await message.answer('Вы успешно зарегистрировались!')
                        file = open('logs_and_passes.txt', 'w')
                        file.write(users[id][2] + ' ' + message.text + '\n')
                elif not users[id][0] and users[id][1]:
                    if message.text not in logs:
                        await message.answer('Такой логин не обнаружен')
                    else:
                        users[id].append(message.text)
                        await message.answer('Теперь введите пароль')
                        users[id][1], users[id][0] = False, False
                elif not users[id][1] and not users[id][0]:
                    if [users[id][2], message.text] not in log_pass:
                        await message.answer('Пароль неверный')
                    else:
                        users[id].append(message.text)
                        await message.answer('Вы успешно авторизовались')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    dp.startup.register(set_main_menu)
    asyncio.run(main())