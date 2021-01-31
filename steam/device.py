from steam.enrich import *
from steam.format import *
from steam.condition import *


class Device:
    def __init__(self, batchlen=0):
        self._batchlen = batchlen
        self._parser = None
        self._endpoints = []
        self._functions = []
        self._packets = []
        self._values = []
        self._packet = {'id': 0, 'value': 0, 'unit': 'un', 'timestamp': 0}
        self._enrich = Enrich(self._packet)

    def config(self):
        raise NotImplementedError
        
    def setParser(self, parser):
        self._parser = parser
        
    def addEndpoint(self, endpoint):
        endpoint.setPacket(self._packet)
        if not endpoint.hasFormat():
            endpoint.setFormat(TSVFormat())
        if not endpoint.hasCondition():
            endpoint.setCondition(Condition())
        endpoint._format.setPacket(self._packet)
        endpoint._condition.setPacket(self._packet)
        self._endpoints.append(endpoint)

    def addFunction(self, function):
        function.config(self._packets, self._values)
        self._functions.append(function)
        
    def addData(self, data):
        self._packet.clear()
        self._packet.update(data)

        if self._batchlen > 0:
            while len(self._packets) >= self._batchlen:
                self._packets.pop(0)
                self._values.pop(0)
                
        self._packets.append(data)
        self._values.append(data['value'])

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
                self.addData(parsed)
                for f in self._functions:
                    valid, data = f.calculate()
                    if valid:
                        self._enrich.setData(data)
                        self._enrich.enrich()
                
                for e in self._endpoints:
                    if e.evalCondition():
                        e.send()
