from steam.format import *


class Endpoint:
    def __init__(self):
        self._packet = None
        self._format = None
        self._condition = None

    def setPacket(self, packet):
        self._packet = packet

    def hasFormat(self):
        return bool(self._format)
        
    def hasCondition(self):
        return bool(self._condition)

    def setCondition(self, condition):
        self._condition = condition

    def setFormat(self, format):
        self._format = format

    def formatData(self):
        return self._format.format()
        
    def evalCondition(self):
        return self._condition.evaluate()

    def send(self):
        raise NotImplementedError
