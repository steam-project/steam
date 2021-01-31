from app.filedevice import *
from app.fileparser import *
from app.fileendpoint import *
from app.httpendpoint import *
from steam.format import *
from steam.condition import *
from steam import function


if __name__ == "__main__":
    batchlen = 50
    dataformat = None
    sendcondition = None

    device = FileDevice(batchlen)
    device.config('ds2.csv')

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

    if dataformat:
        endpoint.setFormat(dataformat)

    if sendcondition:
        endpoint.setCondition(sendcondition)

    device.setParser(FileParser())
    device.addEndpoint(endpoint)

    device.addFunction(function.Min(batchlen=10))
    device.addFunction(function.Max(batchlen=3))
    #device.addFunction(function.Sum(batchlen))
    device.addFunction(function.Count())
    #device.addFunction(function.Mean(batchlen))
    #device.addFunction(function.StDev(batchlen))
    #device.addFunction(function.AutoArimaFunction(batchlen=20, periods=3))
    #device.addFunction(function.ArimaFunction(batchlen=20, periods=5, p=2, d=0, q=0))
    device.run()
