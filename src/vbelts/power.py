"""Power

Utilities to calculate power transmission through v-belts"""

from vbelts.util import _read_csv_data, _interpol, OutOfRangeError


def belt_transmission(p_b:float, p_a: float, f_cc:float, f_cac: float):
    """Power transmission capacity by belt unit

    Args:
        p_b (float): basic power, hp
        p_a (float): additional power, hp
        f_cc (float): length correction factor
        f_cac (float): contact arc correction factor
        
    Returns:
        float: capacity to transmit power by belt unit"""
    return (p_b + p_a) * f_cc * f_cac


def basic(vbelt_model:str, vbelt_profile:str, pulley_diam:float, rpm_fastest:float):
    """Select the basic power transmitted by belt unit

    Args:
        vbelt_model (str): model of the v-belt, valid values are \'hi_power\' and \'super_hc\'
        vbelt_profile (str): profile of the v-belt, valid values are \'A\'~\'D\' and \'3V\',\'5V\' and \'8V\'
        pulley_diam (float): main diameter of the smallest pulley, mm
        rpm_fastest (float): rpm speed of the fastest pulley, rpm
    
    Returns:
        float: Basic power transmitted, or p_b"""
    filename_pb = f'{vbelt_model}_{vbelt_profile}_pb'
    for line in _read_csv_data(filename_pb):
        if line['diameter'] == pulley_diam:
            if line['rpm'] == rpm_fastest:
                return line['power_b']
            elif line['rpm'] > rpm_fastest:
                return _interpol(rpm_fastest, last_rpm, line['rpm'], last_pb, line['power_b'])
        elif line['diameter'] > pulley_diam:  # if the pulley is bigger than the standard
            if line['rpm'] == rpm_fastest:
                temp_result = line['power_b']
                if 0 < temp_result <= 0.3:
                    return temp_result, 2
                elif 0.30 < temp_result <= 1:
                    return temp_result - 0.25
                elif 1 < temp_result <= 10:
                    return temp_result - 0.5  # subtracts 0.5 hp
                elif 10 < temp_result <= 120:
                    return temp_result - 2.5  # subtracts 2.5 hp
            elif (line['rpm'] > rpm_fastest):
                temp_result = _interpol(rpm_fastest, last_rpm, line['rpm'], last_pb, line['power_b'])
                if 0 < temp_result <= 0.3:
                    return temp_result
                elif 0.30 < temp_result <= 1:
                    return temp_result - 0.25
                elif 1 < temp_result <= 10:
                    return temp_result - 0.5
                elif 10 < temp_result <= 120:
                    return temp_result - 2.5
        last_rpm = line['rpm']
        last_pb = line['power_b']
    raise OutOfRangeError('Value out of range for these parameters')

def additional(vbelt_model:str, vbelt_profile:str, gear_ratio:float, rpm_fastest:float):
    """Selects the additional power transmitted by belt unit

    Args:
        vbelt_model (str): model of v-belt, valid values are \'hi_power\' and \'super_hc\'
        vbelt_profile (str): profile of the v-belt model, valid values are \'A\'~\'D\' and \'3V\',\'5V\' and \'8V\'
        gear_ratio (float): gear ratio for the pulleys in the system
        rpm_fastest (float): rpm of the fastest pulley, rpm
    
    Returns:
        float: additional power, or p_a"""
    filename_pb = f'{vbelt_model}_{vbelt_profile}_pa'
    for line in _read_csv_data(filename_pb):
        if line['gr_low'] > gear_ratio:
            raise OutOfRangeError('Value out of range for these parameters')
        elif line['gr_low'] <= gear_ratio < line['gr_high']:
            if line['rpm'] == rpm_fastest:
                return line['power_a']
            elif line['rpm'] > rpm_fastest:
                return _interpol(rpm_fastest, last_rpm, line['rpm'], last_pa, line['power_a'])
        last_rpm = line['rpm']
        last_pa = line['power_a']
    raise OutOfRangeError('Value out of range for these parameters')


def corr_factor(vbelt_model:str, vbelt_type:str):
    """Selects the appropriate correction factor for belt length

    Args:
        vbelt_model (str): model of v-belt, valid values are \'hi_power\' and \'super_hc\'
        vbelt_type (str): type of v-belt, valid values are in the documentation
    
    Returns:
        float: correction factor"""
    filename_fcc = f'{vbelt_model}_fcc'
    for line in _read_csv_data(filename_fcc):
        if line['type'] == vbelt_type:
            return float(line['fcc'])


def corr_arc_contact(max_diam:float, min_diam:float, corr_distance_pulleys:float):
    """Selects the appropriate correction factor for contact arc

    Args:
        max_diam (float): Major diameter for the pulleys in the system, mm
        min_diam (float): Minor diameter for the pulleys in the system, mm
        corr_distance_pulleys (float): corrected distance between the pulley's center, mm
    
    Returns:
        float: correction factor for contact arc"""
    factor = (max_diam - min_diam) / corr_distance_pulleys
    last_factor = 0
    last_fcac = 1
    for line in _read_csv_data('fcac_contact_arc'):
        if line['factor'] == factor:
            return line['fcac']
        elif last_factor < factor < line['factor']:
            return _interpol(factor, last_factor, line['factor'], last_fcac, line['fcac'])
        last_factor = line['factor']
        last_fcac = line['fcac']
    raise OutOfRangeError('Value out of range for these parameters')
