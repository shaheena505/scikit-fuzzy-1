"""
rule.py : Contains `Rule` object which is used to connected
atecedents with conqeuents in a `ControlSystem`.
"""

import numpy as np
import networkx as nx
from weakref import WeakKeyDictionary
from .antecedent_consequent import Antecedent, Consequent, Intermediary
from .fuzzyvariable import (FuzzyVariable, FuzzyVariableTerm,
                            FuzzyAggregationMethod,
                            FuzzyVariableTermAggregate)
from .visualization import ControlSystemVisualizer
from .state import StatefulProperty

try:
    from collections import OrderedDict
except ImportError:
    from .ordereddict import OrderedDict


class WeightedConsequent(object):
    def __init__(self, term, weight):
        assert isinstance(term, FuzzyVariableTerm)
        self.term = term
        self.weight = weight
        self.activation = StatefulProperty(None)

    def __repr__(self):
        if self.weight == 1.:
            return self.term.full_label
        else:
            return "%s@%02.f" % (self.term.full_label, self.weight)


class Rule(object):

    def __init__(self, antecedent=None, consequent=None, label=None):
        self.label = label
        self.aggregation_method = FuzzyAggregationMethod()

        self.aggregate_firing = StatefulProperty(None)

        self._antecedent = None
        self._consequent = None
        if antecedent is not None:
            self.antecedent = antecedent
        if consequent is not None:
            self.consequent = consequent


    def __repr__(self):
        """
        Print a concise, readable summary of the fuzzy rule.
        """
        if self.label is not None:
            return self.label
        if len(self.consequent) == 1:
            cons = self.consequent[0]
        else:
            cons = self.consequent
        return "IF %s THEN %s" % (self.antecedent, cons)

    @property
    def antecedent(self):
        if self._antecedent is None:
            raise ValueError("Antecedent not set")
        return self._antecedent
    @antecedent.setter
    def antecedent(self, value):
        if hasattr(value, 'membership_value'):
            # Should be either FuzzyVariableTerm or FuzzyVariableTermAggregate
            self._antecedent = value
        else:
            raise ValueError("Unexpected antecedent type")

    @property
    def antecedent_terms(self):
        # Grab all the terms that make up my antecedent clause
        terms = []
        def _find_terms(obj):
            if isinstance(obj, FuzzyVariableTerm):
                terms.append(obj)
            else:
                assert isinstance(obj, FuzzyVariableTermAggregate)
                _find_terms(obj.term1)
                _find_terms(obj.term2)
        _find_terms(self.antecedent)
        return terms

    @property
    def consequent(self):
        if self._consequent is None:
            raise ValueError("Consquent not set")
        return self._consequent
    @consequent.setter
    def consequent(self, value):
        """
        Accepts consequents in four formats:
         a) Unweighted single output.
            eg: output['term']
         b) Weighted single output
            eg: (output['term'], 0.5)
         c) Unweighted multiple output
            eg: (output1['term1'], output2['term2'])
         d) Weighted multiple output
            eg: ( (output1['term1'],1.0), (output2['term2'],0.5) )
        """
        if isinstance(value, FuzzyVariableTerm):
            self._consequent = [WeightedConsequent(value, 1.)]

        elif not hasattr(value, '__iter__'):
            raise ValueError("Unexpected consequent type")

        else:

            # Must be one of formats b) to d)
            self._consequent = []
            for i in value:
                if isinstance(i, FuzzyVariableTerm):
                    self._consequent.append(WeightedConsequent(i, 1.))
                else:
                    try:
                        assert len(i) == 2
                    except:
                        # Could die to assertion or because i is not iterable
                        raise ValueError("Unexpected consequent type")
                    self._consequent.append((WeightedConsequent(i[0], i[1])))

    @property
    def graph(self):
        graph = nx.DiGraph()
        # Link all antecedents to me by decomposing
        #  FuzzyVariableTermAggregate down to just FuzzyVariableTerms
        for t in self.antecedent_terms:
            assert isinstance(t, FuzzyVariableTerm)
            graph.add_path([t, self])
            graph.add_path([t.parent_variable, t])

        # Link all consequents from me
        for c in self.consequent:
            graph.add_path([self, c.term])
            graph.add_path([c.term, c.term.parent_variable])
        return graph


    def view(self):
        ControlSystemVisualizer(self).view().show()