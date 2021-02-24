import json


class Format:
    def __init__(self, columns=[]):
        self._packet = None
        self._source_packet = None
        self._columns = columns

    def setPacket(self, packet):
        self._source_packet = packet

    def format(self):
        if len(self._columns) > 0:
            nested_cols = [ x for x in self._columns if '.' in x ]
            simple_cols = [ x for x in self._columns if not '.' in x ]

            self._packet = { key: value for key, value in self._source_packet.items() if key in simple_cols }
            for x in nested_cols:
                key1, key2 = x.split('.')
                if key1 in self._source_packet:
                    if key2 in self._source_packet[key1]:
                        self._packet.update({key2: self._source_packet[key1][key2]})
        else:
            self._packet = self._source_packet

        return True, self._packet


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
