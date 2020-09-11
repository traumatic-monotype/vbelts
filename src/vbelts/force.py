"""Force
"""
from math import pi, exp
from vbelts.util import _read_csv_data, _interpol, OutOfRangeError

def torque(power:float, rpm_pulley:float):
    """Torque of the pulley

    Args:
        power (float): power of the system, hp
        rpm_pulley (float): rotational speed of the pulley, rpm

    Returns:
        float: torque of the pulley, kgf*m"""
    return (2250*power)/(pi*rpm_pulley)


def _contact_arc_rad(factor:float):
    """Contact arc for a given factor searched and interpolated from a csv data table

    Args:
        factor (float): factor (D-d)/Ca

    Returns:
        float: angle of contact of the v-belt, rad"""
    last_factor = 0
    last_contact_arc = 180
    for line in _read_csv_data('fcac_contact_arc'):
        if line['factor'] == factor:
            contact_arc = line['contact_arc']
            return (pi*contact_arc/180)
        elif last_factor < factor < line['factor']:
            contact_arc = _interpol(factor, last_factor, line['factor'], last_contact_arc, line['contact_arc'])
            return (pi*contact_arc/180)
        last_factor = line['factor']
        last_contact_arc = line['contact_arc']
    raise OutOfRangeError('Value out of range for these parameters')


def _fric_coef(belt_material:str, pulley_material:str):
    """Select coefficient of friction from csv data

    Args:
        belt_material (string): belt material, valid values are \'polyurethane\', \'nylon\' and \'rubber\'
        pulley_material (string): pulley material, valid values are \'steel\' and \'aluminum\'
    
    Returns:
        float: friction coefficient"""
    for line in _read_csv_data('fric_coef'):
        if line['belt_material'] == belt_material:
            if line['pulley_material'] == pulley_material:
                return line['fric_coef']
    raise OutOfRangeError('Value out of range for these parameters')


def _forces(m_torque:float, diam_driving:float, diam_driven:float, corr_distance_pulleys:float, belt_material:str, pulley_material:str):
    """Main forces of the pulley-belt system

    Args:
        m_torque (float): torque of the system, kgf*m
        diam_driving (float): diameter of the driving pulley, mm
        diam_driven (float): dimater of the driven pulley, mm
        corr_distance_pulleys (float): corrected distance between the pulley's center, mm
        belt_material (string): belt material, valid values are \'polyurethane\', \'nylon\' and \'rubber\'
        pulley_material (string): pulley material, valid values are \'steel\' and \'aluminum\'
    
    Returns:
        list: three main force values, f_0, f_1 and f_z, in N"""
    f_u = (m_torque * 9.81)/(diam_driving/(2 * 1000))
    factor_contact = (max(diam_driving, diam_driven) - min(diam_driving, diam_driven))/corr_distance_pulleys
    carc_rad = _contact_arc_rad(factor_contact)
    mu = _fric_coef(belt_material, pulley_material)    
    f_0 = f_u/(exp(mu*carc_rad)-1)
    f_1 = f_u*(exp(mu*carc_rad)/(exp(mu * carc_rad)-1))
    f_z = f_u*(exp(mu*carc_rad)+1)/(exp(mu * carc_rad)-1)
    return [f_0, f_1, f_z]


def axle(m_torque:float, diam_driving:float, diam_driven:float, corr_distance_pulleys:float, belt_material:str, pulley_material:str):
    """Axle force on the pulley

    Args:
        m_torque (float): torque of the system, kgf*m
        diam_driving (float): diameter of the driving pulley, mm
        diam_driven (float): dimater of the driven pulley, mm
        corr_distance_pulleys (float): corrected distance between the pulley's center, mm
        belt_material (string): belt material, valid values are \'polyurethane\', \'nylon\' and \'rubber\'
        pulley_material (string): pulley material, valid values are \'steel\' and \'aluminum\'
    
    Returns:
        float: axle force on the pulley, kgf"""
    return (_forces(m_torque, diam_driving, diam_driven, corr_distance_pulleys, belt_material, pulley_material)[2])/9.81


def tangential(m_torque:float, diam_driving:float, diam_driven:float, corr_distance_pulleys:float, belt_material:str, pulley_material:str):
    """Tangential force on the v-belt

    Args:
        m_torque (float): torque of the system, kgf*m
        diam_driving (float): diameter of the driving pulley, mm
        diam_driven (float): dimater of the driven pulley, mm
        corr_distance_pulleys (float): corrected distance between the pulley's center, mm
        belt_material (string): belt material, valid values are \'polyurethane\', \'nylon\' and \'rubber\'
        pulley_material (string): pulley material, valid values are \'steel\' and \'aluminum\'
    
    Returns:
        float: tangential force on the v-belt, kgf"""
    ft_1, ft_2 = _forces(m_torque, diam_driving, diam_driven, corr_distance_pulleys, belt_material, pulley_material)[:2]
    return (ft_1 - ft_2)/9.81