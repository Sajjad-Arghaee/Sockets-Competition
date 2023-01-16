import socket
from pytimedinput import timedInput

HOST = '127.0.0.1'
PORT = 54122
END_CHAT = False
CHAT_STARTED = False


def receive_handler(socket_chat: socket):
    global CHAT_STARTED
    socket_chat.listen()
    conn, addr = socket_chat.accept()
    print(f'client {addr} wants to chat')
    CHAT_STARTED = True


def send_handler(port):
    global END_CHAT
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sender_socket,\
            socket.socket(socket.AF_INET, socket.SOCK_STREAM) as host_socket:
        sender_socket.bind((HOST, port))
        receiver_port = int(input('write down receiver port number >> '))
        sender_socket.connect((HOST, receiver_port))
        host_socket.connect((HOST, PORT))
        host_socket.sendall(f'im gonna chat to {receiver_port}')
        print(f'wait for client {receiver_port} to accept')
        message = sender_socket.recv(1024).decode()
        if message == 'NACK':
            print('client refused to connect')
            print('press ctrl+c to quit')
        else:
            while not END_CHAT:
                message, timed_out = timedInput(f'to client {receiver_port}>> ', timeout=5)
                if not (timed_out or message == ''):
                    print(f'You: {message}')
                    sender_socket.sendall(message.encode())
                    host_socket.sendall(message.encode())
                sender_socket.setblocking(False)
                ready = sender_socket.select([sender_socket], [], [], 1)
                if ready[0]:
                    data = sender_socket.recv(1024).decode()
                    if data == 'END_CHAT':
                        END_CHAT = True
                    print(f'{receiver_port}: {data}'.encode())
