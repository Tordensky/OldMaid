'''
Created on Jan 23, 2013

@author: Simon
'''
from Properties import CardType, CardColor
import random, time
import sys
from EventHandler import EventType

random.seed(time.clock())

class Hand(object):
    '''
    Class for holding the hand of the player
    '''
    def __init__(self, eventQueue):
        self._cardsOnHand = []
        self._pairs = []
        self.eventQueue = eventQueue
        
    def __str__(self):
        return "Cards in hand: " + str(self._cardsOnHand)
        
    def shuffle(self):
        random.shuffle(self._cardsOnHand)
    
    def addCardFromRes(self, res):
        res = res["card"]
        newCard = Card(res[0], res[1])
        self.addCard(newCard)
        
    def addCard(self, newCard):
        isPair, pairCard = self._checkIfPair(newCard)
        if isPair:
            print "Got", newCard, "to hand, is pair with", pairCard
            self._pairs.append([pairCard.tolist(), newCard.tolist()])
            self.eventQueue.addNewEvent(EventType.GOT_PAIR_ON_HAND)
        else:
            print "Added", newCard, "to hand"
            self._cardsOnHand.append(newCard)
        self.shuffle()
    
    def _checkIfPair(self, newCard):
        for card in self._cardsOnHand:
            if card.isPair(newCard):
                tmp = card
                self._cardsOnHand.remove(card)
                return (True, tmp)
        return (False, None)
        
    def getAllCards(self):
        return self._cardsOnHand
    
    def _removePair(self):
        return self._pairs.pop(0)
    
    def removeNextPair(self):
        if self.countPairs() > 0:
            return self._removePair()
        return None
            
    def removeAllPairs(self):
        tmp = self._pairs
        self._pairs =[]
        return tmp;
        
    def pickCard(self, index = 0):
        try:
            self.lastCard()
            return self._cardsOnHand.pop(index).tolist()
        except:
            print "Error picking card from hand:", sys.exc_info()[0]
            raise
        
    def count(self):
        return len(self._cardsOnHand)
    
    def countPairs(self):
        return len(self._pairs)
    
    def lastCard(self):
        if len(self._cardsOnHand) == 0:
            return True
        return False

        
class Card(object):
    '''
    Class holding a single card
    '''
    def __init__(self, number, kind):
        self._number = number
        self._kind = kind
    
    #def __eq__(self, card):
    #    return self._isCompatiblePair(card)
    
    def __str__(self):
        if self._kind == CardType.JOKER:
            return "Card: %s" % (CardType.JOKER)
        return "Card: %s of %s" % (str(self._number), self._kind)
        
    def __repr__(self):
        return self.__str__()
    
                
    @property    
    def color(self):
        if self._kind in [CardType.SPADES, CardType.CLUBS]:
            return CardColor.BLACK
        elif self._kind in [CardType.HEARTS, CardType.DIAMONDS]:
            return CardColor.RED
        elif self._kind in [CardType.JOKER]:
            return CardColor.JOKER
        else:
            print "kind is", self._kind
            raise Exception("Invalid Card Kind")
                
    def getNumber(self):
        return self._number
    
    def getKind(self):
        return self._kind
    
    def tolist(self):
        return [self._number, self._kind]
            
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
    pass
    