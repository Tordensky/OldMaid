'''
Created on Jan 23, 2013

@author: Simon
'''
import CardHandler
import NameGenerator
import json
from Properties import ServerSettings

class Player(object):
    '''
    Class for implementing player code
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.playerName = NameGenerator.Generator().generateName()
        print "Player name: " + self.playerName
        
        self.hand = CardHandler.Hand()
        
        self._game = Game()
    
    def start(self):
        self._joinNewGame()        
        
    def _joinNewGame(self):
        self._game.joinGame(self.playerName)

class Game(object):
    '''
    This class holds the game functionality toward server and other clients
    '''
    
    def __init__(self):
        pass
    
    # Server methods
    def joinGame(self, nick):
        print "Joining new game @ addr:", ServerSettings.ADDR, "port:", ServerSettings.PORT
        msg = {"cmd" : "join", "nick" : nick}
        msg = json.dumps(msg)
        
        
        
    def drawCard(self):
        pass
    
    def discardPair(self):
        pass
    
    def outOfCards(self):
        pass
    
    def getStatus(self):
        pass
    
    #Client methods
    def yourTurn(self):
        pass
    
    def offerHand(self):
        pass
    
    def pickCard(self):
        pass
    
    
if __name__ == '__main__':    
    player = Player()
    player.start()
        