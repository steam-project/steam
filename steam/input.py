import os
import psutil

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
                    if line[0] not in '# ': # skip empty and comments
                        return True, line
                        
class SystemMonitoringInput(Input):
    def __init__(self, interval_sec=1):
        self._interval_sec = interval_sec

    def readData(self):
        cpu = psutil.cpu_percent(self._interval_sec)
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        net = psutil.net_io_counters()
        disk_usage = psutil.disk_usage('/')
        disk_count = psutil.disk_io_counters()
        
        line = {
            'cpu_pc': cpu,
            'mem_pc': mem.percent,
            'mem_used': mem.used,
            'swap_pc': swap.percent,
            'swap_used': swap.used,
            'net_bytes_sent': net.bytes_sent,
            'net_bytes_recv': net.bytes_recv,
            'disk_pc': disk_usage.percent,
            'disk_used':disk_usage.used,
            'disk_read_count': disk_count.read_count,
            'disk_write_count': disk_count.write_count,
            'disk_read_bytes': disk_count.read_bytes,
            'disk_write_bytes': disk_count.write_bytes,
            'disk_read_time': disk_count.read_time,
            'disk_write_time': disk_count.write_time
        }

        return True, line
