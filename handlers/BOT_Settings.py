import os
import sqlite3

from aiogram import Bot, Dispatcher, executor, types
import logging
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, ChatTypeFilter
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

# Создаём директории если их нет
if not os.path.exists("c:/Face_recognition/BOT_DB"):
    os.mkdir("c:/Face_recognition/BOT_DB")


class CTS(object):
    # Вводим токен бота
    file = "c:/Face_recognition/TOKEN.txt"
    open(file, "a").close()
    with open("c:/Face_recognition/TOKEN.txt") as f:
        TOKEN = f.readline()
        if not TOKEN:
            token = input('Введите  TOKEN: ')
            with open(file, 'w') as file:
                file.write(token)
                file.close()
                TOKEN = f.readline()
            if not token:
                exit("Ошибка!: Не найден ТОКЕН бота!\n"
                     "Запишите TOKEN в текстовый файл c:/Face_recognition/TOKEN.txt\n")
    BOT = Bot(token=TOKEN)
    ### BOT_DB ###
    CONN = sqlite3.connect("c:/Face_recognition/BOT_DB/bot_db.db")
    CUR = CONN.cursor()
