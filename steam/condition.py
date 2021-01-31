class Condition:
    def __init__(self):
        self._packet = None
        self._attribute = None

    def config(self, attribute='value'):
        self._attribute = attribute

    def setPacket(self, packet):
        self._packet = packet
        
    def evaluate(self):
        return True


class ThresholdCondition(Condition):
    def config(self, attribute='value', lower=None, upper=None):
        super().config(attribute)
        self._lower = lower
        self._upper = upper

    def evaluate(self):
        result = False

        if self._attribute in self._packet:
            value = self._packet[self._attribute]

            if not result:
                if self._lower:
                    result = value < self._lower
                    #print(value, '<', self._lower, result)
      
            if not result:
                if self._upper:
                    result = value > self._upper
                    #print(value, '>', self._upper, result)
        
        return result
