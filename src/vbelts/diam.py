"""Pulley diameter utilities (REVIEW)

Utilities for determining pulley mininimum diameter and related variables"""

from vbelts.util import _interpol, _read_csv_data, Interpol, CSVData, Data, OutOfRangeError, NotValidError, ConvergenceError
from time import time

    
class MinDiam():
    def __init__(self, vbelt_model:str, power:float, rpm:float):
        self.vbelt_model = vbelt_model
        self.power = power
        self.rpm = rpm
        self.filename = f'{self.vbelt_model}_diam'

    
    def calc(self):
        return (Data(self.filename, 'rpm_low', 'rpm_high', 'engine_power', 'diam').iterate_4rows(self.rpm, self.power)*25.4)


class Define():
    def __init__(self, gear_ratio:float):
        self.gear_ratio = gear_ratio

    
    def driven_pulley(self, driving_pulley_diam:float):
        """Driven pulley diameter given the driving pulley diameter
        :param driving_pulley_diam: diameter of the driving pulley, mm
        :type driving_pulley_diam: float
        :param gear_ratio: gear ratio of the pulleys in decimal form
        :type gear_ratio: float
        :return: driven pulley diameter, mm
        :rtype: float
        """
        self.type_pulley = 'driven'
        return driving_pulley_diam * self.gear_ratio
    

    def driving_pulley(self, driven_pulley_diam:float):
        """Driving pulley diameter given the driven pulley diameter
        :param driven_pulley_diam: diameter of the driven pulley, mm
        :type driven_pulley_diam: float
        :param gear_ratio: gear ratio of the pulleys in decimal form
        :type gear_ratio: float
        :return: driving pulley diameter, mm
        :rtype: float
        """
        self.type_pulley = 'driving'
        self.diameter = driven_pulley_diam / self.gear_ratio


def driven_commercial(gear_ratio:float, rpm_input:float, driving_pulley:float, desired_pulley_diam:int):
    """Selects an approximate to the commercial diameter of a pulley through convergence
    :param gear_ratio: reference gear ratio in decimal form
    :type gear_ratio: float
    :param rpm_input: rotational speed of the driving axle, rpm
    :type rpm_input: float
    :param driving_pulley: diameter of the driving pulley, mm
    :type driving_pulley: float
    :param desired_pulley_diam: desired diameter of the driven pulley, mm
    :type desired_pulley_diam: int
    :return: a list with the calculated driven diameter, new gear ratio for this diameter, driving and driven speed of the axles
    :rtype: list
    """
    # calculate gear ratio range
    range_rpm = 100
    rpm_output = rpm_input/gear_ratio
    gear_ratio_max = rpm_input/(rpm_output - range_rpm)
    gear_ratio_min = rpm_input/(rpm_output + range_rpm)
    error_min = 0.01
    driven_pulley = gear_ratio * driving_pulley
    diam_calc = driven_pulley

    # iterate
    error = 1
    t_i = time()
    while error > error_min:
        gear_ratio_calc = diam_calc/driving_pulley
        # control iteration parameters
        if gear_ratio_calc > gear_ratio_max:
            diam_calc -= diam_calc * error * 0.01
        elif gear_ratio_calc < gear_ratio_min:
            diam_calc += diam_calc * error
        else:
            diam_calc *= error
        error = 1-(diam_calc/desired_pulley_diam)
        # control for infinite loops
        t_f = time()
        elapsed_time = t_f - t_i
        if elapsed_time > 4:
            raise ConvergenceError('The function could not reach convergence, try again with a lower value')
    
    # recalculate rpm_output
    base = 10
    diam_out = base * round(diam_calc/base)  # round the number to nearest 5 integer
    gear_ratio_out = diam_out/driving_pulley
    rpm_out = rpm_input/gear_ratio_out
    return [diam_out, gear_ratio_calc, rpm_input, rpm_out]
