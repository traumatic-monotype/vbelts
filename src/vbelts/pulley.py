"""Pulley"""

from vbelts.util import Pulley, Iterate, ConvergenceError
from time import time

class Driven(Pulley):
    def __init__(self, diam, vbelt_profile:str, power:float, rpm:float, iterator:Iterate=Iterate):
        super().__init__(diam, vbelt_profile, power, rpm, iterator)
    

    def driving_pulley(self, gear_ratio:float):
        """Driving pulley diameter given the driven pulley diameter
        :param driven_pulley_diam: diameter of the driven pulley, mm
        :type driven_pulley_diam: float
        :param gear_ratio: gear ratio of the pulleys in decimal form
        :type gear_ratio: float
        :return: driving pulley diameter, mm
        :rtype: float
        """
        self.min_diam = self.diam / gear_ratio
        return self.min_diam
    

    def commercial(self, gear_ratio:float, driving_pulley:float, desired_pulley_diam:int):
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
        rpm_output = self.rpm/gear_ratio
        gear_ratio_max = self.rpm/(rpm_output - range_rpm)
        gear_ratio_min = self.rpm/(rpm_output + range_rpm)
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
        rpm_out = self.rpm/gear_ratio_out
        self.diam_comm = diam_out
        self.rpm_comm = rpm_out
        return [diam_out, gear_ratio_calc, self.rpm, rpm_out]


class Driving(Pulley):
    def __init__(self, diam:float, vbelt_profile:str, power:float, rpm:float, iterator:Iterate=Iterate):
        super().__init__(diam, vbelt_profile, power, rpm, iterator)
    

    def driven_pulley(self, gear_ratio:float):
        """Driven pulley diameter given the driving pulley diameter
        :param driving_pulley_diam: diameter of the driving pulley, mm
        :type driving_pulley_diam: float
        :param gear_ratio: gear ratio of the pulleys in decimal form
        :type gear_ratio: float
        :return: driven pulley diameter, mm
        :rtype: float
        """
        return self.diam * gear_ratio