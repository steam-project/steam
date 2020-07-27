from steam.enrich import *

class Device(object):
    def __init__(self):
        self._enrich = Enrich()
        self._endpoints = []
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
        raise NotImplementedError
        
    def setParser(self, parser):
        self._parser = parser
        
    def addEndpoint(self, endpoint):
        self._endpoints.append(endpoint)
        
    def addFunction(self, function):
        self._functions.append(function)
        
    def readData(self):
        raise NotImplementedError
        
    def run(self):
        while True:
            valid, line = self.readData()
            if not valid:
                break
            
            self._parser.setData(line)
            valid, parsed = self._parser.parse()
            if valid:
                self.resetPacket()
                self._packet.update(parsed)
                for f in self._functions:
                    f.addData(parsed['value'])
                    valid, data = f.calculate()
                    if valid:
                        self._enrich.setData(self._packet, data)
                        self._enrich.enrich()
                
                for e in self._endpoints:
                    e.setData(self._packet)
                    e.send()