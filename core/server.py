import socket
import time
from competiton_functions import *


def chat_listener(s1: socket, msg):
    print(msg)
    CHAT_STATE[0] = 1
    while msg != 'end_chat':
        msg = s1.recv(1024).decode()
        print(msg)


def print_timer(t):
    while t > 0:
        minutes, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(minutes, secs)
        print(timer, end='\r')
        time.sleep(1)
        t -= 1


def hold_competition():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        connections = start_competition(server)
        with connections.keys():
            index = 0
            while index < len(QUESTIONS):
                t = 45
                send_question(connections, index)
                print_timer(t)
                check_answers(connections, index)
                index += 1
                show_scoreboard(connections)
                time.sleep(5)

            end_competition(connections)


if __name__ == "__main__":
    hold_competition()
