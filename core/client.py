import time
from pynput import keyboard
from chat import *
from client_functions import *

START_CHAT = False


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
    with keyboard.GlobalHotKeys({key: on_activate(key), '<ctrl>+c': finish}) as listener:
        listener.join()
        if START_CHAT:
            client.close()
            send_handler(port)
        quit()


def connect_to_server(client, chat_socket):
    chat_socket.bind((HOST, 23001))
    print(f'your chat port is ', chat_socket.getsockname()[1])
    port = int(input('write your port number >> '))
    client.bind((HOST, port))
    client.connect((HOST, PORT))
    key = client.recv(1024).decode()
    print(f'You can enter {key} key, to enter chat room')
    return key, port


def finish_competition(message):
    if message == 'end':
        print('competition has been finished')
        return True
    return False


def participate():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client, \
            socket.socket(socket.AF_INET, socket.SOCK_STREAM) as chat_socket:
        key, port = connect_to_server(client, chat_socket)
        receive_handler_thread = threading.Thread(target=receive_handler, args=(chat_socket,))
        receive_handler_thread.start()
        key_handler_thread = threading.Thread(target=key_handler, args=(client, key, port,))
        key_handler_thread.start()

        message = ''
        while message != 'end':
            message = client.recv(1024).decode()
            finish_competition(message)
            timer_thread_1 = threading.Thread(target=timer, args=(45,))
            timer_thread_1.start()
            answer = get_answer(message)
            message = client.recv(1024).decode()
            send_answer(message, answer, client)
        print('press ctrl+c to exit')


if __name__ == "__main__":
    participate()
