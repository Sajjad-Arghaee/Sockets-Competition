import socket
from pytimedinput import timedInput

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


def send_handler(client_socket):
    global END_CHAT
    with client_socket, socket.socket(socket.AF_INET, socket.SOCK_STREAM) as host_socket:
        receiver_port = input('write down receiver port number >> ')
        client_socket.connect((HOST, receiver_port))
        host_socket.connect((HOST, PORT))
        host_socket.sendall(f'im gonna chat to {receiver_port}')
        print(f'wait for client {receiver_port} to accept')
        message = client_socket.recv(1024).decode()
        if message == 'NACK':
            print('clinet refused to connect')
            print('press ctrl+c to quit')
        else:
            while not END_CHAT:
                message, timed_out = timedInput(f'to client {receiver_port}>> ', timeout=5)
                if not (timed_out or message == ''):
                    print(f'You: {message}')
                    client_socket.sendall(message.encode())
                    host_socket.sendall(message.encode())
                client_socket.setblocking(False)
                ready = client_socket.select([client_socket], [], [], 1)
                if ready[0]:
                    data = client_socket.recv(1024).decode()
                    if data == 'END_CHAT':
                        END_CHAT = True
                    print(f'{receiver_port}: {data}'.encode())
