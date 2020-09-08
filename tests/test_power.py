from vbelts import power as p
import pytest

# ########### Eval func

def eval_belt_transmission(p_b, p_a, f_cc, f_cac):
    return p.belt_transmission(p_b, p_a, f_cc, f_cac)


def eval_basic(model, profile, diam, rpm):
    return p.basic(model, profile, diam, rpm)


def eval_additional(model, profile, gear_ratio, rpm):
    return p.additional(model, profile, gear_ratio, rpm)

# ########### Test func

def test_belt_transmission():
    assert eval_belt_transmission(8, 7, 1.1, 1.2) == 19.8

def test_eval_basic():
    assert eval_basic('hi_power', 'a', 65, 950) == 0.55  # diameter == pulley_diam, rpm == rpm_fastest
    assert eval_basic('hi_power', 'a', 65, 300) == 0.26  # diameter == pulley_diam, rpm > rpm_fastest
    assert eval_basic('hi_power', 'a', 68, 400) == 0.16  # diameter > pulley_diam, rpm == rpm_fastest, result <= 0.3
    assert eval_basic('hi_power', 'a', 68, 600) == 0.29  # diameter > pulley_diam, rpm == rpm_fastest, 0.3 < result <= 1
    assert eval_basic('hi_power', 'a', 68, 2200) == 0.66  # diameter > pulley_diam, rpm == rpm_fastest, 1 < result <= 10
    # ? 10 < result <= 120
    assert eval_basic('hi_power', 'a', 68, 250) == 0.28  # diameter > pulley_diam, rpm > rpm_fastest, result <= 0.3
    assert eval_basic('hi_power', 'a', 68, 1300) == 0.64  # diameter > pulley_diam, rpm > rpm_fastest, 0.3 < result <= 1
    assert eval_basic('hi_power', 'a', 68, 3100) == 0.75  # diameter > pulley_diam, rpm > rpm_fastest, 1 < result <= 10
    # ? 10 < result <= 120

def test_eval_additional():
    assert eval_additional('hi_power', 'a', 1.0, 950) == 0  # gear_low > gear_ratio, rpm == rpm_fastest
    assert eval_additional('hi_power', 'a', 1.01, 950) == 0  # gear_low  < gear_ratio <= gear_high, rpm == rpm_fastest
    assert eval_additional('hi_power', 'a', 1.05, 300) == 0.01 # gear_low < gear_ratio <= gear_high, rpm < rpm_fastest

# ########### Test fail func

def test_additional_fail():
    with pytest.raises(Exception):
        eval_additional('hi_power', 'a', 0.99, 300)
        eval_additional('a', 'a', 1, 300)
        eval_additional('hi_power', 'a', 11, 300)
        eval_additional('hi_power', 'a', 1.08, 6801)


def test_belt_transmission_fail():
    with pytest.raises(Exception):
        eval_belt_transmission('a', 8, 8, 8)


def test_eval_basic_fail():
    with pytest.raises(Exception):
        eval_basic('a', 'a', 1, 1)
        eval_basic('hi_power', 'f', 1, 1)
        eval_basic('hi_power', 'a', 64, 200)
        eval_basic('hi_power', 'a', 65, 5600)
        eval_basic('hi_power', 'a', 191, 6000)