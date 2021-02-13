from app.filedevice import *
from app.fileparser import *
from app.fileendpoint import *
from app.httpendpoint import *
from steam.format import *
from steam.condition import *
from steam import function


if __name__ == "__main__":
    batchlen = 50
    endpoint = None
    dataformat = None
    sendcondition = None

    device = FileDevice(batchlen)
    device.config('sensors.txt')

    endpoint = FileEndpoint()
    endpoint.config('saida.txt')

    #endpoint = HTTPEndpoint()
    #endpoint.config('http://localhost:38080/logdata')
    #endpoint.config('http://192.168.9.61:8006/inputStreamSave')

    #dataformat = JSONFormat()
    #dataformat = CSVFormat()
    #dataformat.config(header=False)

    #sendcondition = ThresholdCondition()
    #sendcondition.config(attribute='count', lower=20)

    if endpoint:
        device.addEndpoint(endpoint)

    if dataformat:
        endpoint.setFormat(dataformat)

    if sendcondition:
        endpoint.setCondition(sendcondition)

    device.setParser(Parser(unit='C', separator='\t', columns=['id', 'timestamp', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9']))

    #device.addFunction(function.Min(batchlen=10))
    #device.addFunction(function.Max(batchlen=3))
    #device.addFunction(function.Sum(batchlen=batchlen))
    #device.addFunction(function.Count(batchlen=batchlen))
    device.addFunction(function.Mean(batchlen=10, attribute='value.s1'))
    device.addFunction(function.Slope(batchlen=2, attribute='value.s2'))
    device.addFunction(function.Max(id='max_mean', batchlen=5, attribute='mean'))
    device.addFunction(function.Max(id='max_slope', batchlen=5, attribute='slope'))
    #device.addFunction(function.StDev(batchlen=batchlen))
    #device.addFunction(function.EWMA(batchlen=10))
    #device.addFunction(function.AutoArimaFunction(batchlen=50, periods=5))
    #device.addFunction(function.ArimaFunction(batchlen=20, periods=5, p=2, d=0, q=0))
    device.run()
