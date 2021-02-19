import json
from steam.endpoint import *


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
