from app.filedevice import *
from app.fileparser import *
from app.fileendpoint import *
from app.httpendpoint import *
from steam.format import *
from steam.condition import *
from steam import function


if __name__ == "__main__":
    # Variables initialization
    batchlen = 50
    endpoint = None
    dataformat = None
    sendcondition = None

    # Read raw data from file
    device = FileDevice(filename='sensors.txt', batchlen=batchlen)

    # Raw data parser
    device.setParser(Parser(unit='C', separator='\t', columns=['s1', 's2', 's3']))

    # Save processed data to file
    endpoint = FileEndpoint(filename='saida.txt')

    # Send processed data to HTTP service
    #endpoint = HTTPEndpoint(url='http://localhost:38080/logdata')
    #endpoint = HTTPEndpoint(url='http://192.168.9.61:8006/inputStreamSave')

    # Format of processed data
    #dataformat = JSONFormat(['id', 'value.s1', 'value.s2', 'value.s3', 'mean', 'slope', 'max_mean', 'max_slope'])
    #dataformat = CSVFormat()
    dataformat = TSVFormat(['id', 'value.s1', 'value.s2', 'value.s3', 'mean', 'slope', 'max_mean', 'max_slope'])

    # Condition for sending processed data
    #sendcondition = ThresholdCondition(columns=['value.s1', 'value.s2'], upper=[-20, -20])

    # Configure application - begin - do not change order
    if dataformat:
        endpoint.setFormat(dataformat)

    if sendcondition:
        endpoint.setCondition(sendcondition)

    if endpoint:
        device.addEndpoint(endpoint)
    # Configure application - end - do not change order

    # Analytical function list
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

    # Run the application
    device.run()
