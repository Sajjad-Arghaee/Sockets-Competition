import socket
import time

from pytimedinput import timedInput
import threading

HOST = '127.0.0.1'
PORT = 54122
answered = False


def timer(num):
    t = num
    while t > 0:
        minutes, secs = divmod(t, 60)
        result = '{:02d}:{:02d}'.format(minutes, secs)
        # conn1.sendall(timer.encode())
        # conn2.sendall(timer.encode())
        # conn3.sendall(timer.encode())
        print(result, end='\r') if answered else None
        time.sleep(1)
        t -= 1


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    msg = ''
    while msg != 'end':
        msg = s.recv(1024).decode()
        print(msg)
        if msg == 'end':
            break

        answered = False
        t1 = threading.Thread(target=timer, args=(5,))
        t1.start()
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
