# -*- coding: utf-8 -*-
# 作者: vancaho
# 日期: 2022.08
# 功能：共用的一些函数

def strip_outmost_brackets(input):
    input_len = len(input)
    if len(input) == 0:
        return False, input

    if input[0]!= '(' or input[-1] != ')':
        return False, input

    bracket_depth = 0
    bracket_closed = False

    bracket_match = False
    for offset in range(0, input_len):
        if input[offset] == '(':
            bracket_depth = bracket_depth + 1
        elif input[offset] == ')':
            if offset == input_len - 1:
                if bracket_depth == 1 and bracket_closed == False:
                    bracket_match = True

            bracket_depth = bracket_depth - 1
            if bracket_depth == 0:
                bracket_closed = True

    if bracket_match == True:
        return True, input[1:-1]
    return False, input

def strip_all_outmost_brackets(input):
    stripped = True
    res = input
    while stripped == True:
        stripped, res = strip_outmost_brackets(res)

    return res

def strip_input(input):
    return strip_all_outmost_brackets(strip_comment_and_space(input))

def strip_comment_and_space(input):
    # remove the # or % comment sign
    comment_end = input.find('#')
    if comment_end == -1:
        comment_end = input.find('%')

    if comment_end != -1:
        output = input[0:comment_end]

    # remove the spaces or '-' sign
    output = input.strip().lstrip('-').strip().rstrip('.')
    return output
