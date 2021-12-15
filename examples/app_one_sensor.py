import sys
sys.path.append('../steam')

from steam.device import *
from steam.input import *
from steam.format import *
from steam.condition import *
from steam import function as fn

if __name__ == "__main__":
    ## Create the Device object ##
    device = Device(batchlen=20)

    ## Define the Input method ##
    device.setInput(FileInput('./examples/data/one_sensor.txt'))

    ## Create data parser ##
    device.setParser(Parser(columns=('id', 'timestamp', 'unit', 'value')))

    ## Create the endpoints ##
    # Save to log file
    ep_data_file = FileEndpoint('./examples/logs/one_sensor_log.txt')
    # ep_data_file.setFormat(JSONFormat())
    device.addEndpoint(ep_data_file)

    ## Clear the dashboard
    # ep_clear = HTTPEndpoint(url='http://localhost:1880/clear_one')
    # ep_clear.setCondition(EquationCondition('id == 1'))
    # device.addEndpoint(ep_clear)

    ## Send data to dashboard chart
    # ep_data = HTTPEndpoint(url='http://localhost:1880/datastream_one')
    # ep_data.setFormat(JSONFormat())
    # device.addEndpoint(ep_data)

    ## Send messages to dashboard display
    # ep_upper = HTTPEndpoint(url='http://localhost:1880/msgstream_one')
    # con_upper = ThresholdCondition(columns='value', upper='upper')
    # fmt_upper = MessageFormat('<font color=red>{timestamp} - Value {value:.2f} above {upper:.2f}</font><br>')
    # ep_upper.setCondition(con_upper)
    # ep_upper.setFormat(fmt_upper)
    # device.addEndpoint(ep_upper)
    
    ## Send messages to dashboard display
    # ep_lower = HTTPEndpoint(url='http://localhost:1880/msgstream_one')
    # con_lower = ThresholdCondition(columns='value', lower='lower')
    # fmt_lower = MessageFormat('<font color=blue>{timestamp} - Value {value:.2f} below {lower:.2f}</font><br>')
    # ep_lower.setCondition(con_lower)
    # ep_lower.setFormat(fmt_lower)
    # device.addEndpoint(ep_lower)

    ## Analytical functions ##
    # device.addFunction(fn.Mean(format='{:.2f}'))
    # device.addFunction(fn.StDev(format='{:.2f}'))
    # device.addFunction(fn.Max(format='{:.2f}'))
    # device.addFunction(fn.Min(format='{:.2f}'))

    # device.addFunction(
    #     fn.Equation(
    #         id='upper',
    #         format='{:.2f}',
    #         equation='mean + 2 * stdev'))

    # device.addFunction(
    #     fn.Equation(
    #         id='lower',
    #         format='{:.2f}',
    #         equation='mean - 2 * stdev'))

    ## Run the application ##
    device.run()