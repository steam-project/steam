from steam.utils import *

class Condition:
    def __init__(self, columns=[]):
        self._packet = None
        self._columns = columns

    def setPacket(self, packet):
        self._packet = packet
        
    def evaluate(self):
        return True


class MissingValueCondition(Condition):
    def __init__(self, columns=[]):
        super().__init__(columns)

    def evaluate(self):
        for col in self._columns:
            if get_value(self._packet, col) in ['', None]:
                return True

        return False


class ThresholdCondition(Condition):
    def __init__(self, columns=['value'], lower=[], upper=[]):
        super().__init__(columns)
        self._lower = lower
        self._upper = upper

    def evaluate(self):
        for i in range(len(self._columns)):
            value = get_value(self._packet, self._columns[i])

            if value:
                lower = self._lower[i] if i < len(self._lower) else None
                if lower:
                    if value < lower:
                        return True

            if value:
                upper = self._upper[i] if i < len(self._upper) else None
                if upper:
                    if value > upper:
                        return True

        return False
