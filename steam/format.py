import json
from steam.utils import *


class Format:
    def __init__(self, columns=[]):
        self._packet = None
        self._source_packet = None
        self._columns = columns

    def setPacket(self, packet):
        self._source_packet = packet

    def format(self):
        if len(self._columns) > 0:
            self._packet = {}
            for col in self._columns:
                self._packet.update({col.split('.')[-1]: get_value(self._source_packet, col)})
        else:
            self._packet = self._source_packet

        return True, self._packet


class MessageFormat(Format):
    def __init__(self, message='', columns=[]):
        super().__init__(columns)
        self._message = message
        
    def format(self):
        super().format()
        out = ''
        
        try:
            out = self._message % self._packet
            return True, out
        except:
            return False, self._packet

class CSVFormat(Format):
    def __init__(self, columns=[], header=True):
        super().__init__(columns)
        self._header = header
        
    def format(self):
        super().format()
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
    def __init__(self, columns=[], header=True):
        super().__init__(columns)
        self._header = header
        
    def format(self):
        super().format()
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
    def __init__(self, columns=[]):
        super().__init__(columns)
        
    def format(self):
        super().format()
        try:
            out = json.dumps(self._packet, separators=(',', ':'))
            out = out.replace("''", 'null').replace('""', 'null')
            return True, out
        except:
            return False, self._packet


class WSO2Format(Format):
    def __init__(self, columns=[]):
        super().__init__(columns)
        
    def format(self):
        super().format()
        try:
            out = {'event': self._packet}
            return True, out
        except:
            return False, self._packet
