'''
Created on Jan 24, 2013

@author: Simon
'''

import random

partA = [ \
         "crazy",
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
        "pencil",
        "firetruck",
        "airplane",
        "pilot",
        "manBearPig",
        "transistor",
        "horse",
        "donkey",
        "robot",
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
        "rappist",
        "runner",
        "swimmer",
        "sitter",
        "writer",
        "screamer",
        "smeller",
        "storyTeller", 
        "gamer",
        "numberOne" \
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
        
        
        
        