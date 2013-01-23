'''
Created on Jan 23, 2013

@author: Simon
'''
from Properties import SPADES, HEARTS, CLUBS, DIAMONDS, RED, BLACK
from random import shuffle
import sys

class Hand(object):
    '''
    Class for holding the hand of the player
    '''
    def __init__(self):
        self.cardDeck = []
        
    def shuffle(self):
        shuffle(self.cardDeck)
    
    def addCard(self, card):
        self.cardDeck.append(card)
        self.shuffle()
        
    def getAllCards(self):
        return self.cardDeck
    
    def pickCard(self, index):
        try:
            return self.cardDeck.pop(index)
        except:
            print "Error picking card from hand:", sys.exc_info()[0]
            raise
        
    def count(self):
        return self.cardDeck.count()

        
class Card(object):
    '''
    Class holding a single card
    '''
    def __init__(self, number, kind):
        self._number = number
        self._kind = kind
    
    @property    
    def color(self):
        if self._kind in [SPADES, CLUBS]:
            return BLACK
        elif self._kind in [HEARTS, DIAMONDS]:
            return RED
        else:
            raise Exception("Invalid Card Kind")
            
        
    def getNumber(self):
        return self._number
    
    def getKind(self):
        return self._kind
        
    def isPair(self, card):
        '''
        Method for checking if two cards are compatible
        '''
        if self._number == card.getNumber():
            if self._isCompatiblePair(card):
                return True
        return False
        
    def _isCompatiblePair(self, card):
        if self.color == card.color:
            return True
        return False
        
        
if __name__ == '__main__':    
    # Tests for cards class
    cardA = Card(1, SPADES)
    cardB = Card(1, DIAMONDS)
    cardC = Card(1, HEARTS)
    
    print "Should be False is: %s" % (cardA.isPair(cardB))
    print "Should be True is: %s" % (cardC.isPair(cardB))  
    print "Should be %d is: %d" % (RED, cardB.color)
    print "Should be %d is: %d" % (BLACK, cardA.color)  
    print "Should be %d is: %d" % (1, cardB.getNumber())
    print "Should be %s is: %s" % (SPADES, cardA.getKind())
    
    #tests for Hand Class
    hand = Hand()
    print "Should be an exception", hand.pickCard(2)
    
    #
    
        
