import sys

from client import START_CHAT
from pytimedinput import timedInput
from __init_client__ import *


def finish_competition(message):
    if message == 'end':
        print('competition has been finished')
        return True
    return False


def get_answer(message):
    sys.stdout.buffer.write(message.encode("utf-8"))
    if START_CHAT or CHAT_STARTED:
        quit()
    user_text, timed_out = timedInput("type your answer >> ", timeout=45)
    if timed_out:
        answer = 'no answer'
    else:
        answer = user_text
        print('your answer was submitted.')
        print('please wait until timeout')
    return answer


def send_answer(message, answer, client):
    if message == 'send':
        if answer == '':
            answer = 'null'
        client.sendall(answer.encode())
        score_board = client.recv(1024).decode()
        print(score_board)
        print('so now take a rest for 5 seconds')
        if START_CHAT or CHAT_STARTED:
            quit()
