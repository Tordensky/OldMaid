'''
Created on Jan 23, 2013

@author: Simon
'''
import socket
import sys


class Communication(object):
    '''
    classdocs
    '''

    def __init__(self, addr, port):
        '''
        Constructor
        '''
        self.addr = addr
        self.port = port
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self):
        self.socket.connect((self.addr, self.port))
        
    def listen(self):
        self.socket.bind((self.addr, self.port))
        self.socket.listen(2)
        
    def accept(self):
        self.socket.accept()
        print "got connection"
        
    def send(self, msg):
        self.socket.send(msg)
        
    def receive(self, size):
        return self.socket.recv(size)
    
    def close(self):
        self.socket.close()
        
        
if __name__ == "__main__":
    if len(sys.argv) > 1: 
        if sys.argv[1] == "-c":
            print "comes here"
            client = Communication("localhost", 60000)
            client.connect()
            client.send("test message")
            client.close()
    else:
        server = Communication("0.0.0.0", 60000)
    
        server.listen()
    
        server.accept()
    
        print server.receive(100)
    
        server.close()
    
    
    
        
        
        