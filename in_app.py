from main import *


async def look_in():
    name = await face_rec()
    if name is None:
        text = "Вас плохо видно!!! Попробуйте снова!"
        await get_text(text)
    # Голосовое приветствие
    if name == 'No name':
        text = "Лицо не распознано, пользователь неизвестен!!!"
        await get_text(text)
        return
    else:
        text = 'Здравствуйте ' + name
        await get_text(text)
        write_db(name)
        cv2.destroyAllWindows()


def write_db(name):
    # Записываем в BD ВХОД СОТРУДНИКА
    conn = sqlite3.connect(r'c:/Face_recognition/DB/employee.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS MARK ( id INTEGER PRIMARY KEY
    , INP TEXT NOT NULL);''')
    cur.execute('INSERT OR REPLACE INTO MARK (id, INP) VALUES (1, "Вход");')

    cur.execute('''CREATE TABLE IF NOT EXISTS STAFF ( id INTEGER PRIMARY KEY AUTOINCREMENT
    , FIO TEXT NOT NULL
    , DATE timestamp NOT NULL
    , TIME timestamp INTEGER
    , MARK TEXT NOT NULL
    , FOREIGN KEY (MARK) REFERENCES MARK(id));''')
    # вставляем данные сотрудника
    sqlite_insert_with_name = """INSERT INTO 'STAFF'
                      ('FIO', 'DATE', 'TIME', 'MARK')
                      VALUES (?, ?, ?, "Вход");"""

    name_tuple = (name, f"{time.strftime('%Y-%m-%d')}", FR.NOW,)
    cur.execute(sqlite_insert_with_name, name_tuple)
    conn.commit()
    conn.close()
    print(f"Сотрудник -> {name} успешно добавлен")


def table_db():
    conn = sqlite3.connect(r'c:/Face_recognition/DB/employee.db')
    cur = conn.cursor()
    cur.execute('''SELECT STAFF.FIO, MARK.INP FROM
            STAFF INNER JOIN MARK ON STAFF.MARK=MARK.id
            WHERE MARK.INP='Вход';''')
    for i in cur.fetchall():
        print(i)
    conn.close()
