import json

CHAT_STARTED = False
HOST = '127.0.0.1'
PORT = None
f = open('users.json', encoding="utf8")
data = json.load(f)
client_ports = []
for item in data:
    if item['type'] == 'host':
        PORT = item['port']
f.close()
