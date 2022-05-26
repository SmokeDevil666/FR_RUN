import pyttsx3
import select, socket, queue
from in_app import *
from out import *


def get_text_tts(text_tts):
    tts = pyttsx3.init("sapi5")
    tts.say(text_tts)
    tts.runAndWait()


srv_ip = input("Введите ip адрес сервера: ")
SERVER = srv_ip
PORT = 4444

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)
server.bind((SERVER, PORT))
print("Сервер запущен")
server.listen(5)
inputs = [server]
outputs = []
message_queues = {}

while True:
    readable, writable, exceptional = select.select(inputs, outputs, inputs)
    for s in readable:
        if s is server:
            connection, client_address = s.accept()
            print("Новое подключение : ", client_address)
            connection.setblocking(False)
            inputs.append(connection)
            message_queues[connection] = queue.Queue()
        else:
            data = s.recv(1024)
            msg = data.decode('utf-8')
            if msg == 'Вход':
                name = look_in()
                get_text_tts(msg)
                get_text_tts(name)
                connection.send(bytes(str(name), encoding='utf8'))
            elif msg == 'Выход':
                name = look_out()
                get_text_tts(name)
                get_text_tts(msg)
                connection.send(bytes(str(name), encoding='utf8'))
                print("Выход")
            if msg == '':
                print("Отключение!")
                break
            if data:
                message_queues[s].put(data)
                if s not in outputs:
                    outputs.append(s)
            else:
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                del message_queues[s]

    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
        except queue.Empty:
            outputs.remove(s)
        else:
            if s == '':
                print("Отключение!")
                s.task_done()
            s.send(next_msg)

    for s in exceptional:
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        del message_queues[s]
