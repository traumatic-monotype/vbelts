from vbelts import profile as prf
from vbelts import service_factor as sf
import pytest

def eval_service_factor(mach, dr, sh):
    return sf(mach, dr, sh)

def eval_profile(power, rpm):
    return prf.hi_power_2(power, rpm)

def test_service_factor():
    assert eval_service_factor('stirrer','normal',3) == 1.0
    assert eval_service_factor('stirrer','normal',6) == 1.1
    assert eval_service_factor('stirrer','normal',11) == 1.2
    assert eval_service_factor('stirrer','high',3) == 1.1
    assert eval_service_factor('stirrer','high',6) == 1.2
    assert eval_service_factor('stirrer','high',11) == 1.3

def test_profile():
    assert eval_profile(8,540) == 'B'
