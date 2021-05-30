import requests

class Endpoint:
    def __init__(self):
        self._packet = None
        self._format = None
        self._condition = None

    def setPacket(self, packet):
        self._packet = packet
        self._format.setPacket(self._packet)
        self._condition.setPacket(self._packet)

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
        print(self._packet)

class HTTPEndpoint(Endpoint):
    def __init__(self, url):
        super().__init__()
        self._url = url
        self._session = requests.Session()
        
    def send(self):
        ret, out = self.formatData()
        if ret:
            if type(out) == dict:
                self._session.post(self._url, json=out)
            else:
                self._session.post(self._url, data=out)

class FileEndpoint(Endpoint):
    def __init__(self, filename):
        super().__init__()
        self._filename = filename
        self._fout = open(filename, 'w')

    def __del__(self):
        if self._fout:
            self._fout.close()

    def send(self):
        if self._fout:
            ret, out = self.formatData()
            if ret:
                if self._fout.tell() > 0:
                    self._fout.write('\n')
                self._fout.write(str(out))
                