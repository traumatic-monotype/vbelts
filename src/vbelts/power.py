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
                return round(_interpol(rpm_fastest, last_rpm, line['rpm'], last_pb, line['power_b']), 2)
        elif line['diameter'] > pulley_diam:  # if the pulley is bigger than the standard
            if line['rpm'] == rpm_fastest:
                temp_result = line['power_b']
                if 0 < temp_result <= 0.3:
                    return round(temp_result, 2)
                elif 0.30 < temp_result <= 1:
                    return round(temp_result - 0.25, 2) 
                elif 1 < temp_result <= 10:
                    return round(temp_result - 0.5, 2)  # subtracts 0.5 hp
                elif 10 < temp_result <= 120:
                    return round(temp_result - 2.5, 2)  # subtracts 2.5 hp
            elif line['rpm'] > rpm_fastest:
                temp_result = round(_interpol(rpm_fastest, last_rpm, line['rpm'], last_pb, line['power_b']), 2)
                print(temp_result)
                if 0 < temp_result <= 0.3:
                    return round(temp_result, 2)
                elif 0.30 < temp_result <= 1:
                    return round(temp_result - 0.25, 2)
                elif 1 < temp_result <= 10:
                    return round(temp_result - 0.5, 2)
                elif 10 < temp_result <= 120:
                    return round(temp_result - 2.5, 2)
        last_rpm = line['rpm']
        last_pb = line['power_b']
    raise OutOfRangeError('Value out of range for these parameters')

def additional(vbelt_model:str, vbelt_profile:str, gear_ratio:float, rpm_fastest:float):
    filename_pb = f'{vbelt_model}_{vbelt_profile}_pa'
    for line in _read_csv_data(filename_pb):
        if line['gr_low'] > gear_ratio:
            raise OutOfRangeError('Value out of range for these parameters')
        elif line['gr_low'] <= gear_ratio < line['gr_high']:
            if line['rpm'] == rpm_fastest:
                return line['power_a']
            elif line['rpm'] > rpm_fastest:
                return round(_interpol(rpm_fastest, last_rpm, line['rpm'], last_pa, line['power_a']), 2)
        last_rpm = line['rpm']
        last_pa = line['power_a']
    raise OutOfRangeError('Value out of range for these parameters')
    
