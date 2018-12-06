"""
Dalton Gray
CS 494
11/10/18
IRC Project

This file contains the client side implementation
of the IRC application.
"""

import sys
import socket
import select
import string

if len(sys.argv) != 4:
    print "USAGE: irc_c.py <HOST> <PORT>, <SCREENNAME>";
    sys.exit(0)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = sys.argv[1]      #Host name.
port = int(sys.argv[2]) #Port number.
sn = sys.argv[3]        #Screenname

try:
    s.connect((host, port))
except:
    print 'Connection to server not established'
    sys.exit()

print 'Connection Established'
try:
    s.send(sn)
except:
    print 'Username not accepted'
    sys.exit()

while(1):
    connect = [s, sys.stdin]

    inputready, outputready, exceptready = select.select(connect, [], [])

    for i in inputready:
        if i == s:
            data = s.recv(1024)
            if not data:
                print 'Connection lost.'
                sys.exit()
            else:
                print data + '\n'
        else:
            message = sys.stdin.readline()
            s.send(message)

