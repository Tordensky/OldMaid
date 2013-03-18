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




def debugPrint(fn):
    debugPrint = False
    def wrapper(*args, **kwargs):
        if debugPrint:
            print "\nCall Method:", fn.__name__
            print "\tNum args:", (len(args) + len(kwargs))
            print "\targs:", args
            print "\tkwargs", kwargs
            ret = fn(*args, **kwargs)
            print "\treturns", ret
            print "end of call\n"
        else:
            ret = fn(*args, **kwargs)
        return ret
    return wrapper

    
    