"""
antecedent_consequent.py : Contains Antecedent and Consequent classes.
"""
import numpy as np

from skfuzzy.control.state import StatefulProperty
from ..fuzzymath import interp_membership
from .fuzzyvariable import FuzzyVariable
from ..defuzzify import defuzz

try:
    from collections import OrderedDict
except ImportError:
    from .ordereddict import OrderedDict


class Antecedent(FuzzyVariable):
    """
    Antecedent (input/sensor) variable for a fuzzy control system.

    Parameters
    ----------
    universe : array-like
        Universe variable. Must be 1-dimensional and convertible to a NumPy
        array.
    label : string
        Name of the universe variable.
    """
    # Customized subclass of `FuzzyVariable`
    def __init__(self, universe, label):
        """""" + Antecedent.__doc__
        super(Antecedent, self).__init__(universe, label)
        self.__name__ = 'Antecedent'
        self.input = StatefulProperty(None)


class Consequent(FuzzyVariable):
    """
    Consequent (output/control) variable for a fuzzy control system.

    Parameters
    ----------
    universe : array-like
        Universe variable. Must be 1-dimensional and convertible to a NumPy
        array.
    label : string
        Name of the universe variable.

    Notes
    -----
    The ``label`` string chosen must be unique among Antecedents and
    Consequents in the ``ControlSystem``.
    """
    # Customized subclass of `FuzzyVariable`
    def __init__(self, universe, label):
        """""" + Consequent.__doc__
        super(Consequent, self).__init__(universe, label)
        self.__name__ = 'Consequent'
        self.output = StatefulProperty(None)

        # Default accumulation method is to take the max of any cut
        self.accumulation_method = np.max



class Intermediary(FuzzyVariable):
    def __init__(self, universe, label):
        super(Intermediary, self).__init__(universe, label)
        self.__name__ = "Intermediary"

        # Default accumulation method to max
        self.accumulation_method = np.max

