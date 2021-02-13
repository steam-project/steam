class Enrich:
    def __init__(self, packet, packets):
        self._packet = packet
        self._packets = packets
        self._data = None

    def setData(self, data):
        self._data = data
        
    def enrich(self):
        self._packet.update(self._data)
        self._packets[-1].update(self._data)