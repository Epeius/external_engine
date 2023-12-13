# -*- coding: utf-8 -*-
# 作者: vancaho
# 日期: 2022.08
# 功能：解析prolog格式的参数字符串

from rule.common import strip_input
import json

class ArgumentParser:
    def __init__(self, args_info):
        if isinstance(args_info, list):
            self._args = []
            for arg in args_info:
                try:
                    arg_item = {}
                    arg_item['type'] = arg['type']
                    arg_item['concrete'] = arg['concrete']
                    if arg_item['type'] == 'json':
                        if isinstance(arg['value'], str):
                            arg_item['value'] = json.loads(arg['value'])
                        else:
                            arg_item['value'] = arg['value']
                    else:
                        arg_item['value'] = arg['value']
                    self._args.append(arg_item)
                except:
                    pass
            # self._args = args_info
        else:
            self._args = self._extract_args_from_str(args_info)

        self._arg_str =  ', '.join(str(self._args))

        return

    def get_arguments(self):
        return self._args

    def _extract_args_from_list(self, args_info):
        args = []
        for arg_info in args_info:
            if arg_info['type'] == 'json':
                try:
                    args.append(json.loads(arg_info['value']))
                except:
                    pass
            else:
                args.append(arg_info['value'])
        return args

    def _extract_args_from_str(self, arg_str):
        '''
        从字符串中提取参数信息，如果参数的括号不匹配，将错误
        :param arg_str:
        :return:
        '''
        arg_str = strip_input(arg_str)
        arg_str_len = len(arg_str)
        bracket_depth = 0
        square_bracket_depth = 0
        last_offest = 0
        args = []
        for offset in range(0, arg_str_len):
            if arg_str[offset] == '(':
                bracket_depth = bracket_depth + 1
            elif arg_str[offset] == ')':
                bracket_depth = bracket_depth - 1

            elif arg_str[offset] == '[':
                square_bracket_depth =square_bracket_depth + 1
            elif arg_str[offset] == ']':
                square_bracket_depth=square_bracket_depth - 1

            if (arg_str[offset] == ',' or offset == arg_str_len-1) and bracket_depth == 0 and square_bracket_depth== 0:
                if offset == arg_str_len - 1:
                    args.append(arg_str[last_offest:].strip(',').strip())
                else:
                    args.append(arg_str[last_offest:offset].strip())
                last_offest = offset+1

        if bracket_depth!=0 or square_bracket_depth != 0:
            print("[*] [ArgumentParser] The bracket or square_bracket mismatch for {}".format(arg_str))
            return []
        return args


def main():

    return

if __name__ == "__main__":
    main()
