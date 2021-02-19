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

    device = FileDevice('sensors.txt', batchlen)
    device.setParser(Parser(unit='C', separator='\t', columns=['s1', 's2', 's3']))

    endpoint = FileEndpoint('log.txt')

    #endpoint = HTTPEndpoint()
    #endpoint.config('http://localhost:38080/logdata')
    #endpoint.config('http://192.168.9.61:8006/inputStreamSave')

    #dataformat = JSONFormat()
    #dataformat = TSVFormat(['id', 's1_mean', 's1_slope', 's2_mean', 's2_slope', 's3_mean', 's3_slope'])
    dataformat = TSVFormat(['id', 'value.s1', 'value.s2', 'value.s3', 's1_slope', 's2_slope', 's3_slope'])
    #dataformat.config(header=False)

    #sendcondition = ThresholdCondition()
    #sendcondition.config(attribute='count', lower=20)

    if dataformat:
        endpoint.setFormat(dataformat)

    if sendcondition:
        endpoint.setCondition(sendcondition)

    if endpoint:
        device.addEndpoint(endpoint)

    #device.addFunction(function.Min(batchlen=10))
    #device.addFunction(function.Max(batchlen=3))
    #device.addFunction(function.Sum(batchlen=batchlen))
    #device.addFunction(function.Count(batchlen=batchlen))

    #device.addFunction(function.Mean(id='s1_mean', batchlen=2, attribute='value.s1'))
    #device.addFunction(function.Mean(id='s2_mean', batchlen=2, attribute='value.s2'))
    #device.addFunction(function.Mean(id='s3_mean', batchlen=2, attribute='value.s3'))

    device.addFunction(function.Slope(id='s1_slope', batchlen=3, attribute='value.s1'))
    device.addFunction(function.Slope(id='s2_slope', batchlen=3, attribute='value.s2'))
    device.addFunction(function.Slope(id='s3_slope', batchlen=3, attribute='value.s3'))

    #device.addFunction(function.Slope(id='s1_slope', batchlen=2, attribute='s1_mean'))
    #device.addFunction(function.Slope(id='s2_slope', batchlen=2, attribute='s2_mean'))
    #device.addFunction(function.Slope(id='s3_slope', batchlen=2, attribute='s3_mean'))

    #device.addFunction(function.Max(id='max_mean', batchlen=5, attribute='mean'))
    #device.addFunction(function.Max(id='max_slope', batchlen=5, attribute='slope'))
    #device.addFunction(function.StDev(batchlen=batchlen))
    #device.addFunction(function.EWMA(batchlen=10))
    #device.addFunction(function.AutoArimaFunction(batchlen=50, periods=5))
    #device.addFunction(function.ArimaFunction(batchlen=20, periods=5, p=2, d=0, q=0))
    device.run()
