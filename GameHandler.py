'''
Created on Jan 23, 2013
@author: Simon
'''
import CardHandler, NameGenerator, json, EventHandler,socket, thread
from Communication import Communication, Server
from Properties import ServerSettings, State, EventType

class Players(object):
    def __init__(self, myName = ""):
        self.players = []
        self.myName = myName
        self.myAddr = ""
        self.myNum = -1
    
    def __str__(self):
        return self.__repr__()
        
    def __repr__(self):
        msg = ""
        for x in self.players:
            msg = msg + ("%s" % (x))
        return msg
    
    def addPlayersFromJson(self, msg):
        for player in sorted(msg["players"].keys()):
            
            name, num, addr = self._parsePlayerInfo(player, msg["players"][player])
            
            player = Player(name, num, addr)
            
            if name == self.myName:
                self.myNum = num
                self.myAddr = addr
                player.isMe = True
            
            self.players.append(player)
        
        print "Added following players to game:"    
        print self
    
    def _parsePlayerInfo(self, key, playerData):
        name = playerData[1]
        num = int(key[-1])
        addr = tuple(playerData[0])
        return name, num, addr
                    
class Player(object):
    def __init__(self, name, playerNum, addr):
        self.name = name
        self.num = playerNum
        self.addr = addr
        self.isMe = False
        self.out = False
    
    def __repr__(self):
        return "Player%s is %s @ Addr: %s, IsMe: %s\n" % (self.num, self.name, self.addr, self.isMe)
        
    def isFirst(self):
        if self.myNum == 1:
            return True
        return False
     
class Game(object):
    '''
    Class for implementing player code
    '''
    def __init__(self):
        
        name = NameGenerator.Generator().generateName()
        print 'Game name: ' + name
                
        self.players = Players(name)
        self.hand = CardHandler.Hand()
 
        self.eventQueue = EventHandler.EventQueue()
        self.dispatcher = EventHandler.Dispatcher()
        self._setupEvents()
 
        self.cardServer = Communication(ServerSettings.ADDR)
             
    def _setupEvents(self):
        self.dispatcher.register_handler(EventType.FINNISH, self._finnish)
        
        self.dispatcher.register_handler(EventType.JOIN, self.joinGame)
        
        self.dispatcher.register_handler(EventType.ERROR, self._error)
        
    def _finnish(self, event):
        # Todo teardown system
        print "Client is shutting down"
        self.finished = True
        
    def _error(self, event):
        data = event.data
        
        if data.has_key("msg"):
            print data["msg"]
            
        if data.has_key("fatal"):
            if data["fatal"] == True:
                self.eventQueue.addNewEvent(EventType.FINNISH)
                
    def start(self):
        self.eventQueue.addNewEvent(EventType.JOIN)
        
        self.finished = False
        while not self.finished:
            for event in self.eventQueue.getAll():
                self.dispatcher.dispatch(event)
        
    def wait(self):
        res = self.leftPlayer.receive()
        
        print "RESULT IN WAIT:", res
        res = json.loads(res)
        
        if res["cmd"] == "your_turn":
            msg = {"result" : "ok"}
            msg = json.dumps(msg)
            self.leftPlayer.send(msg)
            self.state = State.DRAW
        
        elif res["cmd"] == "offer":
            print res
            msg = {"result" : "ok"}
            msg = json.dumps(msg)
            self.leftPlayer.send(msg)
            self.state = State.PICK
                                              
    # Server methods
    def joinGame(self, event):
        '''
        send: {'cmd':'join', 'nick':your_nick}
        recv: {'result':'ok', 'players':['player1':[(ip, port), nick], 'player2':[(ip, port), nick], ...]}
        '''
        print 'Joining new game @ addr:', ServerSettings.HOST, 'port:', ServerSettings.PORT
        
        try: 
            self.cardServer.connect()
            cmd = {"cmd" : "join", "nick" : self.players.myName}
            result = self.cardServer.cmd(cmd)
            if result["result"] == "ok":
                self.players.addPlayersFromJson(result)
                
            else:
                eventData = {"msg" : "Error: Got some kind of error from card server", "fatal" : True}
                self.eventQueue.addNewEvent(EventType.ERROR, eventData)
                
        except TypeError:
            eventData = {"msg" : "Error: Could not parse to JSON in joinGame", "fatal" : True}
            self.eventQueue.addNewEvent(EventType.ERROR, eventData)
        
        except socket.error:
            eventData = {"msg" : "Error: Could not connect to card server after several tries, Exiting", "fatal" : True}
            self.eventQueue.addNewEvent(EventType.ERROR, eventData)
            
        self._setupPlayerCom()
               
    def _setupPlayerCom(self):
        print "Starting to set up connection to left and right player"
        
        self.rigthHand = Server(self.players.myAddr, self.eventQueue)
        thread.start_new(self.rigthHand.run, ())
#        self.listener = Communication(self.addr)
#        self.listener.listen()
#    
#        self.rightPlayer = Communication(self.players[0].addr)
#        self.rightPlayer.connect()
#        
#        self.leftPlayer = self.listener.accept()
                
    def drawCard(self):
        '''
        send: {'cmd':'draw'} 
        recv: {'result':'ok'/'last_card'/'error', 'card': ['3', 'spades']}
        '''
        msg = {'cmd' : 'draw'}
        msg = json.dumps(msg)
        self.server.send(msg)
        res = self.server.receive(1024)
        
        res = json.loads(res)
        
        if res["result"] == "ok":
            self.hand.addCardFromJSON(res["card"])
            self.state = State.NEXT_TURN
        elif res["result"] == "last_card":
            print "last Card"
            self.state = State.LAST_CARD
        elif res["result"] == "error":
            print "GOT ERROR FROM SERVER"
             
    
    def discardPair(self):
        '''
        send: {'cmd':'discard', 'cards': [['3', 'spades'], ['3', 'clubs']], 'last_cards':'true'/'false'} 
        recv: {'result': 'ok'/'error', 'message':'ok'/error_message}
        '''
        pass
    
    def outOfCards(self):
        '''
        send: {'cmd':'out_of_cards'}
        recv: {'result':'ok'}
        '''
        pass
    
    def getStatus(self):
        '''
        send: {'cmd':'status'}
        recv: {'in':['player1', 'player2', ...], 'out':{'player3'}}
        '''
        pass
    
    #Client methods
    def yourTurn(self):
        '''
        send: {'cmd':'your_turn'}
        recv: {'result':'ok'}
        '''
        msg = {"cmd" : "your_turn"}
        msg = json.dumps(msg)
        self.rightPlayer.send(msg)
        
        res = self.rightPlayer.receive(1024)
        res = json.loads(res)
        
        if res["result"] == "ok":
            self.state = State.WAIT
        else:
            self.state = State.ERROR
        
        
    def offerHand(self):
        '''
        send: {'cmd':'offer', 'num_cards':number of cards left}
        recv: {'result':'ok'/'out'}
        '''
        msg = {"cmd" : "offer", "num_cards" : str(self.hand.count())}
        msg = json.dumps(msg)
        
        self.rightPlayer.send(msg)
        
        res = self.rightPlayer.receive(1024)
    
        print "offerHand before jsonloads: ", res
        res = json.loads(res)
        if res["result"] == "ok":
            self.state = State.WAIT
            print res
            
        elif res["result"] == "out":
            # TODO connect to next player            
            print "player to offer hand is out of cards"
    
    def pickCard(self):
        '''
        send: {'cmd':'pick', 'card_num': the number of the card chosen (must be between 0 and
                number_of_cards_left offered}
        recv: {'result':'ok'/'error', 'card':['3', 'spades']}
        '''
        pass
    
    
if __name__ == '__main__':    
    player = Game()
    player.start()
        