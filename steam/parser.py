import time

from steam.utils import *


class Parser:
    def __init__(self, unit='un', separator='\t', columns=[]):
        self._id = 0
        self._data = 0
        self._timestamp = 0
        self._unit = unit
        self._columns = columns
        self._separator = separator

    def setData(self, data):
        self._data = data
        
    def parse(self):
        self._id += 1
        self._timestamp = int(time.time() * 1000000)

        parsed = {
            'id': self._id,
            'timestamp': self._timestamp,
            #'value': self._data,
            'unit': self._unit
        }

        if len(self._columns) > 0:
            values = [ to_number(x) for x in self._data.split(self._separator) ]
            values = dict(zip(self._columns, values))
            parsed.update(values)

            # for attr in ['id', 'timestamp', 'unit']:
            #     if attr in values:
            #         parsed.update({attr: values.get(attr)})

            # parsed['value'] = values
        else:
            parsed['value'] = to_number(self._data)

        return True, parsed
