'''
Created on Jan 23, 2013

@author: Simon
'''
class ServerSettings(object):
    ADDR = "njaal.net"
    PORT =  9898

class Kinds(object):
    SPADES = "spades"
    CLUBS = "clubs"
    HEARTS = "hearts"
    DIAMONDS = "diamonds"
    JOKER = "joker"
    
class CardColor(object):
    JOKER = 2
    BLACK = 1
    RED = 0
    
class State(object):
    NOT_STARTED = 0
    JOINED = 1
    CONNECTED = 2
    DRAW = 3
    WAIT = 4
    NEXT_TURN = 5
    LAST_CARD = 6
    ERROR = 7
    OFFER_HAND = 8
    PICK = 9

