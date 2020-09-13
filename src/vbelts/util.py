"""Utilities"""

import csv
import os

class OutOfRangeError(Exception):
    """Raised when value is out of range of the list"""
    pass

class NotValidError(Exception):
    """Raised when the value passed to the function is not valid"""
    pass

class ConvergenceError(Exception):
    """Raised when the value passed to an iterator function does not converge"""
    pass

def _read_csv_data(filename:str):
    """Read csv data and return a generator function
    :param filename: file name of the csv file without the extension
    :type filename: str
    :return: contents of the csv file in an ordered dictionary
    :rtype: dict
    """
    # use the full path and pass the file path as filename, OS independent
    file_path = os.path.join(os.path.dirname(__file__), 'data', filename)  # fetch full path
    with open(f'{file_path}.csv', mode='r', encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file, quoting=csv.QUOTE_NONNUMERIC)  # not quoted values are floats
        # next(reader)
        for line in reader:
            yield line


def _interpol(x_data:float, x_min:float, x_max:float, y_min:float, y_max:float):
    """Linear interpolation of table data
    :param x_data: input data point to be calculated
    :type x_data: float
    :param x_min: nearest minimum input value in relation to the data point
    :type x_min: float
    :param x_max: nearest maximum input value in relation to the data point
    :type x_max: float
    :param y_min: nearest minimum output value in the relation to the data point
    :type y_min: float
    :param y_max: nearest maximum output value in the relation to the data point
    :type y_max: float
    :return: interpolated output data
    :rtype: float
    """
    return y_max-((x_max - x_data)/(x_max - x_min))*(y_max - y_min)

def _min_dist(x:float, x_min:float, x_max:float):
    """Nearest value between two items given one value that is in the interval
    :param x: value on the interval
    :type x:
    :param x_min: nearest minimum value on the scale
    :type x_min: float
    :param x_max: nearest maximum value on the scale
    :type x_max:
    :return: nearest value of the x
    :rtype: float
    """
    dist_1 = (x - x_min)/x
    dist_2 = (x_max - x)/x
    if dist_1 < dist_2:
        return x_min
    elif dist_1 > dist_2:
        return x_max
    elif dist_1 == dist_2: # if both are equal, return the maximum
        return x_max
    else:
        raise ValueError

def gear_ratio(rpm_input:float, rpm_output:float):
    """Pulley gear ratio
    :param rpm_input: input (driving) axle speed, rpm
    :type rpm_input: float
    :param rpm_output: output (driven) axle speed, rpm
    :type rpm_output: float
    :return: gear ratio
    :rtype: float
    """
    if isinstance(rpm_input, (float, int)) and isinstance(rpm_output, (float, int)):
        return rpm_input/rpm_output
    else:
        raise ValueError


def est_power(engine_power:float, serv_factor:float):
    """Estimated power to run the pulley system
    :param engine_power: engine power, hp
    :type engine_power: float
    :param serv_factor: calculated service factor
    :type serv_factor: float
    :return: estimated power, hp
    :rtype: float
    """
    if isinstance(engine_power, (float, int)) and isinstance(serv_factor, (float, int)):
        return engine_power * serv_factor
    else:
        raise ValueError


def belt_qty(est_power_system:float, belt_transmission_capacity:float):
    """Number of belts to transmit the estimated power
    :param est_power_system: estimated power to run the pulley system, hp
    :type est_power_system: float
    :param belt_transmission_capacity: power transmission capacity per chosen belt model and conditions
    :type belt_transmission_capacity: float
    :return: number of belts required
    :rtype: float
    """
    return est_power_system/belt_transmission_capacity