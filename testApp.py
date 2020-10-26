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
    fendpoint.config('saida.txt', 'json') # format = 'csv', 'tsv' or 'json'
    hendpoint = HTTPEndpoint()
    #hendpoint.config('http://127.0.0.1:8006/inputStream')
    #hendpoint.config('http://localhost:38080/logdata')
    
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
