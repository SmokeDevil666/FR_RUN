from handlers.BOT_Settings import *

from in_app import *
from out import *

dp = Dispatcher(CTS.BOT, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

if not os.path.exists("c:/Face_recognition/BOT_DB"):
    os.mkdir("c:/Face_recognition/BOT_DB")

conn = sqlite3.connect("c:/Face_recognition/BOT_DB/bot_db.db")
cur = conn.cursor()


class Form(StatesGroup):
    start = State()


@dp.message_handler(CommandStart(), ChatTypeFilter(chat_type=types.ChatType.PRIVATE))
async def cmd_weather(message: types.Message):
    info = cur.execute(f'SELECT * FROM users WHERE user_id = "{message.from_user.id}"')
    if info.fetchone() is None:
        await message.answer('🔒 Учётная запись отсутствует ')
    else:
        await Form.start.set()
        keyboard = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        buttons = ['КПП', 'СТОЛОВАЯ']
        keyboard.add(*buttons)
        await message.answer('Приветствую, выбери что нужно', reply_markup=keyboard)


@dp.message_handler(state=Form.start)
async def bot_start(message: types.Message):
    if message.text == 'КПП':
        buttons = [
            types.InlineKeyboardButton(text='Вход', callback_data='Вход'),
            types.InlineKeyboardButton(text='Выход', callback_data='Выход'),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        await message.answer_sticker(r'CAACAgIAAxkBAAED-pxiE205Ckr9p9iQ_b4wFEBvBfJxlwACQBUAAmWzmEiFTnaIF_RyISME')
        await message.answer('КПП!', reply_markup=keyboard)

    @dp.callback_query_handler(state=Form.start, text='Вход')
    async def send_bounce_value(call: types.CallbackQuery):
        await call.answer(text='Вход 🔓')
        await call.message.edit_reply_markup()
        # text = 'Внимание!!'
        # await get_text(text)
        await look_in()
        await call.message.edit_text('КПП!', reply_markup=keyboard)

    @dp.callback_query_handler(state=Form.start, text='Выход')
    async def send_bounce_value(call: types.CallbackQuery):
        await call.answer(text='Выход 🔒')
        await call.message.edit_reply_markup()
        # text = 'Внимание!!'
        # await get_text(text)
        await look_out()
        await call.message.edit_text('КПП!', reply_markup=keyboard)

if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp, skip_updates=True)
