import copy
import json
from program_state.operations import SMT_OP, OP_TO_STR


class Expression(object):
    def __init__(self, op_type):
        self._op_type = op_type
        self._params = []

    def __str__(self):
        if self._op_type >= SMT_OP.NOT_IMP:
            return "INVALID_EXPRESSION"
        estr = ''
        estr += OP_TO_STR[self._op_type]
        estr += '('
        for param in self._params:
            estr += str(param)
            estr += ', '
        estr = estr[:-2]
        estr += ')'
        return estr

    @property
    def to_json(self):
        dict_value = {'op_type': self._op_type, 'params': []}
        for param in self._params:
            dict_value['params'].append(param.to_json)
        return json.dumps(dict_value)

    def copy(self):
        return copy.deepcopy(self)

    def is_logic_expr(self):
        return SMT_OP.GT <= self._op_type <= SMT_OP.NEQ

    def visit(self, func):
        for v in self._params:
            func(v)
            if isinstance(v, Expression):
                v.visit(func=func)


class AddExpression(Expression):
    def __init__(self, p1, p2):
        super().__init__(SMT_OP.ADD)
        self._params.append(p1)
        self._params.append(p2)


class SubExpression(Expression):
    def __init__(self, p1, p2):
        super().__init__(SMT_OP.SUB)
        self._params.append(p1)
        self._params.append(p2)


class MulExpression(Expression):
    def __init__(self, p1, p2):
        super().__init__(SMT_OP.MUL)
        self._params.append(p1)
        self._params.append(p2)


class DivExpression(Expression):
    def __init__(self, p1, p2):
        super().__init__(SMT_OP.DIV)
        self._params.append(p1)
        self._params.append(p2)


class OrExpression(Expression):
    def __init__(self, p1, p2):
        super().__init__(SMT_OP.OR)
        self._params.append(p1)
        self._params.append(p2)


class XorExpression(Expression):
    def __init__(self, p1, p2):
        super().__init__(SMT_OP.XOR)
        self._params.append(p1)
        self._params.append(p2)


class AndExpression(Expression):
    def __init__(self, p1, p2):
        super().__init__(SMT_OP.AND)
        self._params.append(p1)
        self._params.append(p2)


class NotExpression(Expression):
    def __init__(self, p1):
        super().__init__(SMT_OP.NOT)
        self._params.append(p1)


class GtExpression(Expression):
    def __init__(self, p1, p2):
        super().__init__(SMT_OP.GT)
        self._params.append(p1)
        self._params.append(p2)


class GeExpression(Expression):
    def __init__(self, p1, p2):
        super().__init__(SMT_OP.GE)
        self._params.append(p1)
        self._params.append(p2)


class LtExpression(Expression):
    def __init__(self, p1, p2):
        super().__init__(SMT_OP.LT)
        self._params.append(p1)
        self._params.append(p2)


class LeExpression(Expression):
    def __init__(self, p1, p2):
        super().__init__(SMT_OP.LE)
        self._params.append(p1)
        self._params.append(p2)


class EqExpression(Expression):
    def __init__(self, p1, p2):
        super().__init__(SMT_OP.EQ)
        self._params.append(p1)
        self._params.append(p2)


class NeqExpression(Expression):
    def __init__(self, p1, p2):
        super().__init__(SMT_OP.NEQ)
        self._params.append(p1)
        self._params.append(p2)


class LsExpression(Expression):
    def __init__(self, p1, p2):
        super().__init__(SMT_OP.LS)
        self._params.append(p1)
        self._params.append(p2)


class RsExpression(Expression):
    def __init__(self, p1, p2):
        super().__init__(SMT_OP.RS)
        self._params.append(p1)
        self._params.append(p2)


class ConstExpression(Expression):
    def __init__(self, p1):
        super().__init__(SMT_OP.CONST)
        self._params.append(p1)

    def __str__(self):
        return "Constant(" + str(self._params[0]) + ")"

    @property
    def to_json(self):
        dict_value = {'op_type': SMT_OP.CONST, 'params': [{'value': self._params[0]}]}
        return json.dumps(dict_value)


class VCMExpression(Expression):
    def __init__(self, addr_expr, is_unsigned):
        super().__init__(SMT_OP.VCM)
        self._params.append(addr_expr)
        self._params.append(is_unsigned)

    def __str__(self):
        estr = 'VCM'
        estr += '( '
        estr += str(self._params[0])  # addr_expr
        estr += ', '
        if self._params[1]:  # is_unsigned
            estr += 'unsigned char'
        else:
            estr += 'signed char'
        estr += ')'
        return estr

    @property
    def to_json(self):
        dict_value = {'op_type': SMT_OP.VCM, 'params': [{'addr': self._params[0].to_json, 'is_unsigned':
            self._params[1]}]}
        return json.dumps(dict_value)


class VIMExpression(Expression):
    def __init__(self, addr_expr, is_unsigned, bit_width):
        super().__init__(SMT_OP.VIM)
        self._params.append(addr_expr)
        self._params.append(is_unsigned)
        self._params.append(bit_width)

    def __str__(self):
        estr = 'VIM'
        estr += '('
        estr += str(self._params[0])  # addr_expr
        estr += ', '
        if self._params[1]:  # is_unsigned
            estr += 'unsigned int'
        else:
            estr += 'signed int'
        estr += str(self._params[2])  # bit_width
        estr += ')'
        return estr

    @property
    def to_json(self):
        dict_value = {'op_type': SMT_OP.VIM, 'params': [{'addr': self._params[0].to_json, 'is_unsigned':
            self._params[1], 'bit_width': self._params[2]}]}
        return json.dumps(dict_value)


class VFMExpression(Expression):
    def __init__(self, addr_expr):
        super().__init__(SMT_OP.VFM)
        self._params.append(addr_expr)


class VDMExpression(Expression):
    def __init__(self, addr_expr):
        super().__init__(SMT_OP.VDM)
        self._params.append(addr_expr)


class VCRExpression(Expression):
    def __init__(self, reg_name, is_unsigned):
        super().__init__(SMT_OP.VCR)
        self._params.append(reg_name)
        self._params.append(is_unsigned)

    def __str__(self):
        estr = 'VCR'
        estr += '('
        estr += self._params[0]  # reg_name
        estr += ', '
        if self._params[1]:  # is_unsigned
            estr += 'unsigned char'
        else:
            estr += 'signed char'
        estr += ')'
        return estr

    @property
    def to_json(self):
        dict_value = {'op_type': SMT_OP.VCR, 'params': [{'reg_name': self._params[0], 'is_unsigned':
            self._params[1]}]}
        return json.dumps(dict_value)


class VIRExpression(Expression):
    def __init__(self, reg_name, is_unsigned, bit_width):
        super().__init__(SMT_OP.VCR)
        self._params.append(reg_name)
        self._params.append(is_unsigned)
        self._params.append(bit_width)

    def __str__(self):
        estr = 'VIR'
        estr += '('
        estr += self._params[0]  # reg_name
        estr += ', '
        if self._params[1]:  # is_unsigned
            estr += 'unsigned int'
        else:
            estr += 'signed int'
        estr += str(self._params[2])  # bit_width
        estr += ')'
        return estr

    @property
    def to_json(self):
        dict_value = {'op_type': SMT_OP.VIR, 'params': [{'reg_name': self._params[0], 'is_unsigned':
            self._params[1], 'bit_width': self._params[2]}]}
        return json.dumps(dict_value)


class VFRExpression(Expression):
    def __init__(self, reg_name):
        super().__init__(SMT_OP.VFR)
        self._params.append(reg_name)


class VDRExpression(Expression):
    def __init__(self, reg_name):
        super().__init__(SMT_OP.VDR)
        self._params.append(reg_name)


class OFBExpression(Expression):
    def __init__(self, lib_name, offset_expr):
        super().__init__(SMT_OP.OFB)
        self._params.append(lib_name)
        self._params.append(offset_expr)

    def __str__(self):
        estr = 'OFB'
        estr += '('
        estr += self._params[0]  # lib_name
        estr += ', '
        estr += str(self._params[1])  # offset_expr
        estr += ')'
        return estr

    @property
    def to_json(self):
        dict_value = {'op_type': SMT_OP.OFB, 'params': [{'lib_name': self._params[0], 'offset': self._params[
            1].to_json}]}
        return json.dumps(dict_value)


class REGCTLExpression(Expression):
    def __init__(self, reg_name):
        super().__init__(SMT_OP.REG_CTL)
        self._params.append(reg_name)

    def __str__(self):
        estr = 'CTL('
        estr += self._params[0]
        estr += ')'
        return estr

    @property
    def to_json(self):
        dict_value = {'op_type': SMT_OP.REG_CTL, 'params': [{'data': self._params[0]}]}
        return json.dumps(dict_value)


class MEMCTLExpression(Expression):
    def __init__(self, mem_expr, size_in_byte):
        super().__init__(SMT_OP.MEM_CTL)
        self._params.append(mem_expr)
        self._params.append(size_in_byte)

    def __str__(self):
        estr = 'CTL('
        estr += str(self._params[0])
        estr += ', '
        estr += 'size = '
        estr += str(self._params[1])
        estr += ')'
        return estr

    @property
    def to_json(self):
        dict_value = {'op_type': SMT_OP.MEM_CTL, 'params': [{'data': self._params[0], 'size': self._params[1]}]}
        return json.dumps(dict_value)


def construct_expression_from_json(json_str):
    try:
        dict_value = json.loads(json_str)
    except:
        return None
    op_type = dict_value['op_type']
    if op_type == SMT_OP.ADD:
        params_dict = dict_value['params']
        p1_dict = params_dict[0]
        p2_dict = params_dict[1]
        p1 = construct_expression_from_json(p1_dict)
        p2 = construct_expression_from_json(p2_dict)
        return AddExpression(p1, p2)
    elif op_type == SMT_OP.SUB:
        params_dict = dict_value['params']
        p1_dict = params_dict[0]
        p2_dict = params_dict[1]
        p1 = construct_expression_from_json(p1_dict)
        p2 = construct_expression_from_json(p2_dict)
        return SubExpression(p1, p2)
    elif op_type == SMT_OP.MUL:
        params_dict = dict_value['params']
        p1_dict = params_dict[0]
        p2_dict = params_dict[1]
        p1 = construct_expression_from_json(p1_dict)
        p2 = construct_expression_from_json(p2_dict)
        return MulExpression(p1, p2)
    elif op_type == SMT_OP.DIV:
        params_dict = dict_value['params']
        p1_dict = params_dict[0]
        p2_dict = params_dict[1]
        p1 = construct_expression_from_json(p1_dict)
        p2 = construct_expression_from_json(p2_dict)
        return DivExpression(p1, p2)
    elif op_type == SMT_OP.OR:
        params_dict = dict_value['params']
        p1_dict = params_dict[0]
        p2_dict = params_dict[1]
        p1 = construct_expression_from_json(p1_dict)
        p2 = construct_expression_from_json(p2_dict)
        return OrExpression(p1, p2)
    elif op_type == SMT_OP.XOR:
        params_dict = dict_value['params']
        p1_dict = params_dict[0]
        p2_dict = params_dict[1]
        p1 = construct_expression_from_json(p1_dict)
        p2 = construct_expression_from_json(p2_dict)
        return XorExpression(p1, p2)
    elif op_type == SMT_OP.AND:
        params_dict = dict_value['params']
        p1_dict = params_dict[0]
        p2_dict = params_dict[1]
        p1 = construct_expression_from_json(p1_dict)
        p2 = construct_expression_from_json(p2_dict)
        return AndExpression(p1, p2)
    elif op_type == SMT_OP.NOT:
        params_dict = dict_value['params']
        p1_dict = params_dict[0]
        p1 = construct_expression_from_json(p1_dict)
        return NotExpression(p1)
    elif op_type == SMT_OP.GT:
        params_dict = dict_value['params']
        p1_dict = params_dict[0]
        p2_dict = params_dict[1]
        p1 = construct_expression_from_json(p1_dict)
        p2 = construct_expression_from_json(p2_dict)
        return GtExpression(p1, p2)
    elif op_type == SMT_OP.GE:
        params_dict = dict_value['params']
        p1_dict = params_dict[0]
        p2_dict = params_dict[1]
        p1 = construct_expression_from_json(p1_dict)
        p2 = construct_expression_from_json(p2_dict)
        return GeExpression(p1, p2)
    elif op_type == SMT_OP.LT:
        params_dict = dict_value['params']
        p1_dict = params_dict[0]
        p2_dict = params_dict[1]
        p1 = construct_expression_from_json(p1_dict)
        p2 = construct_expression_from_json(p2_dict)
        return LtExpression(p1, p2)
    elif op_type == SMT_OP.LE:
        params_dict = dict_value['params']
        p1_dict = params_dict[0]
        p2_dict = params_dict[1]
        p1 = construct_expression_from_json(p1_dict)
        p2 = construct_expression_from_json(p2_dict)
        return LeExpression(p1, p2)
    elif op_type == SMT_OP.EQ:
        params_dict = dict_value['params']
        p1_dict = params_dict[0]
        p2_dict = params_dict[1]
        p1 = construct_expression_from_json(p1_dict)
        p2 = construct_expression_from_json(p2_dict)
        return EqExpression(p1, p2)
    elif op_type == SMT_OP.NEQ:
        params_dict = dict_value['params']
        p1_dict = params_dict[0]
        p2_dict = params_dict[1]
        p1 = construct_expression_from_json(p1_dict)
        p2 = construct_expression_from_json(p2_dict)
        return NeqExpression(p1, p2)
    elif op_type == SMT_OP.LS:
        params_dict = dict_value['params']
        p1_dict = params_dict[0]
        p2_dict = params_dict[1]
        p1 = construct_expression_from_json(p1_dict)
        p2 = construct_expression_from_json(p2_dict)
        return LsExpression(p1, p2)
    elif op_type == SMT_OP.RS:
        params_dict = dict_value['params']
        p1_dict = params_dict[0]
        p2_dict = params_dict[1]
        p1 = construct_expression_from_json(p1_dict)
        p2 = construct_expression_from_json(p2_dict)
        return RsExpression(p1, p2)
    elif op_type == SMT_OP.CONST:
        params_dict = dict_value['params'][0]
        value = params_dict['value']
        return ConstExpression(value)
    elif op_type == SMT_OP.VCM:
        params_dict = dict_value['params'][0]
        addr = params_dict['addr']
        is_unsigned = params_dict['is_unsigned']
        return VCMExpression(addr, is_unsigned)
    elif op_type == SMT_OP.VIM:
        params_dict = dict_value['params'][0]
        addr = params_dict['addr']
        is_unsigned = params_dict['is_unsigned']
        bit_width = params_dict['bit_width']
        return VIMExpression(addr, is_unsigned, bit_width)
    elif op_type == SMT_OP.VFM:
        params_dict = dict_value['params'][0]
        addr = params_dict['addr']
        return VFMExpression(addr)
    elif op_type == SMT_OP.VDM:
        params_dict = dict_value['params'][0]
        addr = params_dict['addr']
        return VDMExpression(addr)
    elif op_type == SMT_OP.VCR:
        params_dict = dict_value['params'][0]
        reg_name = params_dict['reg_name']
        is_unsigned = params_dict['is_unsigned']
        return VCRExpression(reg_name, is_unsigned)
    elif op_type == SMT_OP.VIR:
        params_dict = dict_value['params'][0]
        reg_name = params_dict['reg_name']
        is_unsigned = params_dict['is_unsigned']
        bit_width = params_dict['bit_width']
        return VIRExpression(reg_name, is_unsigned, bit_width)
    elif op_type == SMT_OP.VFM:
        params_dict = dict_value['params'][0]
        reg_name = params_dict['reg_name']
        return VFRExpression(reg_name)
    elif op_type == SMT_OP.VDM:
        params_dict = dict_value['params'][0]
        reg_name = params_dict['reg_name']
        return VDRExpression(reg_name)
    else:
        return None

