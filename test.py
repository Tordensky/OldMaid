'''
Created on Feb 6, 2013

@author: Simon
'''

import json

messageError = { "msg" : "Nick is missing", "result" : "error"}
messageOk = {"result" : "ok", "players" : []}



if __name__ == '__main__':
    print messageError.has_key("result")
    print messageError["result"]
    
    