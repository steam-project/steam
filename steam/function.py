from pmdarima import auto_arima
from statsmodels.tsa.arima_model import ARIMA
import statistics
import warnings


# Base class for functions
class Function:
    def __init__(self, id, batchlen):
        self._id = id
        self._count = 0
        self._batchlen = batchlen

    def config(self, packets, values):
        self._packets = packets
        self._values = values
        
    def calculate(self):
        first = 0
        if self._batchlen > 0 and len(self._values) > self._batchlen:
            first = len(self._values) - self._batchlen
        
        self._batchpackets = self._packets[first:]
        self._batchvalues = self._values[first:]
        
        calculated = { self._id: self._batchvalues[-1] }
        self._count += 1
        return True, calculated


# Min function
class Min(Function):
    def __init__(self, id='min', batchlen=0):
        super().__init__(id, batchlen)
        
    def calculate(self):
        try:
            super().calculate()
            return True, { self._id: min(self._batchvalues) }
        except:
            return False, { self._id: self._batchvalues }


# Max function
class Max(Function):
    def __init__(self, id='max', batchlen=0):
        super().__init__(id, batchlen)
        
    def calculate(self):
        try:
            super().calculate()
            return True, { self._id: max(self._batchvalues) }
        except:
            return False, { self._id: self._batchvalues }


# Sum function
class Sum(Function):
    def __init__(self, id='sum', batchlen=0):
        super().__init__(id, batchlen)
        
    def calculate(self):
        try:
            super().calculate()
            return True, { self._id: sum(self._batchvalues) }
        except:
            return False, { self._id: self._batchvalues }


# Count function
class Count(Function):
    def __init__(self, id='count', batchlen=0):
        super().__init__(id, batchlen)
        
    def calculate(self):
        try:
            super().calculate()
            return True, { self._id: len(self._batchvalues) }
        except:
            return False, { self._id: self._batchvalues }


# Mean function
class Mean(Function):
    def __init__(self, id='mean', batchlen=0):
        super().__init__(id, batchlen)
        
    def calculate(self):
        try:
            super().calculate()
            return True, { self._id: statistics.mean(self._batchvalues) }
        except:
            return False, { self._id: self._batchvalues }


# StDev function
class StDev(Function):
    def __init__(self, id='stdev', batchlen=0):
        super().__init__(id, batchlen)
        
    def calculate(self):
        super().calculate()
        if len(self._batchvalues) > 1:
            try:
                return True, { self._id: statistics.pstdev(self._batchvalues) }
            except:
                return False, { self._id: self._batchvalues }
        else:
            return True, { self._id: 0.0 }


class AutoArimaFunction(Function):
    def __init__(self, id='auto_arima', batchlen=0, periods=1, start_p=0, d=0, start_q=0, max_p=5, max_d=5, max_q=5, start_P=0, D=0, start_Q=0, max_P=5, max_D=5, max_Q=5, max_order=5, m=1, seasonal=True, stationary=False):
        self._periods = periods
        self._start_p = start_p
        self._d = d
        self._start_q = start_q
        self._max_p = max_p
        self._max_d = max_d
        self._max_q = max_q
        self._start_P = start_P
        self._D = D
        self._start_Q = start_Q
        self._max_P = max_P
        self._max_D = max_D
        self._max_Q = max_Q
        self._max_order = max_order
        self._m = m
        self._seasonal = seasonal
        self._stationary = stationary
        self._stepwise_model = None
        super().__init__(id, batchlen)

    def set_auto_arima_model(self):
        self._stepwise_model = auto_arima(self._batchvalues, start_p = self._start_p, d = self._d, start_q = self._start_q, max_p = self._max_p, max_d = self._max_d, max_q = self._max_q, start_P = self._start_P, D = self._D, start_Q = self._start_Q, max_P = self._max_P, max_D = self._max_D, max_Q = self._max_Q, max_order = self._max_order, m = self._m, seasonal = self._seasonal, stationary = self._stationary, trace=False,error_action = 'ignore', suppress_warnings = True, stepwise = True)
        self.train_auto_arima_model()

    def get_auto_arima_model(self):
        return self._stepwise_model

    def train_auto_arima_model(self):
        list_treinamento = self._batchvalues[len(self._batchvalues) - self._batchlen:]
        self._stepwise_model.fit(list_treinamento)

    def update_auto_arima_model(self):
        self._stepwise_model.update(self._batchvalues)
        self.train_auto_arima_model()

    def predict_auto_arima(self):
        #return self._stepwise_model.predict(n_periods=self.periods)[0]
        return dict(zip([self._id + '_' + str(x + 1) for x in range(self._periods)], self._stepwise_model.predict(n_periods=self._periods)))

    def calculate(self):
        super().calculate()
        try:
            if self._count == self._batchlen:
                print('Creating auto arima model')
                self.set_auto_arima_model()
            else:
                if self._count > self._batchlen:
                    if self._count % self._batchlen == 0:
                        print('Fitting auto arima model')
                        self.update_auto_arima_model()
                    else:
                        self._stepwise_model.fit(self._batchvalues)

            if self._stepwise_model:
                return True, self.predict_auto_arima()
            else:
                return True, dict(zip([self._id + '_' + str(x + 1) for x in range(self._periods)], [''] * self._periods))
        except:
            return False, { self._id: self._batchvalues }


class ArimaFunction(Function):
    def __init__(self, id='arima', batchlen=0, periods=1, p=0, d=0, q=0):
        self._periods = periods
        self._p = p
        self._d = d
        self._q = q
        self._model = None
        warnings.filterwarnings("ignore")
        super().__init__(id, batchlen)

    def set_arima_model(self):
        self._model = ARIMA(self._batchvalues, order=(self._p, self._d, self._q)).fit(disp=0)

    def update_arima_model(self):
        self._model = ARIMA(self._batchvalues, order=(self._p, self._d, self._q)).fit(disp=0)

    def get_arima_model(self):
        return self._model

    def predict_arima(self):
        return dict(zip([self._id + '_' + str(x + 1) for x in range(self._periods)], self._model.forecast(steps=self._periods)[0]))

    def calculate(self):
        super().calculate()
        try:
            if self._count == self._batchlen:
                print('Creating arima model')
                self.set_arima_model()
            else:
                if self._count > self._batchlen:
                    self.update_arima_model()

            if self._model != None:
                return True, self.predict_arima()
            else:
                return True, dict(zip([self._id + '_' + str(x + 1) for x in range(self._periods)], [''] * self._periods))
        except:
            return False, { self._id: self._batchvalues }
