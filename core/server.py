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


def chat_listener(s1: socket, msg):
    global CHAT_STATE
    print(msg)
    CHAT_STATE[0] = 1
    while msg != 'end_chat':
        msg = s1.recv(1024).decode()
        print(msg)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
    conn1, addr1 = server.accept()
    print(f"First client connected with : {addr1}")
    conn1.sendall(chat_keys.pop().encode())
    conn2, addr2 = server.accept()
    print(f"First client connected with : {addr2}")
    conn2.sendall(chat_keys.pop().encode())
    with conn1, conn2:
        index = 0
        while index < len(questions):
            t = 45
            if not CHAT_STATE[0]:
                conn1.sendall(questions[index].encode())
            if not CHAT_STATE[1]:
                conn2.sendall(questions[index].encode())

            while t > 0:
                minutes, secs = divmod(t, 60)
                timer = '{:02d}:{:02d}'.format(minutes, secs)
                print(timer, end='\r')
                time.sleep(1)
                t -= 1

            conn1.sendall('send'.encode())
            if not CHAT_STATE[0]:
                answer1 = conn1.recv(1024).decode()
                if 'chat' in answer1:
                    chat_thread = threading.Thread(target=chat_listener, args=(conn1, answer1))
                    chat_thread.start()
                elif answer1 == answers[index]:
                    scores[0] += 1
            conn2.sendall('send'.encode())
            if not CHAT_STATE[1]:
                answer2 = conn2.recv(1024).decode()
                if 'chat' in answer2:
                    chat_thread = threading.Thread(target=chat_listener, args=(conn2, answer2))
                    chat_thread.start()
                elif answer2 == answers[index]:
                    scores[1] += 1

            index += 1

            scoreboard = f'player1 : {scores[0]}, player2 : {scores[1]}, player3 : {scores[2]}'
            print(scoreboard)
            if not CHAT_STATE[0]:
                conn1.sendall(scoreboard.encode())
            if not CHAT_STATE[1]:
                conn2.sendall(scoreboard.encode())

            time.sleep(5)
        conn1.sendall("end".encode())
        conn2.sendall("end".encode())
