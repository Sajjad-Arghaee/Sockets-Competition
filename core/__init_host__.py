import json

QUESTIONS = []
ANSWERS = []
f = open('questions.json', encoding="utf8")
data = json.load(f)
for item in data:
    question = item['question'] + '\n'
    for i in range(4):
        question += f'{i+1}) ' + item['options'][i] + '\n'
    QUESTIONS.append(question)
    ANSWERS.append(int(item['answer']))

f.close()

HOST = '127.0.0.1'
PORT = None
f = open('users.json', encoding="utf8")
data = json.load(f)
client_ports = []
for item in data:
    if item['type'] == 'host':
        PORT = item['port']
    else:
        client_ports.append(item['port'])
f.close()

json_object = json.dumps(client_ports)
outfile = open("sample.json", "w")
outfile.write(json_object)
outfile.close()

CLIENTS_NUMBER = 3
SCORES = [0, 0, 0]
CHAT_KEYS = ['i', 'o', 'p']
