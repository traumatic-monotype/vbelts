import pytest
from vbelts import force as f

# ########### Eval func

def eval_torque(power, rpm_pulley):
    return f.torque(power, rpm_pulley)

def eval_forces(m_torque, diam_driving, diam_driven, corr_distance_pulleys, belt_material, pulley_material):
    return f._forces(m_torque, diam_driving, diam_driven, corr_distance_pulleys, belt_material, pulley_material)

def eval_axle(m_torque, diam_driving, diam_driven, corr_distance_pulleys, belt_material, pulley_material):
    return f.axle(m_torque, diam_driving, diam_driven, corr_distance_pulleys, belt_material, pulley_material)

def eval_tangential(m_torque, diam_driving, diam_driven, corr_distance_pulleys, belt_material, pulley_material):
    return f.tangential(m_torque, diam_driving, diam_driven, corr_distance_pulleys, belt_material, pulley_material)

# ######## Test func

def test_eval_torque():
    assert eval_torque(5, 500) == 7.16

def test_eval_forces():
    assert eval_forces(7.16, 450, 200, 2600, 'rubber', 'steel') == [8.9, 40.73, 49.63]