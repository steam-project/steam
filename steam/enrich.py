class Enrich:
    def __init__(self, packet):
        self._packet = packet
        self._data = None

    def setData(self, data):
        self._data = data
        
    def enrich(self):
        self._packet.update(self._data)
