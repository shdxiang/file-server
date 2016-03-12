#!/usr/bin/env python

import time
import sys
import os
import json
import socket 
import logging
import argparse
import struct
import SocketServer  
from SocketServer import StreamRequestHandler as SRH  
from time import ctime  
  
logger = logging.getLogger('server')
#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s',
                )
  
class Servers(SRH):  
    def handle(self):  
        logger.debug('got connection from: %s' ,self.client_address)
        while True:  
            try:
                #data = self.request.recv(2)  
                data = self.rfile.read(2)  
                print len(data)
                name_len, = struct.unpack('>H', data)
                logger.debug('name len: %d', name_len)

                name = self.request.recv(name_len)  
                logger.debug('name: %s', name)

                data = self.request.recv(4)  
                content_len, = struct.unpack('>I', data)
                logger.debug('content len: %d', content_len)

                content = self.request.recv(content_len)  

                path = '/tmp/' + name
                fo = open(path, 'wb')
                fo.write(content)
                fo.close()

                logger.debug("send ack")
                data = struct.pack('>H', 0x03)
                #self.request.send(data) 
                self.wfile.write(data) 
            except Exception as e:
                logger.debug(e)
                break
class myThreadingTCPServer(SocketServer.ThreadingTCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)
        self.server_address = self.socket.getsockname()

def main():

    parser = argparse.ArgumentParser(description='server')
    parser.add_argument('--port', '-p', type=int, help='port(0909)', default=9999)
    args = parser.parse_args()


    host = '0.0.0.0'  
    addr = (host, args.port)  
    server = myThreadingTCPServer(addr, Servers)  
    try:
        logger.debug('starting...')
        server.serve_forever()  
    except KeyboardInterrupt as e:
        logger.debug('shutdown...')
        server.shutdown()
        server.server_close() 
        logger.debug('bye')
        os._exit(0)

if __name__ == '__main__':
    main()

