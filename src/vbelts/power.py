"""Power

Utilities to calculate power transmission through v-belts"""

from vbelts.util import _read_csv_data, _interpol, OutOfRangeError


def belt_transmission(p_b:float, p_a: float, f_cc:float, f_cac: float):
    """Power transmission capacity by belt unit
    :param p_b: basic power, hp
    :type p_b: float
    :param p_a: additional power, hp
    :type p_a: float
    :param f_cc: length correction factor
    :type f_cc: float
    :param f_cac: contact arc correction factor
    :type f_cac: float
    :return: capacity to transmit power by belt unit
    :rtype:float
    """
    return (p_b + p_a) * f_cc * f_cac


def basic(vbelt_model:str, vbelt_profile:str, pulley_diam:float, rpm_fastest:float):
    """Select the basic power transmitted by belt unit
    :param vbelt_model: model of the v-belt, valid values are `hi_power` and `super_hc`
    :type vbelt_model: str
    :param vbelt_profile: profile of the vbelt, valid values are `A`~`D` for hi_power and `3V`, `5V` and `8V` for super_hc
    :type vbelt_profile: str
    :param pulley_diam: main diameter of the smallest pulley, mm
    :type pulley_diam: float
    :param rpm_fastest: rpm speed of the fastest pulley, rpm
    :type rpm_fastest: float
    :return: basic power transmitted, or p_b
    :rtype: float
    """
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

def additional(vbelt_model:str, vbelt_profile:str, gear_ratio_p:float, rpm_fastest:float):
    """Selects the additional power transmitted by belt unit
    :param vbelt_model: model of the v-belt, valid values are `hi_power` and `super_hc`
    :type vbelt_model: str
    :param vbelt_profile: profile of the vbelt, valid values are `A`~`D` for hi_power and `3V`, `5V` and `8V` for super_hc
    :type vbelt_profile: str
    :param gear_ratio_p: gear ratio for the pulleys in the system
    :type gear_ratio_p: float
    :param rpm_fastest: rpm speed of the fastest pulley, rpm
    :type rpm_fastest: float
    :return: additional power transmitted, or p_a
    :rtype: float
    """
    filename_pb = f'{vbelt_model}_{vbelt_profile}_pa'
    if gear_ratio_p < 1:
        gear_ratio = 1/gear_ratio_p
    else:
        gear_ratio = gear_ratio_p
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
    :param vbelt_model: model of the v-belt, valid values are `hi_power` and `super_hc`
    :type vbelt_model: str
    :param vbelt_type: type of v-belt, for more informatio see the documentation
    :type vbelt_type: str
    :return: correction factor
    :rtype: float
    """
    filename_fcc = f'{vbelt_model}_fcc'
    for line in _read_csv_data(filename_fcc):
        if line['type'] == vbelt_type:
            return float(line['fcc'])


def corr_arc_contact(max_diam:float, min_diam:float, corr_distance_pulleys:float):
    """Selects the appropriate correction factor for contact arc
    :param max_diam: major diameter for the pulleys in the system, mm
    :type max_diam: float
    :param min_diam: minor diameter for the pulleys in the system, mm
    :type min_diam: float
    :param corr_distance_pulleys: corrected distance between the pulley's center, mm
    :type corr_distance_pulleys: float
    :return: correction factor for contact arc
    :rtype: float
    """
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
