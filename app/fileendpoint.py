from steam.endpoint import *

class FileEndpoint(Endpoint):
    def __del__(self):
        if self._fout:
            self._fout.close()
            
    def config(self, filename):
        self._filename = filename
        self._fout = open(filename, 'w')
        
    def send(self):
        if self._fout:
            if self._fout.tell() == 0:
                self._fout.write('\t'.join([str(x) for x in self._data.keys()]))
            self._fout.write('\n' + '\t'.join([str(x) for x in self._data.values()]))