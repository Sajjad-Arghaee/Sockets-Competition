import threading
import time
from pynput import keyboard
from chat import *

HOST = '127.0.0.1'
PORT = 54122
answered = False
START_CHAT = False  # False is competition mode and True is chat mode


def timer(num):
    global answered
    global START_CHAT
    t = num
    while t > 0 and not START_CHAT:
        minutes, secs = divmod(t, 60)
        result = '{:02d}:{:02d}'.format(minutes, secs)
        # conn1.sendall(timer.encode())
        # conn2.sendall(timer.encode())
        # conn3.sendall(timer.encode())
        print(result, end='\r') if answered else None
        time.sleep(1)
        t -= 1


def on_activate():
    global START_CHAT
    print(f'{key} pressed')
    START_CHAT = True
    quit()


def finish():
    print('QUIT Competition')
    quit()


def key_handler():
    global START_CHAT
    with keyboard.GlobalHotKeys({key: on_activate, '<ctrl>+c': finish}) as listener:
        listener.join()
        if START_CHAT:
            client.close()
            send_handler(port)
        quit()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client, \
        socket.socket(socket.AF_INET, socket.SOCK_STREAM) as chat_socket:
    chat_socket.bind((HOST, 23001))
    print(f'your chat port is ', chat_socket.getsockname()[1])
    chat_thread = threading.Thread(target=receive_handler, args=(chat_socket,))
    chat_thread.start()
    port = int(input('write your port number >> '))
    client.bind((HOST, port))
    client.connect((HOST, PORT))
    key = client.recv(1024).decode()
    print(f'You can enter {key} key, to enter chat room')
    thread = threading.Thread(target=key_handler, args=())
    thread.start()

    message = ''
    while message != 'end':
        message = client.recv(1024).decode()
        if message == 'end':
            print('competition has been finished')
            break
        print(message)

        answered = False
        timer_thread_1 = threading.Thread(target=timer, args=(45,))
        timer_thread_1.start()
        if START_CHAT or CHAT_STARTED:
            quit()
        user_text, timed_out = timedInput("type your answer >> ", timeout=45)
        if timed_out:
            answer = 'no answer'
        else:
            answered = True
            answer = user_text
            print('your answer was submitted.')
            print('please wait until timeout')

        message = client.recv(1024).decode()
        if message == 'send':
            if answer == '':
                answer = 'null'
            client.sendall(answer.encode())
            score_board = client.recv(1024).decode()
            print(score_board)
            print('so now take a rest for 5 seconds')
            timer_thread_2 = threading.Thread(target=timer, args=(5,))
            timer_thread_2.start()
            if START_CHAT or CHAT_STARTED:
                quit()
    print('press ctrl+c to exit')
