# -*- coding: utf-8 -*-


class SMT_OP:
    """
    定义了所有的SMT操作。
    """
    # 算术操作
    ADD = 1  # 加
    SUB = 2  # 减
    MUL = 3  # 乘
    DIV = 4  # 除

    # 逻辑运算
    OR = 5  # 或
    XOR = 6  # 异或
    AND = 7  # 与
    NOT = 8  # 非

    # 比较运算
    GT = 9  # 大于
    GE = 10  # 大于等于
    LT = 11  # 小于
    LE = 12  # 小于等于
    EQ = 13  # 相等
    NEQ = 14  # 不相等

    # 位运算
    LS = 15  # 左移
    RS = 16  # 右移

    CONST = 17  # 常量

    VCM = 18  # 从内存获取char
    VIM = 19  # 从内存获取整数
    VFM = 20  # 从内存获取浮点数
    VDM = 21  # 从内存获取双精度数

    VCR = 22  # 从寄存器获取char
    VIR = 23  # 从寄存器获取整数
    VFR = 24  # 从寄存器获取浮点数
    VDR = 25  # 从寄存器获取双精度数

    OFB = 26  # 从指定模块的偏移量

    REG_CTL = 27  # 寄存器数据为可控
    MEM_CTL = 28  # 内存数据为可控

    NOT_IMP = 29


# 映射字典，便于转字符串
OP_TO_STR = {1: 'ADD', 2: 'SUB', 3: 'MUL', 4: 'DIV',
             5: 'OR', 6: 'XOR', 7: 'AND', 8: 'NOT',
             9: 'GT', 10: 'GE', 11: 'LT', 12: 'LE', 13: 'EQ', 14: 'NEQ',
             15: 'LS', 16: 'RS', 17: 'CONST',
             18: 'VCM', 19: 'VIM', 20: 'VFM', 21: 'VDM',
             22: 'VCR', 23: 'VIR', 24: 'VFR', 25: 'VDR',
             26: 'OFB', 27: 'REG_CTL', 28: 'MEM_CTL'}
