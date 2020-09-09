# vbelts

## What is vbelts?

vbelts is an open-source python package that provides utilities for constants and tables used in v-belt dimensioning.

## Installation

Run the following to install:

```shell
$ pip install vbelts
```

## Usage

The module is separated into submodules that provide specific functionality. To import vbelts use:

```python
import vbelts
```

### service_factor

The service factor of the v-belts is defined by the driven machine, the  ```machine``` argument, the drive type, ```drive``` argument and the hours of service per day that the system will be in use, ```hours_service``` argument. The syntax is the following, returning a float number, the service factor:

```python
>>> vbelts.service_factor(machine,drive,hours_service)
(float)
```

The arguments ```machine``` and ```drive``` can take only valid entries, meanwhile the ```hours_service``` can assume any value from, but not including, 0 to 24. The machines and drives listed here are examples of common items. If the equipment you need is not listed here, choose the most similar. The following sections contain lists with the valid entries for both arguments. As an example, the service factor is calculated for a centrifugal pump driven by a normal torque ac motor with normal torque used 8 hours a day:

```python
>>> vbelts.service_factor('centrifugal pump','normal torque', 8)
1.1
```

#### ```machine``` valid entries

* ```stirrer```
* ```small blower```
* ```exhaustor```
* ```centrifugal pump```
* ```regular compressor```
* ```light conveyor belt```
* ```heavy conveyor belt```
* ```large blower```
* ```generator```
* ```transmission axle```
* ```laundry machine```
* ```press```
* ```graphical machine```
* ```positive displacement pump```
* ```sieving machine```
* ```pottery machine```
* ```bucket elevator```
* ```reciprocating compressor```
* ```mill```
* ```carpentry machine```
* ```textile machine```
* ```crusher```
* ```crane```
* ```tire shop machine```

#### ```drive``` valid entries

* AC motors
    * ```normal torque ac```
    * ```ring cage ac```
    * ```synchronous ac```
    * ```phase division ac```
    * ```high torque ac```
    * ```high slipping ac```
    * ```repulsion induction ac```
    * ```monophasic ac```
    * ```collector rings ac```
* DC motors
    * ```derivation dc```
    * ```series winding dc```
    * ```mixed winding dc```
* Combustion engines
    * ```single cylinder combustion```
    * ```multiple cylinder combustion```
* ```transmission axle```
* ```clutch```


### profile

The v-belt profile can be determined for several different models, the main two beign Hi-Power II and Super HC. The submodule requires the power of the drive and rpm of the axle, used in the following format ```vbelts.profile.hi_power_2(power, rpm)```. An example for a drive with 8 hp and 540 rpm:

```python
>>> vbelts.profile.hi_power_2(8,540)
'B'
```

A string is returned with the choosed profile.

### Valid values for the power.corr_factor()

Valid values for the ```vbelt_model```:

* ```'hi_power'```
* ```'super_hc'```

Valid values for the ```vbelt_type```, all strings are in the tables below: the first is for Hi-Power-like types and the second for Super-HC-like types.

|A model|B model|C model|D model|
|-------|-------|-------|-------|
|A-26|B-35|C-51|D-120|
|A-27|B-37|C-55|D-128|
|A-31|B-38|C-60|D-144|
|A-32|B-39|C-68|D-158|
|A-33|B-42|C-71|D-162|
|A-35|B-46|C-75|D-173|
|A-37|B-48|C-81|D-180|
|A-38|B-52|C-85|D-195|
|A-41|B-55|C-90|D-210|
|A-42|B-60|C-96|D-225|
|A-45|B-64|C-100|D-240|
|A-46|B-68|C-105|D-270|
|A-49|B-71|C-112|D-300|
|A-53|B-75|C-120|D-330|
|A-57|B-78|C-128|D-360|
|A-60|B-85|C-136|D-390|
|A-64|B-90|C-144|D-420|
|A-68|B-97|C-158|D-480|
|A-71|B-105|C-162||
|A-75|B-112|C-173||
|A-80|B-120|C-180||
|A-85|B-128|C-195||
|A-90|B-136|C-210||
|A-96|B-144|C-225||
|A-105|B-158|C-240||
|A-112|B-162|C-255||
|A-120|B-173|C-270||
|A-128|B-180|C-300||
||B-195|C-330||
||B-210|C-360||
||B-225|C-390||
||B-240|C-420||
||B-270|||
||B-300|||

|3V model|5V model|8V model|
|--------|--------|--------|
|3V250|5V500|8V1000|
|3V265|5V530|8V1060|
|3V280|5V560|8V1120|
|3V300|5V600|8V1180|
|3V315|5V630|8V1250|
|3V335|5V670|8V1320|
|3V355|5V710|8V1400|
|3V375|5V750|8V1500|
|3V400|5V800|8V1600|
|3V425|5V850|8V1700|
|3V450|5V900|8V1800|
|3V475|5V950|8V1900|
|3V500|5V1000|8V2000|
|3V530|5V1060|8V2120|
|3V560|5V1120|8V2240|
|3V600|5V1180|8V2360|
|3V630|5V1250|8V2500|
|3V670|5V1320|8V2650|
|3V710|5V1400|8V2800|
|3V750|5V1500|8V3000|
|3V800|5V1600|8V3150|
|3V850|5V1700|8V3350|
|3V900|5V1800|8V3550|
|3V950|5V1900|8V3750|
|3V1000|5V2000|8V4000|
|3V1060|5V2120|8V4250|
|3V1120|5V2240|8V4500|
|3V1180|5V2360|8V4750|
|3V1250|5V2500|8V5000|
|3V1320|5V2650|8V5600|
|3V1400|5V2800||
||5V3000||
||5V3150||
||5V3350||
||5V3550||

## License information

vbelts is licensed in 3-clause BSD license. See ```LICENSE.txt``` for full information on the terms and conditions for usage of this software, and a disclaimer of all warranties.
