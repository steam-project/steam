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
    device.setInput(FileInput('./examples/data/multi_sensors.txt'))

    ## Create data parser ##
    device.setParser(Parser(columns=['id', 'timestamp', 'unit', 's1', 's2', 's3']))

    ## Create the endpoints ##
    # Save to log file
    ep_data_log = FileEndpoint('./examples/logs/multi_sensor_log.txt')
    device.addEndpoint(ep_data_log)

    ## Clear the dashboard
    # ep_clear = HTTPEndpoint(url='http://localhost:1880/clear_multi')
    # ep_clear.setCondition(EquationCondition('id == 1'))
    # device.addEndpoint(ep_clear)

    ## Send data to dashboard chart
    # ep_data = HTTPEndpoint(url='http://localhost:1880/datastream_multi')
    # ep_data.setFormat(JSONFormat())
    # device.addEndpoint(ep_data)

    ## Send messages to dashboard display
    # ep_missing = HTTPEndpoint(url='http://localhost:1880/msgstream_multi')
    # con_missing = MissingValueCondition(columns=['s1', 's2', 's3'])
    # fmt_missing = MessageFormat('<font color=blue>{timestamp} - Value missing</font><br>')
    # ep_missing.setCondition(con_missing)
    # ep_missing.setFormat(fmt_missing)
    # device.addEndpoint(ep_missing)
    
    ## Send messages to dashboard display
    # ep_slope = HTTPEndpoint(url='http://localhost:1880/msgstream_multi')
    # con_slope = EquationCondition('slope_disagree')
    # fmt_slope = MessageFormat('<font color=red>{timestamp} - Slope disagreement</font><br>')
    # ep_slope.setCondition(con_slope)
    # ep_slope.setFormat(fmt_slope)
    # device.addEndpoint(ep_slope)

    ## Analytical functions ##
    device.addFunction(fn.Slope(id='s1_slope', batchlen=2, attribute='s1', format='{:.1f}'))
    device.addFunction(fn.Slope(id='s2_slope', batchlen=2, attribute='s2', format='{:.1f}'))
    device.addFunction(fn.Slope(id='s3_slope', batchlen=2, attribute='s3', format='{:.1f}'))

    device.addFunction(
        fn.Equation(
            id='slope_disagree',
            equation='max(s1_slope, s2_slope, s3_slope) > 0.1 and min(s1_slope, s2_slope, s3_slope) < -0.1'))

    ## Run the application ##
    device.run()
