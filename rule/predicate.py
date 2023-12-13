# -*- coding: utf-8 -*-
# 作者: vancaho
# 日期: 2022.08
# 功能：表示谓词的一个类

from rule.argument_parser import ArgumentParser
from rule.common import strip_input
from rule.json_converter import JsonConverter
import json
class Predicate:
    def __init__(self, predicate_str):
        try:
            predicate_json = json.loads(predicate_str)
            self._predicate_str, self._func, self._arguments = self._init_from_json(predicate_json)
        except:
            self._predicate_str, self._func, self._arguments = self._init_from_str(predicate_str)
        return

    def is_valid(self):
        if self._func == '':
            return False
        return True

    def _init_from_json(self, predicate_json):
        if 'query_name' in predicate_json:
            predicate = predicate_json['query_name']
        else:
            predicate = ''

        if 'args' in predicate_json:
            arg_list = self._process_args_from_json(predicate_json['args'])
        else:
            arg_list = []

        argument_parser = ArgumentParser(arg_list)
        args = argument_parser.get_arguments()

        return '', predicate, args

    def _init_from_str(self, predicate_str):

        predicate_str = strip_input(predicate_str)

        func_end_pos = predicate_str.find("(")
        arguments_end = predicate_str.rfind(")")

        if func_end_pos != -1 and arguments_end == -1:
            return '', '', []
        if func_end_pos == -1 and arguments_end != -1:
            return '', '', []

        # 如果()符号的位置不对
        if func_end_pos != -1 and arguments_end != -1 and arguments_end < func_end_pos:
            return '', '', []


        if func_end_pos != -1:
            predicate = predicate_str[0:func_end_pos].strip()
            arguments_str = predicate_str[func_end_pos + 1:arguments_end]

        else:
            predicate = predicate_str[0:].strip()
            arguments_str = ''

        argument_parser = ArgumentParser(arguments_str)
        args = argument_parser.get_arguments()
        ret_args = []
        json_converter = JsonConverter()
        for arg in args:

            ret_args.append(self._process_arg(json_converter.convert_item(arg)))

        return predicate_str, predicate, ret_args


    def _process_arg(self, arg):
        if isinstance(arg, int):
            return {'type': 'int', 'value': arg, 'concrete':True}
        elif isinstance(arg, str):
            concrete = True
            if arg.startswith('_'):
                concrete = False
            # if len(arg)>0 and arg[0].isupper():
            #     concrete = False
            return {'type': 'str', 'value': arg, 'concrete':concrete}

        elif isinstance(arg, list):
            return {'type': 'json', 'value': arg, 'concrete':True}
        elif isinstance(arg, dict):
            return {'type': 'json', 'value': arg, 'concrete':True}

    @property
    def func(self):
        return self._func

    def get_arguments(self):
        return self._arguments


    def get_arguments_str(self):
        res_list = []
        for arg in self._arguments:

            if arg['type']=='str':
                if arg['concrete'] == True:
                    res_list.append('"'+arg['value']+'"')
                else:
                    res_list.append(arg['value'])
            else:
                res_list.append(arg['value'])

        return ', '.join([str(x) for x in res_list])

    def __str__(self):
        if len(self._arguments) == 0:
            return "{}()".format(self._func)
        return '{}({})'.format(self._func, self.get_arguments_str())


    def get_input_str(self):
        args = []
        for arg in self._arguments:
            if arg['concrete'] == True:
                args.append(arg['value'])
            else:
                args.append("_")
        return '{}({})'.format(self._func, ','.join(str(args)))


    def _process_args_from_json(self, args):
        ret = []
        for arg in args:
            if arg['type'] == 'var':
                arg['concrete'] = False
            else:
                arg['concrete'] = True
            # if arg['type'] == 'int' or arg['type'] == 'json':
            #     arg['concrete'] = True
            #
            # else:
            #     if arg['value'].startswith("_") or (len(arg) >0 and arg['value'][0].isupper()):
            #         arg['concrete'] = False
            #     else:
            #         arg['concrete'] = True
            ret.append(arg)
        return ret
    def _is_concrete_arg(self, arg):
        if isinstance(arg, int) or isinstance(arg, list) or isinstance(arg, dict):
            return True

        if len(arg) == 0:
            return True

        if isinstance(arg, str) and arg.startswith('_'):
            return False

        # if arg[0].isupper():
        #     return False

        return True

    def are_all_arguments_concrete(self):
        for argument in self.get_arguments():
            if 'concrete' in argument and argument['concrete'] == False:
                return False

        return True


def main():
    # s = "aaab(B0 is Number /\ 255, B1 is (Number >> 8) /\ 255, B2 is (Number >> 16) /\ 255, B3 is (Number >> 24) /\ 255, Bytes = [B0, B1, B2, B3])"
    p = Predicate("predicate(1,2,4,[1,3,4,5],a(b),json([1,2,3,4,[321,123,0x44]]), [31,41,json([a=1,b=2]),[1,23,4]])")
   # p = Predicate("predicate(json([a=1,b=2,c=3]))")

    print(p)
    # p._convert_prolog_json_to_dict("json([c=[1,2,3,4,5]])")
    return

if __name__ == "__main__":
    main()