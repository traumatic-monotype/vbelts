.. vbelts documentation master file, created by
   sphinx-quickstart on Sun Sep 13 18:42:50 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to vbelts' documentation!
==================================

Vbelts projects aims to deliver a tool for v-belt calculation and dimensioning, an open-source software for engineers and technicians working in mechanical engineering. It includes modules for the most common needs when calculating v-belts.

Features
--------

- Profile selection
- Power estimation
- Commercial pulley diameter calculation and selection
- Easily define correct center distance between pulleys
- Choose the appropriate model and quantity of v-belts

Guide
-----

[TODO]

If you are a complete beginner trying to calculate a v-belt for your system, the guide will help you with examples and explanations.

Documentation
-------------

The docs are a reference for the functions in the package. The documentation contain information that help you understand and use vbelts as easily and pain-free as possible. It is *always* recommended to read the documentation before you use vbelts.

.. warning:: Please note that the software is provided "as is", without any warranties. The copyright owners and contributors are, in no event, liable for any damages caused by the use or misuse of the package. For more information see the licensing information.

Getting started
---------------

You can install vbelts from a Python installation with pip by:

.. code-block:: bash

   $ pip install vbelts

To get the git version, run:

.. code-block:: bash

   $ git clone https://github.com/traumatic-monotype/vbelts.git

Latest source code
------------------

You can get the latest development source code at

https://github.com/traumatic-monotype/vbelts


License information
===================

vbelts is BSD licensed. See ``LICENSE.txt`` for full information on the terms & conditions for usage of this software, and a DISCLAIMER OF ALL WARRANTIES.


.. toctree::
   :maxdepth: 3
   :caption: Tutorial:

.. toctree::
   :maxdepth: 3
   :caption: Documentation:

   modules

.. toctree::
   :maxdepth: 2
   :caption: Data:

   data/vbelt_model_profile
   data/vbelt_types
   data/vbelt_length
   data/vbelt_h_factor
   data/motor_machine_data


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
