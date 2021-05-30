from steam.utils import *

class Condition:
    def __init__(self):
        self._packet = None

    def setPacket(self, packet):
        self._packet = packet
        
    def evaluate(self):
        return True


class EquationCondition(Condition):
    def __init__(self, equation):
        super().__init__()
        self._equation = equation

    def evaluate(self):
        try:
            packet = self._packet
            equation = self._equation
            tokens = equation.replace('(', ' ').replace(')', ' ').split()
            var_names = [ x for x in tokens if x in packet ]
            var_names.extend([ x for x in tokens if '.' in x ])
            for var_name in var_names:
                equation = equation.replace(var_name, str(get_value(packet, var_name)))

            evaluated = eval(equation)
            return bool(evaluated)
        except:
            return False


class MissingValueCondition(Condition):
    def __init__(self, columns=['value']):
        super().__init__()
        self._columns = columns

    def evaluate(self):
        for col in self._columns:
            if get_value(self._packet, col) in ['', None]:
                return True

        return False


class ThresholdCondition(Condition):
    def __init__(self, columns=['value'], lower=[], upper=[]):
        super().__init__()
        self._columns = columns
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
