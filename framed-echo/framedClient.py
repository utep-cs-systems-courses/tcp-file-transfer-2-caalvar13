#! /usr/bin/env python3

# Echo client program
import socket, sys, re

sys.path.append("../lib")       # for params
import params

from encapFramedSock import EncapFramedSock


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

sock = socket.socket(addrFamily, socktype)

if sock is None:
    print('could not open socket')
    sys.exit(1)

sock.connect(addrPort)

fsock = EncapFramedSock((sock, addrPort))

for i in range(2):
    print("sending hello world")
    fsock.send( b"hello world", debug)
    print("received:", fsock.receive(debug))