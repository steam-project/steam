import os

class Input:
    def readData(self):
        raise NotImplementedError

class FileInput(Input):
    def __init__(self, filename):
        self._filename = filename
        self._fin = open(filename)
        self._filesize = os.fstat(self._fin.fileno()).st_size

    def readData(self):
        while True:
            if self._fin.tell() == self._filesize:
                self._fin.close()
                return False, None
            else:
                line = self._fin.readline().replace('\r', '').replace('\n', '')
                if len(line.strip()):
                    if line[0] != '#':
                        return True, line