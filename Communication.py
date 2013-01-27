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

    def __init__(self, addr):
        '''
        Constructor
        '''
        self.addr = addr
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
        
    def connect(self):
        self.socket.connect(self.addr)
        
    def listen(self):
        self.socket.bind(self.addr)
        self.socket.listen(2)
        
    def accept(self):
        conn, addr =  self.socket.accept()
        return Handler(conn, addr)
        
        
    def send(self, msg):
        self.socket.send(msg)
        
    def receive(self, size):
        return self.socket.recv(size)
    
    def close(self):
        self.socket.close()
        
class Handler(object):
    def __init__(self, socket, addr):
        self.sock = socket
        self.addr = addr
    
    def receive(self):
        return self.sock.recv(1024)
    
    def send(self, msg):
        self.sock.send(msg)
#        msg = self.sock.recv(1024)
#        print "RECV:", msg
#        self.sock.send(msg+ " - Echo")
    
    
        
        
if __name__ == "__main__":
    if len(sys.argv) > 1: 
        if sys.argv[1] == "-c":
            print "comes here"
            client = Communication(("localhost", 60000))
            client.connect()
            client.send("Hello Server")
            print client.receive(1024)
            client.close()
    
    else:
        server = Communication(("0.0.0.0", 60000))
    
        server.listen()
    
        server.accept()
        
        server.close()
    
    
    
        
        
        