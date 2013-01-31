'''
Created on Jan 23, 2013

@author: Simon
'''
class ServerSettings(object):
    HOST =  "129.242.22.237"#"njaal.net"#
    PORT =  9898
    ADDR = (HOST, PORT)

class CardType(object):
    SPADES = "spades"
    CLUBS = "clubs"
    HEARTS = "hearts"
    DIAMONDS = "diamonds"
    JOKER = "joker"
    
class CardColor(object):
    JOKER = 2
    BLACK = 1
    RED = 0

