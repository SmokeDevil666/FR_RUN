import sqlite3
from colorama import init, Fore
import os
import time
import pickle

from transliterate import translit
import torch
import sounddevice as sd
import time
import pyttsx3 as pytt
import face_recognition
import asyncio
import cv2

init(autoreset=True)


class FR(object):
    # colorama
    RED = Fore.RED
    BLUE = Fore.BLUE
    GREEN = Fore.GREEN
    ##################
    PATHNAME = time.strftime('%Y-%m-%d')
    NOW = time.strftime('%H:%M')
    FULL_PATHNAME = f'c:/Face_recognition/skrin/{PATHNAME}'
    if not os.path.exists('c:/Face_recognition/skrin'):
        os.mkdir('c:/Face_recognition/skrin')
    if not os.path.exists(f'{FULL_PATHNAME}'):
        os.mkdir(f'{FULL_PATHNAME}')
    if not os.path.exists(r'c:/Face_recognition/DB'):
        os.mkdir(r'c:/Face_recognition/DB')
    if not os.path.exists("c:/Face_recognition/BOT_DB"):
        os.mkdir("c:/Face_recognition/BOT_DB")
    CASCADE_PATH_FACE = 'haarcascade_frontalface_default.xml'
    FACE_DETECTOR = cv2.CascadeClassifier(CASCADE_PATH_FACE)
    DATA = pickle.loads(open('c:/Face_recognition/face_enc', "rb").read())
    # Запись в файл ip android device
    file = "c:/Face_recognition/IP_WEBCAM.txt"
    open(file, "a").close()
    with open("c:/Face_recognition/IP_WEBCAM.txt") as f:
        IP_WEBCAM = f.readline()
        print(f'IP_WEBCAM : {GREEN} *** {IP_WEBCAM} ***')
        if not IP_WEBCAM:
            print(f'{RED}***Внимание***\n'
                  f'{BLUE}Скачайте с Google play приложение {GREEN}=> {RED}ip_webcam\n'
                  f'{BLUE}Установите и настройте приложение, установите нужную ориентацию устройства\n'
                  f'Сделать вы это можете так: Введите ip address устройства в браузере, раскройте пункт\n'
                  f'{RED}Дополнительные настройки {GREEN}=> {RED}Ориентация\n\n')
            ip_webcam = input(f'{BLUE}Введите  ip address android device{GREEN}: ')
            with open(file, 'w') as file:
                file.write(ip_webcam)
                file.close()
                IP_WEBCAM = f.readline()


async def output(sleep, text):  # Создаём отдельный поток для цикла while
    await asyncio.sleep(sleep)
    print(text)


async def face_rec():
    count_for_foto = 0
    # TODO for i in range(10):
    #     cam = cv2.VideoCapture(i)
    #     if cam:
    #         break
    while True:
        await output(00000.1, f"{FR.RED}INFO: Поиск Лица")  # Притормаживаем наш шустрый цикл. (:
        cam = cv2.VideoCapture(f'http://{FR.IP_WEBCAM}:8080/video')
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = FR.FACE_DETECTOR.detectMultiScale(gray
                                                  , scaleFactor=1.1
                                                  , minNeighbors=5
                                                  , minSize=(60, 60)
                                                  , flags=cv2.CASCADE_SCALE_IMAGE)
        # Преобразовать входной кадр из BGR в RGB
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Накладываем лица для лица во входном кадре
        encodings = face_recognition.face_encodings(rgb)
        names = []
        # Цикл накладывания лиц
        for encoding in encodings:
            # Сравниваем кодировки с кодировками в data['encodings']
            # Совпадения содержат массив с буливыми значениями True для наложения
            # и False для остальных соответственно
            matches = face_recognition.compare_faces(FR.DATA["encodings"], encoding)
            # Устанавливаем name = в -> unknown если ни одна кодировка не совпадает
            name = "No name"
            # проверка на совпадения
            if True in matches:
                # Находим позиции в True и сохраняем
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                # Цикл по совпавшим индексам и ведение счёта для
                # Каждого распознанного лица
                for i in matchedIdxs:
                    # Проверяем имена в соответствующих индексов которые мы нашли
                    name = FR.DATA["names"][i]
                    # Увеличиваем кол - во для имени которое нашли
                    counts[name] = counts.get(name, 0) + 1
                # Устанавливаем имя с наибольшим кол - вом
                name = max(counts, key=counts.get)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                count_for_foto += 1
                # Сохраняем лицо
                cv2.imwrite(f'{FR.FULL_PATHNAME}/user.' + str(name) + str(count_for_foto) + '.jpg', gray)
            # TODO: cv2.imshow('image', img)  <<< ################################ Вывод изображения
            k = cv2.waitKey(1) & 0xff  # 'ESC'
            if k == 1:
                break
            if count_for_foto >= 1:
                break
        try:
            return name
        except NameError:
            continue


async def get_text(text):
    language = 'ru'
    model_id = 'ru_v3'
    sample_rate = 48000
    speaker = 'baya'
    put_accent = True
    put_yo = True
    device = torch.device('cpu')
    model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                              model='silero_tts',
                              language=language,
                              speaker=model_id)
    model.to(device)

    audio = model.apply_tts(text=text,
                            speaker=speaker,
                            sample_rate=sample_rate,
                            put_accent=put_accent,
                            put_yo=put_yo)
    sd.play(audio, sample_rate)
    time.sleep(len(audio) / 24000)
    sd.stop()
    return text


async def get_text_tts(text_tts):
    tts = pytt.init()
    rate = tts.getProperty('rate')
    volume = tts.getProperty('volume')
    tts.setProperty('volume', volume + 10.9)
    tts.setProperty('rate', rate + 30)
    tts.say(text_tts)
    tts.runAndWait()
    return text_tts


if __name__ == '__main__':
    asyncio.run(face_rec())
