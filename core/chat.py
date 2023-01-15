import socket
import threading

HOST = '127.0.0.1'
PORT = 54122
END_CHAT = False


def receive_handler(receiver_client: socket, host):
    global END_CHAT
    while True:
        stream = receiver_client.recv(1024).decode()
        if stream == 'exit()':
            print('chat ended')
            host.sendall('end_chat'.encode())
            receiver_client.sendall('exit()'.encode())
            END_CHAT = True
            quit(0)
        print(stream) if stream else None


def chat_handler():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s1, \
            socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
        s1.bind((HOST, 13000))
        s2.bind((HOST, 13001))
        receiver = input('write down receiver port number >> ')
        s1.connect((HOST, PORT))
        s1.sendall(f'im gonna connect to {receiver}')
        s2.connect((HOST, receiver))
        thread = threading.Thread(target=receive_handler, args=(s2,s1))
        thread.start()
        while not END_CHAT:
            message = input(f'to client {receiver}>> ')
            print(f'You: {message}')
            s1.sendall(f'client 13000 sent "{message} to client {receiver}"'.encode())
            s2.sendall(message.encode())

