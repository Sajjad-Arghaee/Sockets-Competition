import socket
import time
from pynput import keyboard
from pytimedinput import timedInput
import threading

HOST = '127.0.0.1'
PORT = 54122
answered = False
state = False  # False is competition mode and True is chat mode


def timer(num):
    t = num
    while t > 0 and not state:
        minutes, secs = divmod(t, 60)
        result = '{:02d}:{:02d}'.format(minutes, secs)
        # conn1.sendall(timer.encode())
        # conn2.sendall(timer.encode())
        # conn3.sendall(timer.encode())
        print(result, end='\r') if answered else None
        time.sleep(1)
        t -= 1


def chat_handler():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s1, \
            socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
        s1.bind((HOST, 13000))
        s2.bind((HOST, 13001))
        receiver = input('write down receiver port number >> ')
        s1.connect((HOST, PORT))
        s2.connect((HOST, receiver))

    def on_activate():
        print(f'{key} pressed')
        quit()

    def finish():
        print('QUIT Competition')
        quit()

    def key_handler():
        with keyboard.GlobalHotKeys({key: on_activate, '<ctrl>+c': finish}) as listener:
            listener.join()
            state = True
            chat_handler()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, 13000))
        s.connect((HOST, PORT))
        key = s.recv(1024).decode()
        print(f'You can enter {key} key, to enter chat room')
        thread = threading.Thread(target=key_handler)
        thread.start()

        msg = ''
        while msg != 'end':
            msg = s.recv(1024).decode()
            print(msg)
            if msg == 'end':
                break

            answered = False
            t1 = threading.Thread(target=timer, args=(5,))
            t1.start()
            if state:
                quit()
            userText, timedOut = timedInput("type your answer >> ", timeout=5)
            if timedOut:
                answer = 'no answer'
            else:
                answered = True
                answer = userText
                print('your answer was submitted.')
                print('please wait until timeout')

            msg = s.recv(1024).decode()
            if msg == 'send':
                s.sendall(answer.encode())
                score_board = s.recv(1024).decode()
                print(score_board)
                print('so now take a rest for 5 seconds')
                t1 = threading.Thread(target=timer, args=(5,))
                t1.start()
                if state:
                    quit()
        print('press ctrl+c to exit')
