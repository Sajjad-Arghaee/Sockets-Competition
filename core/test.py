import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 13000))
print('listening on port:', sock.getsockname()[1])
sock.close()