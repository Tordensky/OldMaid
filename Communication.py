'''
Created on Jan 23, 2013

@author: Simon
'''
import socket, json, sys, time, thread

class Communication(object):
    '''
    classdocs
    '''

    CON_RETRIES = 3
    WAIT_SEC_BEFORE_RETRY = 0
    MSG_BUFF_SIZE = 2048
    
    def __init__(self, addr):
        '''
        Constructor
        '''
        self.addr = addr
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                
    def connect(self):
        for x in range(1, self.CON_RETRIES+1):
            try: 
                self.socket.connect(self.addr)
                break
            except:
                print "%d Try to connect to server, got exception: %s" % (x, sys.exc_info()[0])
                if x == self.CON_RETRIES:
                    raise
                time.sleep(self.WAIT_SEC_BEFORE_RETRY)
                    
    def cmd(self, cmd):
        for x in range(1, self.CON_RETRIES+1):
            try:
                msg = json.dumps(cmd) 
                self.socket.send(msg)
                response = self.socket.recv(self.MSG_BUFF_SIZE)
                response = json.loads(response)
                return response
            except TypeError:
                print "Got exception: %s, while trying to parse msg: %s to json" % (sys.exc_info()[0], str(cmd))
                raise
            except:
                print "%d Try to send to server, got exception: %s" % (x, sys.exc_info()[0])
                if x == self.CON_RETRIES:
                    raise
                time.sleep(self.WAIT_SEC_BEFORE_RETRY)
        
    def listen(self):
        self.socket.bind(self.addr)
        self.socket.listen(5)
        
    def accept(self):
        conn, addr =  self.socket.accept()
        return Handler(conn, addr)
            
    def send(self, msg):
        self.socket.send(msg)
        
    def receive(self, size):
        return self.socket.recv(size)
    
    def close(self):
        self.socket.close()
        
class Server(Communication):
    def __init__(self, addr, eventQueue):
        Communication.__init__(self, addr)
        
        self.eventQueue = eventQueue;
        self.listening = True
        
    def run(self):
        self.listen()
        print "Start to listen for incoming events"
        while(self.listening):
            conn, addr =  self.socket.accept()
            handler = Handler(conn, addr, self.eventQueue)
            thread.start_new(handler.run, ())
        
class Handler(object):
    def __init__(self, socket, addr, eventQueue):
        self.sock = socket
        self.addr = addr
        self.eventQueue = eventQueue
        self.running = True
        
    def run(self):
        while (self.running):
            msg = self._receive()
            print msg
        
    def _receive(self):
        return self.sock.recv(1024)
    
    def send(self, msg):
        self.sock.send(msg)

             
        
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
    
    
    
        
        
        