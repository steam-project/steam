import statistics

# Base class for functions
class Function(object):
    def __init__(self, id, name, batchsize = 0):
        self._id = id
        self._name = name
        self._batch = []
        self._batchsize = batchsize
        
    def addData(self, data):
        if self._batchsize > 0:
            while len(self._batch) >= self._batchsize:
                self._batch.pop(0)
        self._batch.append(data)
        
    def calculate(self):
        calculated = { self._id: self._batch[-1] }
        return True, calculated

# Min function
class Min(Function):
    def __init__(self, batchsize = 0):
        super().__init__('min', 'Min value', batchsize)
        
    def calculate(self):
        try:
            return True, { self._id: min(self._batch) }
        except:
            return False, { self._id: self._batch }

# Max function
class Max(Function):
    def __init__(self, batchsize = 0):
        super().__init__('max', 'Max value', batchsize)
        
    def calculate(self):
        try:
            return True, { self._id: max(self._batch) }
        except:
            return False, { self._id: self._batch }
        
# Sum function
class Sum(Function):
    def __init__(self, batchsize = 0):
        super().__init__('sum', 'Sum of values', batchsize)
        
    def calculate(self):
        try:
            return True, { self._id: sum(self._batch) }
        except:
            return False, { self._id: self._batch }

# Count function
class Count(Function):
    def __init__(self, batchsize = 0):
        super().__init__('count', 'Count of values', batchsize)
        
    def calculate(self):
        try:
            return True, { self._id: len(self._batch) }
        except:
            return False, { self._id: self._batch }

# Mean function
class Mean(Function):
    def __init__(self, batchsize = 0):
        super().__init__('mean', 'Mean of values', batchsize)
        
    def calculate(self):
        try:
            return True, { self._id: statistics.mean(self._batch) }
        except:
            return False, { self._id: self._batch }

# StDev function
class StDev(Function):
    def __init__(self, batchsize = 0):
        super().__init__('stdev', 'Standard deviation of values', batchsize)
        
    def calculate(self):
        if len(self._batch) > 1:
            try:
                return True, { self._id: statistics.pstdev(self._batch) }
            except:
                return False, { self._id: self._batch }
        else:
            return True, { self._id: 0.0 }