"""
=====================
emc2.core (emc2.core)
=====================

.. currentmodule:: emc2.core

The procedures in this module contain the core data structures of EMC^2.
In particular, the Instrument class that describes the characteristics
of the instrument to be simulated is stored here. In addition, global
constants used by EMC^2 are also stored in this module.

.. autosummary::
    :toctree: generated/

    Instrument
    hydrometeor_info
    instruments.KAZR
    instruments.HSRL
    instruments.Ten64nm
"""

from . import instruments
from .instrument import Instrument
from . import hydrometeor_info