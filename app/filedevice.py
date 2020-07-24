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

        while True:
            valid, line = self.readData()
            if not valid:
                break
            
            self._parser.setData(line)
            valid, parsed = self._parser.parse()
            if valid:
                self.resetPacket()
                self._packet.update(parsed)
                for f in self._functions:
                    f.addData(parsed['value'])
                    valid, data = f.calculate()
                    if valid:
                        self._enrich.setData(self._packet, data)
                        self._enrich.enrich()
                
                self._endpoint.setData(self._packet)
                self._endpoint.send()
                
        print('\nDone!')