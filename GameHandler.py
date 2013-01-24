'''
Created on Jan 23, 2013

@author: Simon
'''
import CardHandler
import NameGenerator

class Player(object):
    '''
    Class for implementing player code
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.hand = CardHandler.Hand()
        self.playerName = NameGenerator.Generator().generateName()
        print "Player name: " + self.playerName
    
    def start(self):
        print "Joining new Game"
        self._joinNewGame()        
        
    def _joinNewGame(self):
        # TODO join a new game on the server
        pass
    

class Game(object):
    '''
    This class holds the game functionality toward server and other clients
    '''
    
    def __init__(self):
        pass
    
    # Server methods
    def joinGame(self, nick):
        pass
    
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
        