from steam.enrich import *

class Device(object):
    def __init__(self):
        self._enrich = Enrich()
        self._functions = []
        self.resetPacket()
    
    def resetPacket(self):
        self._packet = {
            'id': 0,
            'value': 0,
            'unit': 'un',
            'timestamp': 0
        }
        
    def config(self):
        pass
        
    def setParser(self, parser):
        self._parser = parser
        
    def setEndpoint(self, endpoint):
        self._endpoint = endpoint
        
    def addFunction(self, function):
        self._functions.append(function)
        
    def run(self):
        pass