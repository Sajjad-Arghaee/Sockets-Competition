import time
from pynput import keyboard
from chat import *

HOST = '127.0.0.1'
PORT = 54122
answered = False
state = False  # False is competition mode and True is chat mode


def timer(num):
    global answered
    global state
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


def on_activate():
    global state
    print(f'{key} pressed')
    state = True
    quit()


def finish():
    print('QUIT Competition')
    quit()


def key_handler(s1: socket):
    global state
    with keyboard.GlobalHotKeys({key: on_activate, '<ctrl>+c': finish}) as listener:
        listener.join()
        if state:
            send_handler(s1)
        quit()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    port = int(input('write your port number >> '))
    s.bind((HOST, port))
    s.connect((HOST, PORT))
    key = s.recv(1024).decode()
    print(f'You can enter {key} key, to enter chat room')
    thread = threading.Thread(target=key_handler, args=(s,))
    thread.start()

    msg = ''
    while msg != 'end':
        msg = s.recv(1024).decode()
        if msg == 'end':
            print('competition has been finished')
            break
        print(msg)

        answered = False
        t1 = threading.Thread(target=timer, args=(5,))
        t1.start()
        if state:
            quit()
        user_text, timed_out = timedInput("type your answer >> ", timeout=5)
        if timed_out:
            answer = 'no answer'
        else:
            answered = True
            answer = user_text
            print('your answer was submitted.')
            print('please wait until timeout')

        msg = s.recv(1024).decode()
        if msg == 'send':
            if answer == '':
                answer = 'null'
            s.sendall(answer.encode())
            score_board = s.recv(1024).decode()
            print(score_board)
            print('so now take a rest for 5 seconds')
            t1 = threading.Thread(target=timer, args=(5,))
            t1.start()
            if state:
                quit()
    print('press ctrl+c to exit')
