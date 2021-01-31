import json


class Format:
    def __init__(self):
        self._packet = None
        
    def setPacket(self, packet):
        self._packet = packet
        
    def format(self):
        return True, self._packet


class CSVFormat(Format):
    def __init__(self):
        super().__init__()
        self._header = True
        
    def config(self, header):
        self._header = header
       
    def format(self):
        out = ''
        
        try:
            if self._header:
                self._header = False
                out = ','.join([str(x) for x in self._packet.keys()]) + '\r'
            out += ','.join([str(x) for x in self._packet.values()])

            return True, out
        except:
            return False, self._packet


class TSVFormat(Format):
    def __init__(self):
        super().__init__()
        self._header = True
        
    def config(self, header):
        self._header = header

    def format(self):
        out = ''
        
        try:
            if self._header:
                self._header = False
                out = '\t'.join([str(x) for x in self._packet.keys()]) + '\r'
            out += '\t'.join([str(x) for x in self._packet.values()])

            return True, out
        except:
            return False, self._packet


class JSONFormat(Format):
    def __init__(self):
        super().__init__()
        
    def format(self):
        try:
            out = json.dumps(self._packet, separators=(',', ':'))
            return True, out
        except:
            return False, self._packet


class WSO2Format(Format):
    def __init__(self):
        super().__init__()
        
    def format(self):
        try:
            out = {'event': self._packet}
            return True, out
        except:
            return False, self._packet
