from program_state.expressions import *


def get_char_from_memory(addr, is_unsigned):
    return VCMExpression(addr_expr=addr, is_unsigned=is_unsigned)


def get_int_from_memory(addr, is_unsigned, bit_width):
    return VIMExpression(addr_expr=addr, is_unsigned=is_unsigned, bit_width=bit_width)


def get_float_from_memory(addr):
    return VFMExpression(addr_expr=addr)


def get_double_from_memory(addr):
    return VDMExpression(addr_expr=addr)


def get_char_from_register(reg_name, is_unsigned):
    return VCRExpression(reg_name=reg_name, is_unsigned=is_unsigned)


def get_int_from_register(reg_name, is_unsigned, bit_width):
    return VIRExpression(reg_name=reg_name, is_unsigned=is_unsigned, bit_width=bit_width)


def get_float_from_register(reg_name):
    return VFRExpression(reg_name=reg_name)


def get_double_from_register(reg_name):
    return VDRExpression(reg_name=reg_name)
