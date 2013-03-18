'''
Created on Feb 18, 2013

@author: Simon
'''
class Players(object):
    def __init__(self, myName = ""):
        self.players = []
        self.myName = myName
        self.myAddr = ""
        self.myNum = -1
        self.out = False
        
        self.myTurn = False
        self.numPlayers = 0
    
    def __str__(self):
        return self.__repr__()
        
    def __repr__(self):
        msg = ""
        for x in self.players:
            msg = msg + ("%s" % (x))
        return msg
    
    def addPlayersFromJson(self, msg):
        num = 0
        for player in msg["players"]:
        #for player in sorted(msg["players"].keys()):
            
        #    name, num, addr = self._parsePlayerInfo(player, msg["players"][player])
            addr, name = player
            num += 1
            
            # Ugly hack to handle IPv6 addresses in Windows
            if len(addr[0]) > 14:
                addr[0] = addr[0][7:]
            
            addr = tuple(addr)
            player = Player(name, num, addr)
            
            if name == self.myName:
                self.myNum = num
                self.myAddr = addr
                player.isMe = True
                
                if num == 1:
                    self.myTurn = True
            
            self.players.append(player)
            
        self.numPlayers = len(self.players)
        
        print "Added following", self.numPlayers, "players to game:"    
        print self
    
    def _parsePlayerInfo(self, key, playerData):
        name = playerData[1]
        num = int(key[-1])
        addr = tuple(playerData[0])
        return name, num, addr
    
    def getNextLeftPlayerAddr(self):
        for x in range(self.myNum, self.numPlayers + self.myNum - 1):
            nextLeft = x % self.numPlayers
            if not self.players[nextLeft].out:
                addr = self.players[nextLeft].addr
                print "I Player%d is Connecting to Player%d @ addr: %s" % (self.myNum, self.players[nextLeft].num, addr)
                return addr
        return -1
    
    def setOutFromAddr(self, addr):
        for player in self.players:
            if player.addr == addr:
                player.out = True;
                return True
            
        print "Could not find playes that has addr %s in list of players" % (addr)
        return False
    
    def setOutFromStatus(self, res):
        playersOut = res["out"]
        for player in self.players:
            playString = "player" + str(player.num)
            if playString in playersOut:
                player.out = True
        
            
                    
class Player(object):
    def __init__(self, name, playerNum, addr):
        self.name = name
        self.num = playerNum
        self.addr = addr
        self.isMe = False
        self.out = False
    
    def __repr__(self):
        return "Player%s is %s @ Addr: %s, IsMe: %s, Is out: %s\n" % (self.num, self.name, self.addr, self.isMe, self.out)
        
    def isFirst(self):
        if self.myNum == 1:
            return True
        return False