import time

from steam.parser import *

class FileParser(Parser):
    def parse(self):
        valid, parsed = super().parse()

        if valid:
            try:
                parsed['unit'] = 'C'
                parsed['value'] = float(self._data)
                return True, parsed
            except:
                return False, parsed
        else:
            return False, parsed
