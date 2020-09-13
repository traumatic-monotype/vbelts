"""Speed"""
from math import pi

def peripheral(pulley_diam:float, pulley_rpm:float):
    """Mean peripheral velocity of the v-belt
    :param pulley_diam: mean diameter of the pulley, mm
    :type pulley_diam: float
    :param pulley_rpm: rpm speed of the pulley, rpm
    :type pulley_rpm: float
    :return: linear velocity of the v-belt, m/s
    :rtype: float
    """
    pulley_diam_m = pulley_diam/1000
    return (pi * (pulley_diam_m/2) * pulley_rpm)/30,2