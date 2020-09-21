"""
Length
======

Parei nesse
"""

from vbelts.util import Interpolate, Iterate, OutOfRangeError
from abc import ABC

h_factor = {0:0, 0.02:0.01, 0.04:0.02, 0.06:0.03, 0.08:0.04, 0.1:0.05, 0.12:0.06, 0.14:0.07, 0.16:0.08, 0.18:0.09, 0.2:0.1, 0.21:0.11, 0.23:0.12, 0.25:0.13, 0.27:0.14, 0.29:0.15, 0.3:0.16, 0.32:0.17, 0.34:0.18, 0.35:0.19, 0.37:0.2, 0.39:0.21, 0.4:0.22, 0.41:0.23, 0.43:0.24, 0.44:0.25, 0.46:0.26, 0.47:0.27, 0.48:0.28, 0.5:0.29, 0.51:0.3}


class Dist(ABC):
    def __init__(self, min_diam:float, maj_diam:float):
        self.min_diam = min_diam
        self.maj_diam = maj_diam
        self._c_uc()
        self._l_uc()

    
    def _c_uc(self):
        """Uncorrected center distance"""
        self.center_uncorr = (3 * self.min_diam + self.maj_diam)/2
    

    def _l_uc(self):
        """Uncorrected belt length"""
        self.l_uncorr = 2 * self.center_uncorr + 1.57 * (self.maj_diam + self.min_diam) + ((self.maj_diam - self.min_diam)**2/(4 * self.center_uncorr))


class PulleyBelt(Dist):  # PROBLEMA NA VARIAVEL BELT, ESTA PASSANDO O NOME
    r"""PulleyBelt class calculates the corrected belt length and the corrected center distance.

    Parameters
    ----------
    min_diam : float
        Smallest pulley, [mm]
    maj_diam : float
        Largest pulley, [mm]
    belt : str
        Belt model, [-]
    b_profile : str
        Belt profile, [-]
    
    Methods
    -------
    l_c()
        Returns the corrected belt length and belt type, [mm] [-]
    c_c()
        Returns the corrected center distance, [mm]
    
    Attributes
    ----------
    l_corr : float
        V-Belt corrected length, [mm]
    b_type : str
        V-Belt selected type, [-]
    c_corr : float
        Pulley corrected center length, [mm]


    Notes
    -----
    All the information [#]_ is available online. The valid entries for `belt` and `b_profile` are in the :ref:`Model Profile <vbelt_model_profile>` data section.

    Examples
    --------
    >>> dist = vbelts.length.PulleyBelt(130, 240, 'HiPower', 'a')
    >>> dist.l_c()

    >>> dist.c_c()

    References
    ----------
    .. [#] Claudino Alves, Claudemir. "Transmissão por Correias - Dimensionamento Atividade 2". **Fatec Itaquera**. Accessed September 16, 2020, http://claudemiralves.weebly.com/uploads/3/8/6/2/3862918/dimen._de_correias.pdf.

    """
    def __init__(self, min_diam:float, maj_diam:float, belt:str, b_profile:str, iterator:Iterate=Iterate, interpol:Interpolate=Interpolate):  # inject the objects inside the class
        super().__init__(min_diam, maj_diam)
        self.belt = belt
        self.b_profile = b_profile
        self.iterator = iterator
        self.interpol = interpol
        self.corr_dict = h_factor
        self._l_c()
        self._h_factor()
        self._l_a()


    def _l_c(self):
        """Calculates the corrected v-belt length and type"""
        self.l_corr, self.b_type = self.iterator(f'{self.belt}_length', 'profile', 'length', 'type').belt_type(self.b_profile, self.l_uncorr)
    

    def l_c(self):
        return (self.l_corr, self.b_type)
    
    
    def _h_factor(self):
        """Calculates and selects the appropriate correction factor for the center distance between pulleys"""
        adim_factor = (self.maj_diam - self.min_diam)/self.l_corr
        for key in self.corr_dict:
            last_factor = 0
            if key == adim_factor:
                self._h = self.corr_dict.get(key)
            elif key > adim_factor:
                self._h = self.interpol(adim_factor, last_factor, key, self.corr_dict.get(last_factor), self.corr_dict.get(key)).y_data()
            last_factor = key
        if self._h == None:
            raise OutOfRangeError('Value out of range for these parameters')


    def _l_a(self):
        """Corrected belt length for commercial belts"""
        self._l_adj = self.l_corr - 1.57 * (self.maj_diam - self.min_diam)
    

    def c_c(self):
        """Corrected center distance for commercial belts
        :param l_a: corrected belt length, mm
        :type l_a: float
        :param h: correction factor for the center distance between pulleys
        :type: float
        :param max_diam: major diameter of the pulleys, mm
        :type max_diam: float
        :param min_diam: minor diameter of the pulleys, mm
        :type min_diam: float
        :return: corrected center distance between the pulleys, mm
        :rtype: float
        """
        self.c_corr = (self._l_adj - self._h *(self.maj_diam - self.min_diam))/2
        return self.c_corr