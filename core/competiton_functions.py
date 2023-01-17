import threading
import server as server_socket
from __init__ import *


def start_competition(server):
    server.bind((HOST, PORT))
    server.listen()
    new_connections = {}
    for _ in range(CLIENTS_NUMBER):
        new_conn, addr = server.accept()
        new_connections.update({new_conn: addr})
        print(f"First client connected with : {addr}")
        new_conn.sendall(CHAT_KEYS.pop().encode())
    return new_connections


def show_scoreboard(connections):
    scoreboard = ''
    for i in range(CLIENTS_NUMBER):
        scoreboard += f'player {i} : {SCORES[i]} '
    print(scoreboard)
    for i in range(CLIENTS_NUMBER):
        if not CHAT_STATE[i]:
            list(connections.keys())[i].sendall(scoreboard.encode())


def send_question(connections, index):
    for i in range(CLIENTS_NUMBER):
        if not CHAT_STATE[i]:
            list(connections.keys())[i].sendall(QUESTIONS[index].encode())


def check_answers(connections, index):
    for i in range(CLIENTS_NUMBER):
        conn = list(connections.keys())[i]
        conn.sendall('send'.encode())
        if not CHAT_STATE[i]:
            answer = conn.recv(1024).decode()
            if 'chat' in answer:
                chat_thread = threading.Thread(target=server_socket.chat_listener, args=(conn, connections.get(conn)))
                chat_thread.start()
            elif answer == ANSWERS[index]:
                SCORES[i] += 1


def end_competition(connections):
    for i in range(CLIENTS_NUMBER):
        list(connections.keys())[i].sendall("end".encode())
