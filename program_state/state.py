# -*- coding: utf-8 -*-

from copy import deepcopy
from program_state.constraint import Constraint


class State:
    """
    Basic definition of program state.
    """
    def __init__(self, name=""):
        """
        :param ip: RIP register value.
        :param name(optional): Name of current state.
        """
        self.__name = name
        self.__constraints = []

    @property
    def constraints(self):
        return self.__constraints

    @property
    def name(self):
        if self.__name == "":
            return "anonymous"
        return self.__name

    def add_constraint(self, C):
        """
        Add a constraint to current state
        :param c: new constraint
        :return: nothing
        """
        _c = deepcopy(C)  # do not use C directly!
        self.__constraints.append(_c)

    def __str__(self):
        msg = "Name: %s\n" % self.name
        msg += "Constraints: \n"
        for C in self.__constraints:
            msg += "%s" % str(C)
            msg += '\n'
        return msg


class StateChain:
    def __init__(self):
        self.__state_list = []

    @property
    def num_states(self):
        return len(self.__state_list)

    def get_state_by_index(self, index):
        if index >= self.num_states:
            return None

        return self.__state_list[index]

    def get_state_by_name(self, name):
        for state in self.__state_list:
            if state.name == name:
                return state
        return None

    def append_state(self, S):
        self.__state_list.append(S)

    def merge_state(self, S):
        if self.num_states == 0:
            self.__state_list.append(S)
            return
        for C in S.constraints:
            self.__state_list[-1].add_constraint(C)
        return
