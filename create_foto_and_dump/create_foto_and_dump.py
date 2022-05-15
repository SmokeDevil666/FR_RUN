from imutils import paths
import face_recognition
import pickle

import cv2
import os
import pyttsx3 as pytt


if not os.path.exists('c:/Face_recognition'):
    os.mkdir('c:/Face_recognition')  # <- Если нет директории, создаём её

if not os.path.exists('c:/Face_recognition/Dataset'):
    os.mkdir('c:/Face_recognition/Dataset')  # <- Если нет директории, создаём её


class Person:
    def __init__(self, user_name, num):
        self.user_name = user_name
        self.num = num

        if not os.path.exists(f'c:/Face_recognition/Dataset/{self.user_name}'):
            os.mkdir(f'c:/Face_recognition/Dataset/{self.user_name}')   # <- Если нет директории, создаём её

        try:
            cam = cv2.VideoCapture(self.num)
            face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            # Вводим id лица которое добавляется в имя и потом будет использовать в распознавание.
            text = f"Инициализация захвата лица. {self.user_name}, Посмотрите пожалуйста в камеру и ждите …"
            tts = pytt.init()
            tts.say(text)
            tts.runAndWait()
            count = 0
            while True:
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    count += 1
                    # Сохраняем лицо
                    cv2.imwrite(f'c:/Face_recognition/Dataset/{self.user_name}/user.' + str(f'{count}') + '.' + str(count) + '.jpg',
                                gray[y:y + h, x:x + w])
                k = cv2.waitKey(100) & 0xff  # 'ESC'
                if k == 27:
                    break
                elif count >= 10:  # Если сохранили 30 изображений выход.
                    break
            file_dump = input('Создать дамп файл, лиц из Dataset? yes/no : ')
            if f'{file_dump}' == 'yes':
                # в директории dataset хранятся папки со всеми изображениями
                imagePaths = list(paths.list_images('c:/Face_recognition/Dataset'))
                knownEncodings = []
                knownNames = []
                # перебираем все папки с изображениями
                for (i, imagePath) in enumerate(imagePaths):
                    # извлекаем имя человека из названия папки
                    name = imagePath.split(os.path.sep)[-2]
                    # загружаем изображение и конвертируем его из BGR (OpenCV ordering)
                    # в dlib ordering (RGB)
                    image = cv2.imread(imagePath)
                    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    # используем библиотеку Face_recognition для обнаружения лиц
                    boxes = face_recognition.face_locations(rgb, model='hog')
                    # вычисляем эмбеддинги для каждого лица
                    encodings = face_recognition.face_encodings(rgb, boxes)
                    # loop over the encodings
                    for encoding in encodings:
                        knownEncodings.append(encoding)
                        knownNames.append(name)
                # сохраним эмбеддинги вместе с их именами в формате словаря
                data = {"encodings": knownEncodings, "names": knownNames}
                # для сохранения данных в файл используем метод pickle
                f = open("c:/Face_recognition/face_enc", "wb")
                f.write(pickle.dumps(data))
                f.close()
            else:
                print('Как скажите))')
            print("\n [INFO] Выход из программы, и отчистка ... ")
            text_out = "Спасибо за ожидание, вы мне понравились, пожалуй фотки оставлю на память"
            tts.say(text_out)
            tts.runAndWait()
            cam.release()
        except Exception as _ex:
            text = "Камера не найдена!!! Попробуйте снова "
            tts = pytt.init()
            tts.say(text)
            tts.runAndWait()


if __name__ == '__main__':
    cam_number = 0
    # cam = cv2.VideoCapture(cam_number)
    for i in range(10):
        capture = cv2.VideoCapture(i)
        if capture:
            break
    name = input('Введите имя сотрудника  ==>  ')
    pers = Person(name, cam_number)

