# -*- coding: utf-8 -*-
import json
from utils.io import *
from program_state.expressions import *


class Constraint:
    def __init__(self, comments=""):
        self.expressions = []
        self.__comments = comments

    def __str__(self):
        cstr = '\tComments: ' + self.__comments
        cstr += "\n"
        cstr += "\tExpressions: "
        for expr in self.expressions:
            cstr += str(expr)
            cstr += ' && \n'
        return cstr[:-5]

    def add_expression(self, expr):
        if not expr.is_logic_expr():
            WARN("Ignore adding a none logical expression: %s" % str(expr))
            return
        self.expressions.append(expr)

    @property
    def comments(self):
        return self.__comments

    @property
    def to_json(self):
        info = []
        for expr in self.expressions:
            info.append(expr.to_json)

        return json.dumps(info)

    def from_json(self, json_str):
        try:
            json_data = json.loads(json_str)
        except:
            WARN("Error when loading json when constructing constraint from json!")
            return

        for each_expr_info in json_data:
            expr = construct_expression_from_json(each_expr_info)
            if expr is not None:
                self.expressions.append(expr)
        return
