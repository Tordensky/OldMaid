'''
Created on Jan 27, 2013

@author: Simon
'''
import sys

class DataType(object):
    SOCKET_HANDLER = "socket_handle"
    EXCEPTION = "exception"
    RECEIVED_MESSAGE = "msg"
        
class EventType(object):
    JOIN = "join"
    DRAW = "draw"
    FINISH = "finish"
    YOUR_TURN = "your_turn"
    MY_TURN = "my_turn"
    OUT = "out"
    ERROR = "error"
    SOCKET_HANDLER_EXCEPTION = "socket_handle_exception"
    GOT_PAIR_ON_HAND = "got_pair"
    OFFER_HAND = "offer_hand"
    NO_MORE_CARD_ON_TABLE = "no_more_cards_on_table"  
    PICKED_CARD_FROM_RIGHT_PLAYER = "picked_card_from_left_player"

class Event(object):
    def __init__(self, eType, data = {}):
        self.type = eType
        self.data = data
    
    def __str__(self):
        return self.__repr__()
        
    def __repr__(self):
        return "EventType: %s Data: %s" % (self.type, str(self.data))

class EventQueue():
    def __init__(self):
        self.queue = []
        
    def addEvent(self, event):
        self.queue.append(event)
        
    def addNewEvent(self, eType, data = {}):
        event = Event(eType, data)
        self.addEvent(event)
        
    def getNext(self):
        if len(self.queue) > 0:
            return self.queue.pop(0)
        return None
    
    def getAll(self):
        tmp = self.queue
        self.queue = []
        return tmp

class Dispatcher(object):

    def __init__(self):
        self._handlers = {}
        
        # setup default exit event
        self.register_handler("exit", self._exit)
        
    def register_handler(self, etype, handler):
        self._handlers[etype] = handler
        
    def dispatch(self, event):
        if event.type in self._handlers:
            self._handlers[event.type](event)
        else:
            print "Unregistered event type:", event.type
            
    def _exit(self, event):
        print "exit event received"
        sys.exit()
        
# FOR TESTING        
if __name__ == "__main__":
    pass