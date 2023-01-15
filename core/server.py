import socket
import time
import threading

HOST = '127.0.0.1'
PORT = 54122
CHAT_STATE = [0, 0, 0]
questions = [
    """1. what's the color of sun?
        a) red
        b) green
        c) blue
        d) combination of a,b,c
    """,
    """2. how many months we have in a year?
        a) 12 months
        b) 10 months
        c) 11 month
        d) 9 month
    """
]
answers = ['d', 'a']
scores = [0, 0, 0]
chat_keys = ['i', 'o', 'p']


def chat_listener(s1: socket):
    global CHAT_STATE
    msg = s1.recv(1024).decode()
    print(msg)
    CHAT_STATE[0] = 1
    while msg != 'end_chat':
        msg = s1.recv(1024).decode()
        print(msg)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn1, addr1 = s.accept()
    print(f"First client connected with : {addr1}")
    conn1.sendall(chat_keys.pop().encode())
    # conn2, addr2 = s.accept()
    # print(f"Second client connected with : {addr2}")
    # conn3, addr3 = s.accept()
    # print(f"Third client connected with : {addr3}")
    with conn1:
        index = 0
        while index < len(questions):
            t = 5
            conn1.sendall(questions[index].encode())
            # conn2.sendall(questions[index].encode())
            # conn3.sendall(questions[index].encode())
            thread = threading.Thread(target=chat_listener, args=(conn1,))
            thread.start()
            while t > 0:
                minutes, secs = divmod(t, 60)
                timer = '{:02d}:{:02d}'.format(minutes, secs)
                print(timer, end='\r')
                time.sleep(1)
                t -= 1

            conn1.sendall('send'.encode())
            if not CHAT_STATE[0]:
                answer1 = conn1.recv(1024)
                if answer1.decode() == answers[index]:
                    scores[0] += 1
            # conn2.sendall('send'.encode())
            # conn3.sendall('send'.encode())
            # conn2.sendall("send".encode())
            # answer2 = conn2.recv(1024)
            # if answer2.decode() == answers[index]:
            #     scores[1] += 1
            # conn3.sendall("send".encode())
            # answer3 = conn3.recv(1024)
            # if answer3.decode() == answers[index]:
            #     scores[2] += 1
            index += 1

            scoreboard = f'player1 : {scores[0]}, player2 : {scores[1]}, player3 : {scores[2]}'
            print(scoreboard)
            if not CHAT_STATE[0]:
                conn1.sendall(scoreboard.encode())
            # conn2.sendall(scoreboard.encode())
            # conn3.sendall(scoreboard.encode())
            time.sleep(5)
        conn1.sendall("end".encode())
        # conn2.sendall("end".encode())
        # conn3.sendall("end".encode())
