"""Belt

"""

from vbelts.util import Belt

class HiPower(Belt):
    def __init__(self, est_power:float, rpm_fastest:float):
        super().__init__(est_power, rpm_fastest)
        self.boundary_a = super(HiPower, self)._fun_val(74.1950272674027, 47.215442190042, 3322, self.est_power, 50.7)
        self.boundary_b = super(HiPower, self)._fun_val(19.3889694765281, 32.2532889843209, 2151.4, self.est_power, 122.3)
        self.boundary_c = super(HiPower, self)._fun_val(4.94622293507244, 19.7301462298106, 1335.9, self.est_power, 277.35)
        self.belt_profile()
    
    
    def belt_profile(self):
        """Selects the profile for Hi Power 2 type v-belts with the estimated power and the rpm of the fastest axle
        :param power: estimated power of the system, hp
        :type power: float
        :param rpm: rotational speed of the fastest axle, rpm
        :type rpm: float
        :return: v-belt chosen profile
        :rtype: str
        """
        if self.rpm_fastest >= self.boundary_a:
            profile = 'a'
        elif self.boundary_b <= self.rpm_fastest < self.boundary_a:
            profile = 'b'
        elif self.boundary_c <= self.rpm_fastest < self.boundary_b:
            profile = 'c'
        elif self.boundary_c > self.rpm_fastest:
            profile = 'd'
        self.profile = profile


class SuperHC(Belt):
    def __init__(self, est_power:float, rpm_fastest:float):
        super().__init__(est_power, rpm_fastest)
        self.boundary_3v = super(SuperHC, self)._fun_val(40.6961726224751, 11.8866879052094, 3316.25, self.est_power, 91)
        self.boundary_5v = super(SuperHC, self)._fun_val(4.30114168431602, 3.84423100031302, 1332.74, self.est_power, 309)
        self.belt_profile()

    
    def belt_profile(self):
        """Selects the profile for Super HC type v-Belts with the estimated power and the rpm of the fastest axle
        :param power: estimated power of the system, hp
        :type power: float
        :param rpm: rotational speed of the fastest axle, rpm
        :type rpm: float
        :return: v-belt chosen profile
        :rtype: str
        """
        if self.rpm_fastest >= self.boundary_3v:
            profile = '3v'
        elif self.boundary_5v <= self.rpm_fastest < self.boundary_3v:
            profile = '5v'
        elif self.boundary_5v > self.rpm_fastest:
            profile = '8V'
        self.profile = profile
