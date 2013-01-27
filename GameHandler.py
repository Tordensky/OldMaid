'''
Created on Jan 23, 2013

@author: Simon
'''
import CardHandler
import NameGenerator
import json
from Communication import Communication
from Properties import ServerSettings, State

class Player(object):
    def __init__(self, name, playerNum, addr):
        self.name = name
        self.num = playerNum
        self.addr = addr
     

class Game(object):
    '''
    Class for implementing player code
    '''
    
    def __init__(self):
        self.name = NameGenerator.Generator().generateName()
        self.num = -1
        self.addr = ("", 0)
        
        self.playerCount = 0
        self.otherPlayers = []
        
        print 'Game name: ' + self.name
        
        self.server = Communication(('localhost', 9898))
        self.listener = None
        self.leftPlayer = None
        self.rightPlayer = None
        
        self.hand = CardHandler.Hand()
        
        self.state = State.NOT_STARTED
            
    def start(self):
        self.joinGame(self.name)
        while(True):
            if self.state == State.JOINED:
                self._setupPlayerCom()
            elif self.state == State.CONNECTED:
                self.state = self._isFirst()
            elif self.state == State.DRAW:
                self.drawCard()
            elif self.state == State.NEXT_TURN:
                self.yourTurn()
            elif self.state == State.WAIT:
                self.wait()
            elif self.state == State.ERROR:
                print "GOT AN ERROR STATE"
                break
            elif self.state == State.LAST_CARD:
                print self.hand
                print "NumCards:", self.hand.count()
                print "NumPairs:", self.hand.countPairs()
                self.state = State.OFFER_HAND
            elif self.state == State.OFFER_HAND:
                self.offerHand()
            elif self.state == State.PICK:
                self.pickCard()

    def _isFirst(self):
        if self.num == 1:
            return State.DRAW
        return State.WAIT

    def wait(self):
        res = self.leftPlayer.receive()
        
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
    def joinGame(self, nick):
        '''
        send: {'cmd':'join', 'nick':your_nick}
        recv: {'result':'ok', 'players':['player1':[(ip, port), nick], 'player2':[(ip, port), nick], ...]}
        '''
        print 'Joining new game @ addr:', ServerSettings.ADDR, 'port:', ServerSettings.PORT
        msg = {'cmd' : 'join', 'nick' : nick}
        msg = json.dumps(msg)
        
        self.server.connect()
        self.server.send(msg)
        result = self.server.receive(1024)
        
        print result
        
        try:
            result = json.loads(result)
             
        except:
            print "Error parsing message"
            
        if result["result"] == "ok":
            self._addPlayersInfo(result)
            self.state = State.JOINED
            print self.num, "Player Count:", self.playerCount
        
    def _addPlayersInfo(self, msg):
        for player in msg["players"]:
            self.playerCount += 1
            name, num, addr = self._parsePlayerInfo(player, msg["players"][player])
            if name == self.name:
                self.num = num
                self.addr = addr
            else:
                self.otherPlayers.append(Player(name, num, addr))
    
    def _parsePlayerInfo(self, key, playerData):
        name = playerData[1]
        num = int(key[-1])
        addr = tuple(playerData[0])
        return name, num, addr
    
    def _setupPlayerCom(self):
        self.listener = Communication(self.addr)
        self.listener.listen()
    
        self.rightPlayer = Communication(self.otherPlayers[0].addr)
        self.rightPlayer.connect()
        
        self.leftPlayer = self.listener.accept()
        
        self.state = State.CONNECTED
        print "Goes to accept"
        
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
        