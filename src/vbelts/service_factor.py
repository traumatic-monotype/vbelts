"""Service Factor

This module calculate the service factor for v-belts."""

import re

mach_group_data = [
    ['stirrer', '1'],
    ['small blower', '1'],
    ['exhaustor', '1'],
    ['centrifugal pump', '1'],
    ['regular compressor', '1'],
    ['light conveyor', '1'],
    ['heavy conveyor', '1'],
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
    ['normal torque', '1'],
    ['ring cage', '1'],
    ['synchronous', '1'],
    ['phase division', '1'],
    ['derivation', '1'],
    ['multiple cylinder', '1'],
    ['high torque', '2'],
    ['high slipping', '2'],
    ['repulsion induction', '2'],
    ['monophasic', '2'],
    ['series winding', '2'],
    ['collector rings', '2'],
    ['mixed winding', '2'],
    ['single cylinder', '2'],
    ['transmission axle', '2'],
    ['clutch', '2'],
]


def _group(entry, comp_list):
    data_regex = re.compile(entry)
    for item in comp_list:
        m = data_regex.search(item[0])  # search the first item
        if m is not None:
            return int(item[1])
    raise ValueError # stop the execution if nothing is found

def _sf_partial(mach_group, service_hours):
    if mach_group == 1:
        if 0 < service_hours <= 5:
            sf_part = 1.0
        elif 5 < service_hours <= 10:
            sf_part = 1.1
        elif 10 < service_hours <= 24:
            sf_part = 1.2
    elif mach_group == 2:
        if 0 < service_hours <= 5:
            sf_part = 1.1
        elif 5 < service_hours <= 10:
            sf_part = 1.2
        elif 10 < service_hours <= 24:
            sf_part = 1.3
    elif mach_group == 3:
        if 0 < service_hours <= 5:
            sf_part = 1.2
        elif 5 < service_hours <= 10:
            sf_part = 1.3
        elif 10 < service_hours <= 24:
            sf_part = 1.4
    elif mach_group == 4:
        if 0 < service_hours <= 5:
            sf_part = 1.3
        elif 5 < service_hours <= 10:
            sf_part = 1.4
        elif 10 < service_hours <= 24:
            sf_part = 1.5
    return sf_part

def _calc(mach_group, drive_group, _sf_p):
    if mach_group == 1 and drive_group == 2:
        result = _sf_p + 0.1
    elif mach_group == 2 and drive_group == 2:
        result = _sf_p + 0.1
    elif mach_group == 3 and drive_group == 2:
        if _sf_p == 1.4:
            result = _sf_p + 0.1
        else:
            result = _sf_p + 0.2
    elif mach_group == 4 and drive_group == 2:
        if _sf_p == 1.4:
            result = _sf_p + 0.2
        else:
            result = _sf_p + 0.3
    else:
        result = _sf_p
    return round(result, 1)

        
def service_factor(machine:str, drive:str, hours_service:float, mach_list=mach_group_data, drive_list=drive_group_data):
    """Calculate the service factor

    Args:
        machine (str): The type of machine driven. Valid arguments are:
            stirrer, small blower, exhaustor, centrifugal pump, regular compressor, light conveyor,
            heavy conveyor, large blower, generator, transmission axle, laundry machine, press, graphical machine,
            positive displacement pump, sieving machine, pottery machine, bucket elevator, reciprocating compressor,
            mill, carpentry machine, textile machine, crusher, crane, tire shop machine
        drive (str): The type of drive for the machine. Valid arguments are:
            ac motors: normal torque, ring cage, synchronous, phase division, high torque, high slipping, repulsion induction,
                       monophasic
            dc motors: derivation, series winding, mixed winding
            combustion engine: multiple cylinder, single cylinder
            transmission axle
            clutch
    
    Kargs:
        mach_list: Variable for valid machine list, already configured.
        drive_list: Variable for valid drive list, already configured.

    Returns:
        float: the service factor"""

    machine_group = _group(machine, mach_list)
    drive_group = _group(drive, drive_list)
    precalc = _sf_partial(machine_group, hours_service)
    result = _calc(machine_group, drive_group, precalc)
    return result
