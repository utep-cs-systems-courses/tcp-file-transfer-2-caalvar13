#! /usr/bin/env python3

import sys
sys.path.append("../../lib")
import re, socket, params, os
from os.path import exists
from threading import Thread, enumerate, Lock
global filelock
filelock = Lock()
switchesVarDefaults = (
    (('-l', '--listenPort'), 'listenPort', 50001),
    (('-d', '--debug'), "debug", False),
    (('-?', '--usage'), "usage", False),
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)
activeFiles = []
from threading import Thread;
from encapFramedSock import EncapFramedSock
def FileTransferStart(filename):
    if filename in activeFiles:
        fsock.send(b"exists", debug)
    else:
        activeFiles.append(filename)
def FileTransferEnd(filename):
    activeFiles.remove(filename)
    
class Server(Thread):
    def __init__(self, sockAddr):
        Thread.__init__(self)
        self.sock, self.addr = sockAddr
        self.fsock = EncapFramedSock(sockAddr)
    def run(self):
        print("new thread handling connection from", self.addr)
        
        filename = self.fsock.receive(debug) ## GET FILENAME
        ## ACQUIRE
        filelock.acquire()
        FileTransferStart(filename)## Check if thread is using filename already
        filelock.release()
        newfile = filename.decode()
        newfile = "new"+newfile
        if exists(newfile):
            self.fsock.send(b"True",debug)
        else:
            self.fsock.send(b"False", debug)
            payload = self.fsock.receive(debug)
            if debug: print("rec'd: ",payload)

            if not payload:
                if debug: print(f"thread connected to {addr} done")
                self.fsock.close()
                return
            outfile = open(newfile,"wb")
            outfile.write(filename)
            outfile.write(payload)
            FileTransferEnd(filename) ## Thread done with file
            self.fsock.send(b"file saved to server",debug)
            ##
while True:
    sockAddr = lsock.accept()
    server = Server(sockAddr)
    server.start()