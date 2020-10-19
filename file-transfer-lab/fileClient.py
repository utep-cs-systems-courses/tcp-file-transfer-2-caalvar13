#! /usr/bin/env python3

# Echo client program
import socket, sys, re
import os.path
from os import path
from os.path import exists 
sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

s = socket.socket(addrFamily, socktype)

if s is None:
    print('could not open socket')
    sys.exit(1)

s.connect(addrPort)

file_name = input("Choose a file \n")
if exists(file_name):
    file = open(file_name, 'rb')
    payload = file.read()
    if len(payload) == 0:
        print("Can not send an empty file ")
        sys.exit(0)
    else:
        new_file_name = input("Input a new file name \n")
        framedSend(s, new_file_name.encode(), debug)
        file_exists = framedReceive(s,debug)
        file_exists = file_exists.decode()
        if file_exists == 'True':
            print("This file already exists \n")
            sys.exit(0)
        else:
            try:
                framedSend(s, payload,debug)
            except:
                print("Connection lost while sending data \n")
                sys.exit(0)
            try:
                framedReceive(s,debug)
            except:
                print("Connection lost while recieving data \n")
                sys.exit(0)
else:
    print("File does not exist")
    sys.exit(0)