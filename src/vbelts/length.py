"""Length

Utilities for determining center distances between pulleys and belt length"""

def center_dist(min_diam:float, max_diam: float):
    """Calculate the predetermined center distance between two pulleys

    Args:
        min_diam (float): minor diameter between the pulleys, mm
        max_diam (float): major diameter between the pulleys, mm
    
    Returns:
        float: center distance for the pulleys used, mm"""
    return (3 * min_diam + max_diam)/2

def belt_calc(center:float, max_diam:float, min_diam:float):
    """Calculate the uncorrected belt length

    Args:
        center (float): distance between pulleys, mm
        min_diam (float): minor diameter between the pulleys, mm
        max_diam (float): major diameter between the pulleys, mm
    
    Returns:
        float: uncorrected belt length, mm"""
    return (2*center) + 1.57*(max_diam + min_diam) + ((max_diam - min_diam)**2)/(4 * center)
