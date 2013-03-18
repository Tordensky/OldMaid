'''
Created on Jan 23, 2013

@author: Simon
'''
import socket, json, sys, time, thread, random 
from EventHandler import DataType, EventType
random.seed(time.clock())

class Communication(object):
    CON_RETRIES = 1
    WAIT_SEC_BEFORE_RETRY = 0
    MSG_BUFF_SIZE = 2048
    
    def __init__(self, addr):
        self.addr = addr
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                
    def connect(self):
        for x in range(1, self.CON_RETRIES+1):
            try: 
                self.socket.connect(self.addr)
                break
            
            except:
                print "%d. Try to connect, got exception: %s" % (x, sys.exc_info()[0])
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
            
            except socket.error:
                print "%d Try to send to server, got exception: %s" % (x, sys.exc_info()[0])
                if x == self.CON_RETRIES:
                    raise
                time.sleep(self.WAIT_SEC_BEFORE_RETRY)
        
    def listen(self):
        self.socket.bind(self.addr)
        self.socket.listen(5)
        
    def accept(self):
        conn, addr =  self.socket.accept()
        return RightHandHandler(conn, addr)
            
    def send(self, msg):
        self.socket.send(msg)
        
    def sendOK(self):
        self.socket.send({""})
        
    def receive(self, size):
        return self.socket.recv(size)
    
    def getConnectionAddr(self):
        return self.socket.getpeername()
    
    def close(self):
        self.socket.close()
        
class RightHandServer(Communication):
    def __init__(self, addr, eventQueue, players):
        Communication.__init__(self, addr)
        
        self.eventQueue = eventQueue;
        self.listening = True
        self.players = players
        
    def run(self):
        self.listen()
        print "Start to listen for incoming events"
        while(self.listening):
            conn, addr =  self.socket.accept()
            handler = RightHandHandler(conn, addr, self.eventQueue, self.players)
            thread.start_new(handler.run, ())
            
       
class RightHandHandler(object):
    def __init__(self, socket, addr, eventQueue, players):
        self.sock = socket
        self.addr = addr
        self.eventQueue = eventQueue
        self.running = True
        self.players = players
        
    def run(self):
        while (self.running):
            try:
                msg = self._receive()          
                self._parseMessage(msg)
                
            except socket.error, e:
                eventData = {}
                eventData[DataType.EXCEPTION] = e
                eventData[DataType.SOCKET_HANDLER] = self 
                self.eventQueue.addNewEvent(EventType.SOCKET_HANDLER_EXCEPTION, eventData)
                break;
                  
        self.teardown()
    
    def _parseMessage(self, msg):
        if msg:
            try:
                msg = json.loads(msg)
                if msg.has_key("cmd"):
                    if msg["cmd"] == "your_turn":
                        print "Gets my turn from right player"
                        self.eventQueue.addNewEvent(EventType.MY_TURN)
                        self.sendOK()
                    
                    elif msg["cmd"] == "offer":
                        print "Got Offer hand from right player"
                        if self.players.out:
                            self.sendOUT()
                        
                        else:
                            self.sendOK()
                            time.sleep(0.05)
                            self._pickCard(msg["num_cards"])
                               
                    else:
                        print "received cmd:", msg["cmd"]
                else:
                    print "Error: message does not have a command"
                
            except TypeError:
                print "Error parsing JSON/Message in RightHandler receive"
    
    def _pickCard(self, numCards):
        if numCards > 0:
            
            pick = random.randrange(0, numCards)
            if numCards == 1:
                pick = 0
            
            cmd = {"cmd" : "pick", "card_num" : pick}
            msg = json.dumps(cmd)
            self.send(msg)
            
            res = self._receive()
            res = json.loads(res)
            if res.has_key("result"):
                if res["result"] == "ok":
                    data = {}
                    data[DataType.RECEIVED_MESSAGE] = res
                    self.eventQueue.addNewEvent(EventType.PICKED_CARD_FROM_RIGHT_PLAYER, data)
                    print "Picked Card from right player"
                elif res["result"] == "error":
                    print "Got error trying to pick card"
        else:
            #self.players.setOutFromAddr(self.sock.getpeername())
            self.eventQueue.addNewEvent(EventType.OFFER_HAND)   
            
    def _receive(self):
        return self.sock.recv(2048)
    
    def sendOK(self):
        msg = json.dumps({"result" : "ok"})
        self.send(msg)
        
    def sendOUT(self):
        msg = json.dumps({"result" : "out"})
        self.send(msg)
    
    def send(self, msg):
        self.sock.send(msg)
        
    def teardown(self):
        print "Tearing down connection"
        self.sock.close()


class LeftHand(Communication):
    def __init__(self, eventQueue, players):
        addr = players.getNextLeftPlayerAddr()
        if addr == -1:            
            return None    
        self.addr = addr
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.eventQueue = eventQueue
        self.players = players
        
    def receive(self, size):
        msg = self.socket.recv(size)
        return msg
    
    def send(self, msg):
        self.socket.send(msg)
        
                    
if __name__ == "__main__":
    pass
