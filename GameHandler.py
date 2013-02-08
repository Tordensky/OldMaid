'''
Created on Jan 23, 2013
@author: Simon
'''
import CardHandler, NameGenerator, socket, thread, time, json,sys
from Communication import Communication, RightHandServer, LeftHand
from Properties import ServerSettings
from EventHandler import EventType, Dispatcher, EventQueue, DataType

class Players(object):
    def __init__(self, myName = ""):
        self.players = []
        self.myName = myName
        self.myAddr = ""
        self.myNum = -1
        self.out = False
        
        self.myTurn = False
        self.numPlayers = 0
    
    def __str__(self):
        return self.__repr__()
        
    def __repr__(self):
        msg = ""
        for x in self.players:
            msg = msg + ("%s" % (x))
        return msg
    
    def addPlayersFromJson(self, msg):
        num = 0
        for player in msg["players"]:
        #for player in sorted(msg["players"].keys()):
            
        #    name, num, addr = self._parsePlayerInfo(player, msg["players"][player])
            addr, name = player
            num += 1
            
            # Ugly hack to handle IPv6 addresses in Windows
            if len(addr[0]) > 14:
                addr[0] = addr[0][7:]
            
            addr = tuple(addr)
            player = Player(name, num, addr)
            
            if name == self.myName:
                self.myNum = num
                self.myAddr = addr
                player.isMe = True
                
                if num == 1:
                    self.myTurn = True
            
            self.players.append(player)
            
        self.numPlayers = len(self.players)
        
        print "Added following", self.numPlayers, "players to game:"    
        print self
    
    def _parsePlayerInfo(self, key, playerData):
        name = playerData[1]
        num = int(key[-1])
        addr = tuple(playerData[0])
        return name, num, addr
    
    def getNextLeftPlayerAddr(self):
        print "players", self.players
        for x in range(self.myNum, self.numPlayers + self.myNum - 1):
            nextLeft = x % self.numPlayers
            if not self.players[nextLeft].out:
                addr = self.players[nextLeft].addr
                print "I Player%d is Connecting to Player%d @ addr: %s" % (self.myNum, self.players[nextLeft].num, addr)
                return addr
        return -1
    
    def setOutFromAddr(self, addr):
        for player in self.players:
            if player.addr == addr:
                print player.name, "is OUT of the game"
                player.out = True;
                return True
        print "Could not find playes that has addr %s in list of players" % (addr)
        return False
    
    def setOutFromStatus(self, res):
        playersOut = res["out"]
        for player in self.players:
            playString = "player" + str(player.num)
            if playString in playersOut:
                player.out = True
        
            
                    
class Player(object):
    def __init__(self, name, playerNum, addr):
        self.name = name
        self.num = playerNum
        self.addr = addr
        self.isMe = False
        self.out = False
    
    def __repr__(self):
        return "Player%s is %s @ Addr: %s, IsMe: %s, Is out: %s\n" % (self.num, self.name, self.addr, self.isMe, self.out)
        
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
        
        self.eventQueue = EventQueue()
        self.dispatcher = Dispatcher()
        self._setupEvents()
        
        self.players = Players(name)
        self.hand = CardHandler.Hand(self.eventQueue)
 
        self.cardServer = Communication(ServerSettings.ADDR)
        
        self.noCardOnTable = False
        
        self.leftHand = None
        self.rigthHand = None
             
    def _setupEvents(self):
        self.dispatcher.register_handler(EventType.FINISH, self._finnish)
        self.dispatcher.register_handler(EventType.JOIN, self.joinGame)
        self.dispatcher.register_handler(EventType.ERROR, self._error)
        self.dispatcher.register_handler(EventType.SOCKET_HANDLER_EXCEPTION, self._handlerException)
        self.dispatcher.register_handler(EventType.DRAW, self.drawCard)
        self.dispatcher.register_handler(EventType.GOT_PAIR_ON_HAND, self.discardPair)
        self.dispatcher.register_handler(EventType.OUT, self.outOfCards)
        
        self.dispatcher.register_handler(EventType.MY_TURN, self.myTurn)
        self.dispatcher.register_handler(EventType.YOUR_TURN, self.yourTurn)
        self.dispatcher.register_handler(EventType.OFFER_HAND, self.offerHand)
        
        self.dispatcher.register_handler(EventType.NO_MORE_CARD_ON_TABLE, self._setNoMoreCardsOnTable)
        
        self.dispatcher.register_handler(EventType.PICKED_CARD_FROM_RIGHT_PLAYER, self.gotCard)
        
    def _finnish(self, event):
        # Todo teardown system
        print "Client is shutting down"
        self.finished = True
    
    def _handlerException(self, Event):
        print "Got an socket handler exception", Event
        
    def _error(self, event):
        data = event.data
        
        if data.has_key("msg"):
            print data["msg"]
            
        if data.has_key("fatal"):
            if data["fatal"] == True:
                self.eventQueue.addNewEvent(EventType.FINISH)
    
    def _setNoMoreCardsOnTable(self, event):
        self.noCardOnTable = True
                    
    def start(self):
        self.eventQueue.addNewEvent(EventType.JOIN)
        
        self.finished = False
        while not self.finished:
            
#            if len(self.eventQueue.queue):
#                print self.eventQueue.queue
            time.sleep(0.1)
            
            #print self.players
            
            for event in self.eventQueue.getAll():
                self.dispatcher.dispatch(event)
                #print "CARD LEFT:", self.hand.count(), "Is out:", self.players.out, "Card on table", self.noCardOnTable
    
    def myTurn(self, event):
        if not self.noCardOnTable:
            self.drawCard(None)
    
    def gotCard(self, event):
        self.hand.addCardFromRes(event.data[DataType.RECEIVED_MESSAGE])
        self.eventQueue.addNewEvent(EventType.OFFER_HAND)
        
                                                          
    # RightHandServer methods
    def joinGame(self, event):
        '''
        send: {'cmd':'join', 'nick':your_nick}
        recv: {'result':'ok', 'players':['player1':[(ip, port), nick], 'player2':[(ip, port), nick], ...]}
        '''
        print 'Joining new game @ addr:', ServerSettings.HOST, 'port:', ServerSettings.PORT
        
        try: 
            self.cardServer.connect()
            cmd = {"cmd" : "join", "nick" : self.players.myName, "port" : ServerSettings.MY_PORT}
            result = self.cardServer.cmd(cmd)
            if result["result"] == "ok":
                self.players.addPlayersFromJson(result)
                
            else:
                eventData = {"msg" : "Error: Got some kind of error from card server", "fatal" : True}
                self.eventQueue.addNewEvent(EventType.ERROR, eventData)
                return
                
        except TypeError:
            eventData = {"msg" : "Error: Could not parse to JSON in joinGame", "fatal" : True}
            self.eventQueue.addNewEvent(EventType.ERROR, eventData)
            return
        
        except socket.error:
            eventData = {"msg" : "Error: Could not connect to card server after several tries, Exiting", "fatal" : True}
            self.eventQueue.addNewEvent(EventType.ERROR, eventData)
            return
            
        self._setupPlayerCom()
               
    def _setupPlayerCom(self):
        print "Starting to set up connection to left and right player"
        
        # This is the right hand server handling incoming events
        self.rigthHand = RightHandServer(self.players.myAddr, self.eventQueue, self.players)
        thread.start_new(self.rigthHand.run, ())
                
        try:
            self.leftHand = LeftHand(self.eventQueue, self.players)
            self.leftHand.connect()
        except socket.error:
            eventData = {"msg" : "Error: Could not connect to left player in initial phase, Exiting", "fatal" : True}
            self.eventQueue.addNewEvent(EventType.ERROR, eventData)
            return
            
        print "Connection to other players established successfully"
        
        if self.players.myTurn:
            self.eventQueue.addNewEvent(EventType.DRAW)
                
    def drawCard(self, event):
        '''
        send: {'cmd':'draw'} 
        recv: {'result':'ok'/'last_card'/'error', 'card': ['3', 'spades']}
        '''
        print "Is about to draw a Card"
        
        msg = {'cmd' : 'draw'}
        res = self.cardServer.cmd(msg)
                
        if res["result"] == "ok":
            self.hand.addCardFromRes(res)
            self.eventQueue.addNewEvent(EventType.YOUR_TURN)
            return
        
        elif res["result"] == "last_card":
            print "Got Last Card"
            self.hand.addCardFromRes(res)
            self.noCardOnTable = True
            #print "hand:", self.hand
            self.eventQueue.addNewEvent(EventType.OFFER_HAND)
            pass
        
        elif res["result"] == "error":
            print "got error from server"
        
        else:
            eventData = {"msg" : "Error: Got invalid response from server while trying to draw card, Exiting", "fatal" : True}
            self.eventQueue.addNewEvent(EventType.ERROR, eventData)
            return
        
        
    
    def discardPair(self, event):
        '''
        send: {'cmd':'discard', 'cards': [['3', 'spades'], ['3', 'clubs']], 'last_cards':'true'/'false'} 
        recv: {'result': 'ok'/'error', 'message':'ok'/error_message}
        '''
        pair = self.hand.removeNextPair()
        print "Starting to discard pair", pair, "to cardServer"
        
        lastCardOnHand = self.hand.lastCard()
        
        if lastCardOnHand == True and self.noCardOnTable == True:
            print "Discarded last card on hand, I am out"
            self.players.out = True
            self.outOfCards(None)
        else:
            # Can't exit game if there are more cards that could be drawn from table
            lastCardOnHand = False
        
        cmd = {"cmd" : "discard", "cards" : pair, "last_card" : lastCardOnHand}
        
        res = self.cardServer.cmd(cmd)
        
        if res["result"] == "ok":
            print "Discarded pair to server successfully"
                
        elif res["result"] == "error":
            print "got error:", res["message"]
    
    def outOfCards(self, event):
        '''
        send: {'cmd':'out_of_cards'}
        recv: {'result':'ok'}
        '''
        self.players.out = True
        cmd = {"cmd" : "out_of_cards"}
        res = self.cardServer.cmd(cmd)
        
        print "I am out of cards"        
    
    def getStatus(self):
        '''
        send: {'cmd':'status'}
        recv: {'in':['player1', 'player2', ...], 'out':{'player3'}}
        '''
        cmd = {"cmd" : "status"}
        res = self.cardServer.cmd(cmd)
        
        print "Got status from server: ", res
        if res.has_key("out"):
            print "Players out:", res["out"]
            self.players.setOutFromStatus(res)
    
    #Client methods
    def yourTurn(self, Event):
        '''
        send: {'cmd':'your_turn'}
        recv: {'result':'ok'}
        '''
        cmd = {"cmd" : "your_turn"}
        
        res = self.leftHand.cmd(cmd)
        if res["result"] == "ok":
            print "End of turn, sent yourTurn to next player"
        
    def offerHand(self, event):
        '''
        send: {'cmd':'offer', 'num_cards':number of cards left}
        recv: {'result':'ok'/'out'}
        '''
        count = self.hand.count()
        
        self.noCardOnTable = True
        
        lastCardOnHand = self.hand.lastCard()
        
        if lastCardOnHand == True and self.noCardOnTable == True:
            print "Discarded last card on hand, I am out"
            self.players.out = True
            self.outOfCards(None)
        
        cmd = {"cmd" : "offer", "num_cards" : count}
        
        self.getStatus()
        
        for x in range(self.players.numPlayers):        
            
            res = self.leftHand.cmd(cmd)
            
            if res.has_key("result"):
                if res["result"] == "ok":
                    if count > 0:
                        self.pickCard(self.leftHand.receive(1024))
                        break;
                
                elif res["result"] == "out":
                    print "GOT OUT OF CARDS ! ! !!  ! !! ! !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                    outAddr = self.leftHand.getConnectionAddr()
                    self.getStatus()
                    self.players.setOutFromAddr(outAddr)
                    self.leftHand.close()
                    for x in range(self.players.numPlayers):
                        self.getStatus()
                        self.leftHand = LeftHand(self.eventQueue, self.players)
                        if self.leftHand == None:
                            print "GAME OVER"
                            sys.exit()
                            return
                        else:
                            self.leftHand.connect()
                            break
                    
                
    
    def pickCard(self, res):
        '''
        send: {'cmd':'pick', 'card_num': the number of the card chosen (must be between 0 and
                number_of_cards_left offered}
        recv: {'result':'ok'/'error', 'card':['3', 'spades']}
        '''
        res = json.loads(res)
        if res.has_key("cmd"):
            if res["cmd"] == "pick":
                card = self.hand.pickCard(res['card_num'])
                msg = {"result" : "ok", "card" : card}
                msg = json.dumps(msg)
                self.leftHand.send(msg)
    
if __name__ == '__main__':    
    player = Game()
    player.start()
        