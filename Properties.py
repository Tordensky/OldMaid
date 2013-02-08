'''
Created on Jan 23, 2013

@author: Simon
'''

import random

class ServerSettings(object):
    HOST =  "njaal.net"#"129.242.22.237"#
    PORT =  9898
    ADDR = (HOST, PORT)
    MY_PORT = random.randrange(3000, 4000)

class CardType(object):
    SPADES = "spades"
    CLUBS = "clubs"
    HEARTS = "hearts"
    DIAMONDS = "diamonds"
    JOKER = "maid"
    
class CardColor(object):
    JOKER = 2
    BLACK = 1
    RED = 0

