import socket
import threading


def test(s):
    s.bind(('127.0.0.1', 54122))
    s.listen()
    conn, addr = s.accept()
    print(f"First client connected with : {addr}")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    chat_thread = threading.Thread(target=test, args=(server,))
    chat_thread.start()
    print('still goes on')
