import json
from steam.endpoint import *

class FileEndpoint(Endpoint):
    def __del__(self):
        if self._fout:
            self._fout.close()
            
    def config(self, filename, format):
        self._filename = filename
        self._format = format.lower()
        self._fout = open(filename, 'w')
        
    def formatedOutput(self):
        out = ''

        # csv file
        if self._format == 'csv':
            if self._fout.tell() == 0:
                out = ','.join([str(x) for x in self._data.keys()])
            out += '\n' + ','.join([str(x) for x in self._data.values()])

        # tsv file
        if self._format == 'tsv':
            if self._fout.tell() == 0:
                out = '\t'.join([str(x) for x in self._data.keys()])
            out += '\n' + '\t'.join([str(x) for x in self._data.values()])

        # json file
        if self._format == 'json':
            if self._fout.tell() != 0:
                out = '\n'
            out += json.dumps(self._data, separators=(',', ':'))

        return out

#                if self._fout.tell() == 0:
#                self._fout.write('\t'.join([str(x) for x in self._data.keys()]))
#            self._fout.write('\n' + '\t'.join([str(x) for x in self._data.values()]))
            
    def send(self):
        if self._fout:
            self._fout.write(self.formatedOutput())
