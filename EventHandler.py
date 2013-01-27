'''
Created on Jan 27, 2013

@author: Simon
'''

import pygame
from pygame.locals import *



class Dispatcher(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self._handlers = {}
        
    def register_handler(self, etype, handler):
        self._handlers[etype] = handler
        
    def dispatch(self, event):
        if event.type in self._handlers:
            self._handlers[event.type](event)
        else:
            print "Unregistered event type", event.type
        

def testHandler(event):
    print "works"
        
if __name__ == "__main__":
    pygame.init()
    
    dispatcher = Dispatcher()
    
    dispatcher.register_handler(MOUSEMOTION, testHandler)
    
    finished = False
    while not finished:
        for event in pygame.event.get():
            if event.type == QUIT:
                finished = True
            else:
                dispatcher.dispatch(event)