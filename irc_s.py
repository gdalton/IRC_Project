"""
Dalton Gray
CS 494
IRC Project
11/10/18

This file contains the server side implementation 
of the IRC application.
"""

import sys
import socket
import select


def chat(client, message):
    if (len(users[client]['rooms']) == 0) or (users[client]['current'] == ''):
        client.send('Please join a chatroom.\n')
    else:
        for i in clients:
            if i != s and (users[i]['current'] == users[client]['current']) and i != client:
                i.send(('\n%s: ' % users[client]['sn']) + message)


def parse(client, data):
    data = data.split()

    if data[0] == 'LEAVE':
        if data[1] != '':
            LEAVE(client, data[1])
        else:
            client.send('Please specify a room.')    
    elif data[0] == 'EXIT':
        EXIT(client)
    elif data[0] == 'JOIN':
        if data[1] != '':
            JOIN(client, data[1])
        else:
            client.send('Please specify a room.')    
    elif data[0] == 'HERE':
        if data[1] != '':
            HERE(client, data[1])
        else:
            client.send('Please specify a room.')
    elif data[0] == 'LIST':
        LIST(client)
    else:
        data = ' '.join(data)
        chat(client, data)

def LEAVE(client, to_leave):
    if to_leave in users[client]['rooms']:
        if to_leave == users[client]['current']:
            users[client]['current'] = ''
        users[client]['rooms'].remove(to_leave)
        client.send('Left room.\n')
    else:
        client.send('You have not joined that room.\n')

    
def EXIT(client):
    if len(users[client]['rooms']) > 0:
        for i in rooms:
            if i in users[client]['rooms']:
                LEAVE(client, i)

    sns.remove(users[client]['sn'])
    client.close()
    clients.remove(client)

def JOIN(client, to_join):
    if to_join in rooms:
        if to_join not in users[client]['rooms']:
            users[client]['rooms'].append(to_join)
        users[client]['current'] = to_join
        client.send('Room joined!\n')
    else:
        rooms.append(to_join)
        users[client]['rooms'].append(to_join)
        users[client]['current'] = to_join
        client.send('Room created!\n')

def HERE(client, to_list):
    if to_list in rooms:
        for i in clients:
            if (i != s) and (to_list in users[i]['rooms']):
                client.send(users[i]['sn'])
    else:
        client.send('Could not find the specified room.')

def LIST(client):
    if len(rooms) != 0:
        client.send('Current Rooms on server:\n')
        for i in rooms:
            client.send('%s\n' % i)
    else:
        client.send('No rooms currently exist.')

if len(sys.argv) < 2:
    print "USAGE: irc_s.py <PORT>"
    sys.exit(0)

clients = []
rooms = []
sns = []
users = {}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
port = int(sys.argv[1])
s.bind((host, port))
s.listen(5)
run = 1

clients.append(s)

while(run):
    inputready, outputready, exceptready = select.select(clients, [], [])

    for i in inputready:
        if i == s:
            conn, addr = s.accept()
            clients.append(conn)
            users[conn] = {'sn': '', 'rooms': [], 'current': ''}
            name = conn.recv(1024)

            if name in sns:
                conn.send('\nScreenname is not available\n')
                conn.close()
                clients.remove(conn)
            else:
                users[conn]['sn'] = name
                sns.append(name)
                
        elif i == sys.stdin:
            junk = sys.stdin.readline()
            run = 0
            s.close()
            sys.exit()
        else:
            try:
                data = i.recv(1024)
                if data:
                    parse(i, data)
            except:
                EXIT(i)
                continue

conn.close()


