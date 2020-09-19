"""
Power  (REVIEW)
=====

"""

from vbelts.util import Iterate, OutOfRangeError


class EstPower():
    def __init__(self, engine_power, drive_group, machine_group, hours_service):
        self.engine_power = engine_power
        self.drive_group = drive_group
        self.machine_group = machine_group
        self.hours_service = hours_service
        self._sf()
    

    def _sf(self):
        """Calculate the service factor [1]_ based on the machine driven, the drive engine and hours of service per day.

        :param machine: type of machine driven, for valid values see the documentation
        :type machine: str
        :param drive: type of drive for the machine, for valid values see the documentation
        :type drive: str
        :param hours_service: hours of service of the system
        :type hours_service: float
        :return: service factor
        :rtype: float

        Example
        -------
        >>> service_factor(machine='centrifugal pump', drive='diesel multiple cylinder', hours_service=8)
        1.1
        >>> service_factor(machine='reciprocating compressor', drive='high torque', hours_service=11)
        1.5
        
        References
        ----------
        .. [1] Megadyne. 2016."V-BELTS: Rubber V-belts", **Vermeire webshop**. Accessed September 14, 2020, http://shop.vermeire.com/inc/Doc/courroies/megadyne/2016/v_belts_jan_2016.pdf
        """
        # calculate service_factor partial
        if self.machine_group == 1:
            if 0 < self.hours_service <= 5:
                sf_part = 1.0
            elif 5 < self.hours_service <= 10:
                sf_part = 1.1
            elif 10 < self.hours_service <= 24:
                sf_part = 1.2
        elif self.machine_group == 2:
            if 0 < self.hours_service <= 5:
                sf_part = 1.1
            elif 5 < self.hours_service <= 10:
                sf_part = 1.2
            elif 10 < self.hours_service <= 24:
                sf_part = 1.3
        elif self.machine_group == 3:
            if 0 < self.hours_service <= 5:
                sf_part = 1.2
            elif 5 < self.hours_service <= 10:
                sf_part = 1.3
            elif 10 < self.hours_service <= 24:
                sf_part = 1.4
        elif self.machine_group == 4:
            if 0 < self.hours_service <= 5:
                sf_part = 1.3
            elif 5 < self.hours_service <= 10:
                sf_part = 1.4
            elif 10 < self.hours_service <= 24:
                sf_part = 1.5
        # calculate service_factor additional and final
        if self.machine_group == 1 and self.drive_group == 2:
            result = sf_part + 0.1
        elif self.machine_group == 2 and self.drive_group == 2:
            result = sf_part + 0.1
        elif self.machine_group == 3 and self.drive_group == 2:
            if sf_part == 1.4:
                result = sf_part + 0.1
            else:
                result = sf_part + 0.2
        elif self.machine_group == 4 and self.drive_group == 2:
            if sf_part == 1.4:
                result = sf_part + 0.2
            else:
                result = sf_part + 0.3
        else:
            result = sf_part
        self.service_factor = result

    
    def calc(self):
        """Estimated power to run the pulley system
        :param engine_power: engine power, hp
        :type engine_power: float
        :param serv_factor: calculated service factor
        :type serv_factor: float
        :return: estimated power, hp
        :rtype: float
        """
        pp = self.engine_power * self.service_factor
        return pp


class TransPower():
    def __init__(self, vbelt_model:str, vbelt_profile:str, vbelt_type:str, est_power:float, gear_ratio:float, belt_length_corr:float, min_diam:float, maj_diam:float, rpm:float, iterator:Iterate=Iterate):
        self.b_model = vbelt_model
        self.b_profile = vbelt_profile
        self.b_type = vbelt_type
        self.est_power = est_power
        self.gear_ratio = gear_ratio
        self.l_corr = belt_length_corr
        self.min_diam = min_diam
        self.maj_diam = maj_diam
        self.rpm = rpm
        self.iterator = iterator
        self._fcc()
        self._basic()
        self._additional()
        self._fcac()
    

    def _fcc(self):
        """Selects the appropriate correction factor for belt length. The valid entries for `vbelt_model` are in the :ref:`Data/V-belt Model and Profile <vbelt_model_profile>`, for the `vbelt_type` are in the :ref:`Data/V-belt Type <vbelt_types>`.

        :param vbelt_model: model of the v-belt
        :type vbelt_model: str
        :param vbelt_type: type of v-belt
        :type vbelt_type: str
        :return: correction factor [-]
        :rtype: float

        Notes
        -----
        The data [#]_, is available as a pdf.

        Examples
        --------
        >>> power.corr_factor('super_hc', '3V900')
        1.07
        >>> power.corr_factor('hi_power', 'A-32')
        0.8

        References
        ----------
            .. [#] Claudino Alves, Claudemir. "Transmissão por Correias - Dimensionamento Atividade 2". **Fatec Itaquera**. Accessed September 16, 2020, http://claudemiralves.weebly.com/uploads/3/8/6/2/3862918/dimen._de_correias.pdf."""
        filename_fcc = f'{self.b_model}_fcc'
        for line in self.iterator(filename_fcc).read():
            if line['type'] == self.b_type:
                self.fcc = float(line['fcc'])
    

    def _basic(self):
        """Select the basic power transmitted by belt unit. The valid entries for `vbelt_model` and `vbelt_profile` are in the :ref:`Data <vbelt_model_profile>` section.
        
        :param vbelt_model: model of the v-belt
        :type vbelt_model: str
        :param vbelt_profile: profile of the vbelt
        :type vbelt_profile: str
        :param pulley_diam: main diameter of the smallest pulley [mm]
        :type pulley_diam: float
        :param rpm_fastest: rpm speed of the fastest pulley [rpm]
        :type rpm_fastest: float
        :return: basic power transmitted or p_b [hp]
        :rtype: float

        Notes
        -----
        The data [#]_, is available as a pdf.

        Examples
        --------
        >>> vbelts.power.basic(vbelt_model='hi_power', vbelt_profile='a', pulley_diam=180, rpm_fastest=900)
        4.35999
        >>> vbelts.power.basic(vbelt_model='super_hc', vbelt_profile='3v', pulley_diam=180, rpm_fastest=900)
        5.02

        References
        ----------
        .. [#] Claudino Alves, Claudemir. "Transmissão por Correias - Dimensionamento Atividade 2". **Fatec Itaquera**. Accessed September 16, 2020, http://claudemiralves.weebly.com/uploads/3/8/6/2/3862918/dimen._de_correias.pdf
        """
        filename_pb = f'{self.b_model}_{self.b_profile}_pb'
        temp_result, adjust = self.iterator(filename_pb, 'diameter', 'rpm', 'power_b').three_rows(self.min_diam, self.rpm)
        # result adjusting for interpolation
        if adjust:
            if 0.3 < temp_result <= 1:
                self.p_basic = temp_result - 0.25
            elif 1 < temp_result <= 10:
                self.p_basic = temp_result - 0.5
            elif 10 < temp_result <= 120:
                self.p_basic = temp_result - 2.5
        else:
            self.p_basic = temp_result
    

    def _additional(self):
        """Selects the additional power transmitted by belt unit. The valid entries for `vbelt_model` and `vbelt_profile` are in the :ref:`Data <vbelt_model_profile>` section.

        :param vbelt_model: model of the v-belt
        :type vbelt_model: str
        :param vbelt_profile: profile of the vbelt
        :type vbelt_profile: str
        :param gear_ratio_p: gear ratio for the pulleys in the system [-]
        :type gear_ratio_p: float
        :param rpm_fastest: rpm speed of the fastest pulley [rpm]
        :type rpm_fastest: float
        :return: additional power transmitted, or p_a [hp]
        :rtype: float

        Notes
        -----
        The data [#]_, is available as a pdf.

        Examples
        --------
        >>> vbelts.power.additional(vbelt_model='hi_power', vbelt_profile='a', gear_ratio_p=1.05, rpm_fastest=900)
        0.036667
        >>> vbelts.power.additional(vbelt_model='super_hc', vbelt_profile='3v', gear_ratio_p=0.8, rpm_fastest=900)
        0.11

        References
        ----------
            .. [#] Claudino Alves, Claudemir. "Transmissão por Correias - Dimensionamento Atividade 2". **Fatec Itaquera**. Accessed September 16, 2020, http://claudemiralves.weebly.com/uploads/3/8/6/2/3862918/dimen._de_correias.pdf.
        """
        filename_pa = f'{self.b_model}_{self.b_profile}_pa'
        # checking if gear_ratio is below one and adjust
        if self.gear_ratio < 1:
            gear_ratio_corr = 1/self.gear_ratio
        else:
            gear_ratio_corr = self.gear_ratio
        self.p_add = self.iterator(filename_pa, 'gr_low', 'gr_high', 'rpm', 'power_a').four_rows(gear_ratio_corr, self.rpm)


    def _fcac(self):
        """Selects the appropriate correction factor for contact arc.

        :param max_diam: major diameter for the pulleys in the system, mm
        :type max_diam: float
        :param min_diam: minor diameter for the pulleys in the system, mm
        :type min_diam: float
        :param corr_distance_pulleys: corrected distance between the pulley's center, mm
        :type corr_distance_pulleys: float
        :return: correction factor for contact arc
        :rtype: float

        Notes
        -----
        The data [#]_, is available as a pdf.

        Examples
        --------
        >>> power.corr_arc_contact(320, 130, 1100)
        0.9754545454545455

        References
        ----------
        .. [#] Claudino Alves, Claudemir. "Transmissão por Correias - Dimensionamento Atividade 2". **Fatec Itaquera**. Accessed September 16, 2020, http://claudemiralves.weebly.com/uploads/3/8/6/2/3862918/dimen._de_correias.pdf
        """
        factor = (self.maj_diam - self.min_diam) / self.l_corr
        self.fcac = self.iterator('fcac_contact_arc', 'factor', 'contact_arc', 'fcac').three_rows_choose(factor, 3)


    def belt_qty(self):
        """Power transmission capacity by belt unit.

        :param p_b: basic power [hp]
        :type p_b: float
        :param p_a: additional power [hp]
        :type p_a: float
        :param f_cc: length correction factor [-]
        :type f_cc: float
        :param f_cac: contact arc correction factor [-]
        :type f_cac: float
        :return: capacity to transmit power by belt unit [hp]
        :rtype: float
        
        Notes
        -----
        The formula for belt transmission capacity [#]_, `P_a` is:

        .. math::
        P_a = (P_b + P_a) * f_{cc} * f_{cac}


        Examples
        --------
        >>> vbelts.power.belt_transmission(p_b=1.5, p_a=0.2, f_cc=1.0, f_cac=0.7)
        1.19


        References
        ----------
        .. [#] Oleostatic. 2016. "Correas Trapeciales Convencionales". **Ingineria Mecánica**. Accessed September 14, 2020, http://ocw.uc3m.es/ingenieria-mecanica/diseno-mecanico-1/material_clase/ocw_catalogo_correas
        """
        belt_transmission_capacity = (self.p_basic + self.p_add) * self.fcc * self.fcac
        """Number of belts to transmit the estimated power
        :param est_power_system: estimated power to run the pulley system, hp
        :type est_power_system: float
        :param belt_transmission_capacity: power transmission capacity per chosen belt profile and conditions
        :type belt_transmission_capacity: float
        :return: number of belts required
        :rtype: float
        """
        return self.est_power / belt_transmission_capacity
