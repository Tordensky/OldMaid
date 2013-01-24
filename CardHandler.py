'''
Created on Jan 23, 2013

@author: Simon
'''
from Properties import Kinds, CardColor
from random import shuffle
import sys

class Hand(object):
    '''
    Class for holding the hand of the player
    '''
    def __init__(self):
        self._cardDeck = []
        
    def __str__(self):
        return "Cards in hand: " + str(self._cardDeck)
        
    def shuffle(self):
        shuffle(self._cardDeck)
    
    def addCard(self, card):
        self._cardDeck.append(card)
        self.shuffle()
        
    def getAllCards(self):
        return self._cardDeck
    
    def pickCard(self, index):
        try:
            return self._cardDeck.pop(index)
        except:
            print "Error picking card from hand:", sys.exc_info()[0]
            raise
    
    def _getPairs(self):
        pass
        
    def count(self):
        return self._cardDeck.count()
    
    def countPairs(self):
        pass

        
class Card(object):
    '''
    Class holding a single card
    '''
    def __init__(self, number, kind):
        self._number = number
        self._kind = kind
    
    def __eq__(self, card):
        return self._isCompatiblePair(card)
    
    def __str__(self):
        if self._kind == Kinds.JOKER:
            return "Card: %s" % (Kinds.JOKER)
        return "Card: %d of %s" % (self._number, self._kind)
        
    def __repr__(self):
        return self.__str__()
    
                
    @property    
    def color(self):
        if self._kind in [Kinds.SPADES, Kinds.CLUBS]:
            return CardColor.BLACK
        elif self._kind in [Kinds.HEARTS, Kinds.DIAMONDS]:
            return CardColor.RED
        elif self._kind in [CardColor.JOKER]:
            return Kinds.JOKER
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
    cardA = Card(1, Kinds.SPADES)
    cardB = Card(1, Kinds.DIAMONDS)
    cardC = Card(1, Kinds.HEARTS)
    cardD = Card(0, Kinds.JOKER)
    
    print cardA
    print cardB
    print cardC
    print cardD
    
    print "Should be False is: %s" % (cardA.isPair(cardB))
    print "Should be True is: %s" % (cardC.isPair(cardB))  
    print "Should be %d is: %d" % (CardColor.RED, cardB.color)
    print "Should be %d is: %d" % (CardColor.BLACK, cardA.color)  
    print "Should be %d is: %d" % (1, cardB.getNumber())
    print "Should be %s is: %s" % (Kinds.SPADES, cardA.getKind())
    
    #tests for Hand Class
    hand = Hand()
    try:
        print "Should be an exception", hand.pickCard(2)
        print "Should not have printed this"
    except:
        print "Success got exception"
    
    print hand
    hand.addCard(cardA)
    hand.addCard(cardB)
    hand.addCard(cardC)
    hand.addCard(cardD)
    print hand
    hand.shuffle()
    print "After shuffle", hand
    