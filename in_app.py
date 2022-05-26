from main import *


def look_in():
    name = face_rec()
    # Голосовое приветствие
    if name == 'No name':
        text = "Лицо не распознано, пользователь неизвестен!!!"
        get_text(text)
        return
    else:
        # text_tts = 'Здравствуйте ' + name
        # get_text_tts(text_tts)
        write_db(name)
        return name


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
    print(f"{FR.RED}INFO: {FR.GREEN}Сотрудник -> {name} успешно добавлен")


def table_db():
    conn = sqlite3.connect(r'c:/Face_recognition/DB/employee.db')
    cur = conn.cursor()
    cur.execute('''SELECT STAFF.FIO, MARK.INP FROM
            STAFF INNER JOIN MARK ON STAFF.MARK=MARK.id
            WHERE MARK.INP='Вход';''')
    for i in cur.fetchall():
        print(i)
    conn.close()


if __name__ == '__main__':
    look_in()