import os
from steam.device import *


class FileDevice(Device):
    def config(self, filename):
        self._filename = filename
        self._fin = open(filename)
        self._filesize = os.fstat(self._fin.fileno()).st_size

    def readData(self):
        if self._fin.tell() == self._filesize:
            self._fin.close()
            return False, None
        else:
            return True, self._fin.readline().strip()

    def run(self):
        print('Processing', self._filename)
        super().run()
        print('Done!')
