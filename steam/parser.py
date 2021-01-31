import time


class Parser:
    def __init__(self):
        self._id = 0
        self._data = 0
        self._timestamp = 0
        
    def setData(self, data):
        self._data = data
        
    def parse(self):
        self._id += 1
        self._timestamp = int(time.time() * 1000000)

        parsed = {
            'id': self._id,
            'value': self._data,
            'timestamp': self._timestamp
        }
        return True, parsed
