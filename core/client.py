import threading
import time
from pynput import keyboard
from chat import *
from client_functions import *
import __init_client__

START_CHAT = False
ANSWERED = False


def timer(num):
    t = num
    while t > 0 and not START_CHAT:
        minutes, secs = divmod(t, 60)
        result = '{:02d}:{:02d}'.format(minutes, secs)
        print(result, end='\r') if ANSWERED else None
        time.sleep(1)
        t -= 1


def on_activate(key):
    global START_CHAT
    print(f'{key} pressed')
    START_CHAT = True
    quit()


def finish():
    print('QUIT Competition')
    quit()


def key_handler(client, key, port):
    global START_CHAT
    with keyboard.GlobalHotKeys({key: on_activate, '<ctrl>+c': finish}) as listener:
        listener.join()
        if START_CHAT:
            client.close()
            send_handler(port)
        quit()


def connect_to_server(client):
    f = open('sample.json', encoding="utf8")
    data = json.load(f)
    port = data[0]
    f.close()
    json_object = json.dumps(data[1:])
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)
    print(port)
    client.bind((HOST, port))
    client.connect((HOST, __init_client__.PORT))
    key = client.recv(1024).decode()
    print(f'You can enter {key} key, to enter chat room')
    return key, port


def finish_competition(message):
    if message == 'end':
        print('competition has been finished')
        return True
    return False


def participate():
    global ANSWERED
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        key, port = connect_to_server(client)
        key_handler_thread = threading.Thread(target=key_handler, args=(client, key, port,))
        key_handler_thread.start()

        message = ''
        while message != 'end':
            ANSWERED = False
            message = client.recv(1024).decode()
            if finish_competition(message):
                break
            timer_thread_1 = threading.Thread(target=timer, args=(45,))
            timer_thread_1.start()
            answer = get_answer(message)
            ANSWERED = True
            message = client.recv(1024).decode()
            send_answer(message, answer, client)
            timer_thread_2 = threading.Thread(target=timer, args=(5,))
            timer_thread_2.start()
            timer_thread_2.join()
        print('press ctrl+c to exit')


if __name__ == "__main__":
    participate()
