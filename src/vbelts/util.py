"""Utilities"""

import csv
import os
import re
from abc import ABC, abstractmethod

mach_group_data = [
    ['stirrer', '1'],
    ['small blower', '1'],
    ['exhaustor', '1'],
    ['centrifugal pump', '1'],
    ['regular compressor', '1'],
    ['light conveyor belt', '1'],
    ['heavy conveyor belt', '2'],
    ['large blower', '2'],
    ['generator', '2'],
    ['transmission axle', '2'],
    ['laundry machine', '2'],
    ['press', '2'],
    ['graphical machine', '2'],
    ['positive displacement pump', '2'],
    ['sieving machine', '2'],
    ['pottery machine', '3'],
    ['bucket elevator', '3'],
    ['reciprocating compressor', '3'],
    ['mill', '3'],
    ['carpentry machine', '3'],
    ['textile machine', '3'],
    ['crusher', '4'],
    ['crane', '4'],
    ['tire shop machine', '4'],
]

drive_group_data = [
    ['normal torque ac', '1'],
    ['ring cage ac', '1'],
    ['synchronous ac', '1'],
    ['phase division ac', '1'],
    ['derivation dc', '1'],
    ['multiple cylinders combustion', '1'],
    ['high torque ac', '2'],
    ['high slipping ac', '2'],
    ['repulsion induction ac', '2'],
    ['monophasic ac', '2'],
    ['series winding dc', '2'],
    ['collector rings ac', '2'],
    ['mixed winding dc', '2'],
    ['single cylinder combustion', '2'],
    ['transmission axle', '2'],
    ['clutch', '2'],
]

class OutOfRangeError(Exception):
    """Raised when value is out of range of the list"""
    pass

class NotValidError(Exception):
    """Raised when the value passed to the function is not valid"""
    pass


class ConvergenceError(Exception):
    """Raised when the value passed to an iterator function does not converge"""
    pass


class Interpolate():
    def __init__(self, x_data, x_min, x_max, y_min, y_max):
        self.x_data = x_data
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
    
    def y_data(self):
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
        return self.y_max-((self.x_max - self.x_data)/(self.x_max - self.x_min))*(self.y_max - self.y_min)


class MinDist():
    def __init__(self, x:float, x_min:float, x_max:float):
        self.x = x
        self.x_min = x_min
        self.x_max = x_max
    
    def calc(self):
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
        dist_1 = (self.x - self.x_min)/self.x
        dist_2 = (self.x_max - self.x)/self.x
        if dist_1 < dist_2:
            return self.x_min
        elif dist_1 > dist_2:
            return self.x_max
        elif dist_1 == dist_2: # if both are equal, return the maximum
            return self.x_max
        else:
            raise ValueError


class CSV(ABC):  # abstract class
    @abstractmethod
    def read(self): pass


class Iterate(CSV):
    def __init__(self, filename:str, *row:str, interpol:Interpolate=Interpolate, m_dist:MinDist=MinDist):
        self.filename = filename
        self.row = row
        self.interpol = interpol
        self.m_dist = m_dist

    def read(self):
        """Read csv data and return a generator function
        :param filename: file name of the csv file without the extension
        :type filename: str
        :return: contents of the csv file in an ordered dictionary
        :rtype: generator
        """
        file_path = os.path.join(os.path.dirname(__file__), 'data', self.filename)  # fetch full path
        with open(f'{file_path}.csv', mode='r', encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file, quoting=csv.QUOTE_NONNUMERIC)  # not quoted values are floats
            # next(reader)
            for line in reader:
                yield line
    

    def fcc(self, vbelt_model:str, vbelt_type:str):
        self.filename = f'{vbelt_model}_fcc'
        for line in self.read():
            if line['type'] == vbelt_type:
                return float(line['fcc'])

    
    def three_rows(self, *param:float):
        """Iterate through a file with a list of three rows using two parameters and return the last one, interpolated or not
        """
        for line in self.read():
            if line[self.row[0]] == param[0]:
                if line[self.row[1]] == param[1]:
                    return (line[self.row[2]], False)  # first return the value, second need for adjusting, used in TransPower._basic()
                elif line[self.row[1]] > param[1]:
                    return (self.interpol(param[1], last_row_1, line[self.row[1]], last_row_2, line[self.row[2]]).y_data(), False)
            elif line[self.row[0]] > param[0]:
                if line[self.row[1]] == param[1]:
                    return (self.interpol(param[1], last_row_1, line[self.row[1]], last_row_2, line[self.row[2]]).y_data(), True)
                elif line[self.row[1]] > param[1]:
                    return (self.interpol(), True)
            last_row_1 = line[self.row[1]]
            last_row_2 = line[self.row[2]]
        raise OutOfRangeError('Value out of range for these parameters')


    def three_rows_choose(self, param, w_row:float):
        """Iterate through a file with a list of three rows using one parameter, chosing which row to use to return the value.
        """
        w_row -= 1
        last_row_1 = 0
        last_row_chosed = 0
        for line in self.read():
            if line[self.row[0]] == param:
                return line[self.row[w_row]]
            elif line[self.row[0]] > param:
                return self.interpol(param, last_row_1, line[self.row[0]], last_row_chosed, line[self.row[w_row]]).y_data()
            last_row_1 = line[self.row[0]]
            last_row_chosed = line[self.row[w_row]]
        raise OutOfRangeError('Value out of range for these parameters')


    def four_rows(self, *param:float):
        """Iterate through a file with a list of four rows using two parameters, the first two are a range, and return the last, interpolated or not.
        """
        for line in self.read():
            if line[self.row[0]] > param[0]:
                raise OutOfRangeError('Value out of range for these parameters')
            elif line[self.row[0]] <= param[0] < line[self.row[1]]:
                if line[self.row[2]] == param[1]:
                    return line[self.row[3]]
                elif line[self.row[2]] > param[1]:
                    return self.interpol(param[1], last_row_2, line[self.row[2]], last_row_3, line[self.row[3]]).y_data()
            last_row_2 = line[self.row[2]]
            last_row_3 = line[self.row[3]]
        raise OutOfRangeError('Value out of range for these parameters')

    
    def belt_type(self, *param:float):
        for line in self.read():
            if line[self.row[0]] == param[0]:
                last_length = 0
                if line[self.row[1]] == param[1]:  # if length == length on data
                    return (line[self.row[1]], line[self.row[2]])
                elif line[self.row[1]] > param[1]:
                    chosed_length = self.m_dist(param[1], last_length, line[self.row[1]]).calc()
                    # check what length and type was chosen and return them
                    if chosed_length == line[self.row[1]]:
                        chosed_type = line[self.row[2]]
                    else:
                        chosed_type = last_type
                    return (chosed_length, chosed_type)
            last_length = line[self.row[1]]
            last_type = line[self.row[2]]
        raise OutOfRangeError('Value out of range for these')


class Device():
    def __init__(self, name:str, li_group:list):
        self.name = name
        self.li_group = li_group
        self.group = self.grp()
    

    def grp(self):
        data_regex = re.compile(r'(\w+).?(\w+)?.?(\w+)?')
        try:
            for item in self.li_group:
                m = data_regex.search(item[0])  # search the first item
                if self.name in m.group(0):
                    return int(item[1])
        except:  # stop the execution if nothing is found
            raise ValueError


class Motor(Device):
    def __init__(self, name:str, power:float, li_group:list=drive_group_data):
        super().__init__(name, li_group)
        self.power = power


class Machine(Device):
    def __init__(self, name:str, hours_service:float, li_group:list=mach_group_data):
        super().__init__(name, li_group)
        self.hours_service = hours_service


class Belt():
    def __init__(self, est_power:float, rpm_fastest:float):
        self.est_power = est_power
        self.rpm_fastest = rpm_fastest


    def _fun_val(self, a:float, b:float, c:float, x:float, upper:float):
        """X for a mathematical function with a linear (ax + b) and a constant part
        :param a: a coefficient for the linear part of the function
        :type a: float
        :param b: b coefficient for the linear part of the function
        :type b: float
        :param c: y value for the constant part of the function
        :type c: float
        :param x: input value of x
        :type x: float
        :param upper: upper limit of the linear function in the y axis
        :type upper: float
        :return: y value for the math function
        :rtype: float
        """
        if x < upper:
            eq = a * x + b
            return abs(eq)
        # if the value is within the constant range
        elif x >= upper:
            eq = c
            return eq


class Pulley(ABC):
    def __init__(self, diam, vbelt_profile:str, power:float, rpm:float, iterator:Iterate=Iterate):
        self.diam = diam
        self.vbelt_profile = vbelt_profile
        self.power = power
        self.rpm = rpm
        self.filename = f'{self.vbelt_profile}_diam'
        self.iterator = iterator

    # @abstractmethod
    # def min_diam(self): pass


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
