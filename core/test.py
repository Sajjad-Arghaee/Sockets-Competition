import socket
import select

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mysocket:
    mysocket.setblocking(False)
    ready = select.select([mysocket], [], [], 5)
    if ready[0]:
        data = mysocket.recv(1024)
