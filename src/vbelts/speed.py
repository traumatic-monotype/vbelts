"""Speed

"""

from math import pi

def peripheral(pulley_diam:float, pulley_rpm:float):
    """Mean peripheral velocity of the v-belt

    Args:
        pulley_diam (float): mean diameter of the pulley, mm
        pulley_rpm (float): rpm speed of the pulley, rpm
    
    Returns:
        float: linear velocity of the v-belt, m/s"""
    pulley_diam_m = pulley_diam/1000
    return (pi * (pulley_diam_m/2) * pulley_rpm)/30,2