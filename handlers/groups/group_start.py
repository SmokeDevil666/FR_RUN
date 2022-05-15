from handlers.groups.BOT_Settings import *
from TG_BOT import dp

CTS.CUR.execute('CREATE TABLE IF NOT EXISTS USERS(USER_ID INTEGER, USERNAME TEXT)')


@dp.message_handler(CommandStart(), ChatTypeFilter(chat_type=types.ChatType.SUPERGROUP))
async def bot_start(message: types.Message):
    await message.answer(f'{message.from_user.full_name} Приветствую тебя, в нашей группе!\n'
                         f'🔓 Теперь тебе открыт доступ к боту')
    info = CTS.CUR.execute(f'SELECT * FROM USERS WHERE USER_ID = "{message.from_user.id}"')
    if info.fetchone() is None:
        try:
            CTS.CUR.execute(f'INSERT INTO USERS VALUES("{message.from_user.id}", "@{message.from_user.username}")')
        except Exception as e:
            print(e)
        return CTS.CONN


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.SUPERGROUP), commands='registration')
async def bot_registration(message: types.Message):
    await message.answer(f'{message.from_user.full_name} Приветствую тебя, в нашей группе!\n'
                         f'🔓 Теперь тебе открыт доступ к боту')
    info = CTS.CUR.execute(f'SELECT * FROM USERS WHERE USER_ID = "{message.from_user.id}"')
    if info.fetchone() is None:
        try:
            CTS.CUR.execute(f'INSERT INTO USERS (USER_ID, USERNAME)VALUES("{message.from_user.id}", "@{message.from_user.username}")')
            CTS.CONN.commit()
            # CTS.CONN.close()
        except Exception as e:
            print(e)
        return CTS.CONN


