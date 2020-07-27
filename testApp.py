from app.filedevice import *
from app.fileparser import *
from app.fileendpoint import *
from app.httpendpoint import *
from steam import function

if __name__ == "__main__":
    batchlen = 5

    fdevice = FileDevice()
    fdevice.config('temperature.csv')

    fparser = FileParser()
    
    fendpoint = FileEndpoint()
    fendpoint.config('saida.txt')
    #hendpoint = HTTPEndpoint()
    #hendpoint.config('http://localhost:8080/wso2')
    
    fdevice.setParser(fparser)
    fdevice.addEndpoint(fendpoint)
    #fdevice.addEndpoint(hendpoint)
    fdevice.addFunction(function.Min(batchlen))
    fdevice.addFunction(function.Max(batchlen))
    fdevice.addFunction(function.Sum(batchlen))
    fdevice.addFunction(function.Count(batchlen))
    fdevice.addFunction(function.Mean(batchlen))
    fdevice.addFunction(function.StDev(batchlen))

    fdevice.run()