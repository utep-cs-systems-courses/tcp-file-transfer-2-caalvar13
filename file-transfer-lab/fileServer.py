#! /usr/bin/env python3

import sys
sys.path.append("../lib")       # for params
import re, socket, params, os
from os.path import exists

from framedSock import framedSend, framedReceive

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(3)
print("listening on:", bindAddr)

while True:
    sock, addr = lsock.accept()
    print("Connected to client", addr)
    if not os.fork():
        while True:
            payload = framedReceive(sock,debug)
            if not payload:
                break
            payload = payload.decode()

            if exists(payload):
                framedSend(sock, b"True", debug)
            else:
                framedSend(sock, b"False", debug)
                
                try:
                    payload2 = framedReceive(sock, debug)
                except:
                    print("Connection with client lost will receiving file data")
                    sys.exit(0)
                    
                if not payload2:
                    break
                payload2 += b"!"
                try:
                    framedSend(sock, payload2, debug)
                except:
                    print("Connection lost with client while sending data.")
                    
                output = open(payload, 'wb')
                output.write(payload2)
                sock.close()