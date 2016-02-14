
from weakref import WeakKeyDictionary




class StatefulProperty(object):

    def __init__(self, initial_condition = None):
        self.default = initial_condition
        self.__sim_data = WeakKeyDictionary()

    def __getitem__(self, key):
        from .controlsystem import ControlSystemSimulation
        assert isinstance(key, ControlSystemSimulation)
        try:
            return self.__sim_data[key]
        except KeyError:
            if isinstance(self.default, dict) and len(self.default) == 0:
                # Create a new empty dictionary and remember it
                result = dict()
                self.__sim_data[key] = result
                return result
            else:
                return self.default


    def __setitem__(self, key, value):
        from .controlsystem import ControlSystemSimulation
        assert isinstance(key, ControlSystemSimulation)
        self.__sim_data[key] = value

    def __del__(self):
        # For debugging
        raise RuntimeError("Tried to delete a stateful property!")

