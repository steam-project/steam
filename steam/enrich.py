class Enrich:
    def setData(self, packet, data):
        self._packet = packet
        self._data = data
        
    def enrich(self):
        self._packet.update(self._data)
        return self._packet