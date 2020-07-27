class Endpoint:
    def config(self):
        raise NotImplementedError
        
    def setData(self, data):
        self._data = data

    def send(self):
        raise NotImplementedError