'''
Created on Jan 24, 2013

@author: Simon
'''

import random

partA = [ \
         "crazy",
         "SteffenThe",
         "SimonThe",
         "SimenThe",
         "WeiThe",
         "Marthe",
         "IdaThe",
         "AlexThe",
         "green",
         "skinny",
         "stupidAss",
         "motherFuckingUgly", 
         "sick", 
         "blue", 
         "red", 
         "angry", 
         "tall", 
         "fat", 
         "smart", 
         "fancy", 
         "ugly", 
         "scary", 
         "defeated",
         "sexy",
         "fancy",
         "black",
         "legendary"
         "interesting",
         "notPretty",
         "handsome",
         "girly",
         "matcho",
         "gangsta",
         "overExposed", 
         "winning",
         "suicidal", 
         "gifted" \
         ]

partB = [ \
        "monkey",
        "helicopter",
        "mountain",
        "bread",
        "table",
        "iceCream",
        "pencil",
        "firetruck",
        "airplane",
        "pilot",
        "manBearPig",
        "transistor",
        "horse",
        "donkey",
        "robot",
        "santa",
        "Ass",
        "baby",
        "computer",
        "car",
        "chainssaw",
        "rock",
        "screen", 
        "paper", \
        ]

partC = [\
        "killer",
        "eater", 
        "hunter", 
        "rapist",
        "runner",
        "swimmer",
        "sitter",
        "writer",
        "screamer",
        "smeller",
        "legend", 
        "gamer", \
        ]

class Generator(object):
    '''
    Class for generating random names
    '''
    
    def generateName(self):
        return self._getRandom(partA) + self._getRandom(partB) + self._getRandom(partC) 
        
    def _getRandom(self, words):
        tmp = words[random.randrange(0, len(words))]
        tmp = tmp[0].capitalize() + tmp[1:]
        return tmp
    
if __name__ == '__main__':
    for x in range(200):
        print Generator().generateName() 
        
        
        
        