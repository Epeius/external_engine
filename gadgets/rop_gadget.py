# -*- coding: utf-8 -*-
from pwn import p64
import json


class ROPGadget:
    """
    Basic definition of a ROP gadget.
    """

    def __init__(self, address, last_inst_addr, inst_list, size, stack_size, parameters=None, read_regs=None,
                 write_regs=None):
        """
        Initialize a ROP gadget.
        :param address: 表示Gadget起始地址
        :param last_inst_addr: 表示该Gadget中最后一条指令的地址
        :param inst_list: 表示Gadget中指令列表
        :param size: 表示Gadget代码的字节长度
        :param stack_size: 表示Gadget占用栈空间长度
        :param parameters: 用于为不同Gadget传递参数
        :param read_regs: 该Gadget读取的寄存器列表
        :param write_regs: 该Gadget写入的寄存器列表
        """
        if parameters is None:
            parameters = []
        if read_regs is None:
            read_regs = []
        if write_regs is None:
            write_regs = []
        self.__address = address
        self.__last_inst_addr = last_inst_addr
        self.__inst_list = inst_list
        self.__size = size
        self.__stack_size = stack_size
        self.__parameters = parameters
        self.__read_regs = read_regs
        self.__write_regs = write_regs

    @classmethod
    def from_dict(cls, dict_info):
        if not all(k in dict_info for k in ('address', 'last_inst_addr', 'inst_list', 'size', 'stack_size')):
            raise AttributeError

        if 'parameter' in dict_info.keys():
            parameters = dict_info['parameter']
        else:
            parameters = None

        if 'read_regs' in dict_info.keys():
            read_regs = dict_info['read_regs']
        else:
            read_regs = None

        if 'write_regs' in dict_info.keys():
            write_regs = dict_info['write_regs']
        else:
            write_regs = None

        return cls(address=dict_info['address'], last_inst_addr=dict_info['last_inst_addr'],
                   inst_list=dict_info['inst_list'], size=dict_info['size'],
                   stack_size=dict_info['stack_size'], parameters=parameters,
                   read_regs=read_regs, write_regs=write_regs)

    def __str__(self):
        inst_str = ' \n'.join(self.__inst_list)
        return inst_str

    @property
    def size(self):
        return self.__size

    @property
    def stack_size(self):
        return self.__stack_size

    @property
    def inst_count(self):
        return len(self.__inst_list)

    @property
    def address(self):
        return self.__address

    @property
    def last_inst_addr(self):
        return self.__last_inst_addr

    @property
    def affected_regs(self):
        return self.__write_regs

    @property
    def raw_data(self):
        data = b''
        data += p64(self.__address)
        if self.__parameters is None:
            return data
        for param in self.__parameters:
            data += p64(param)
        return data[:self.__stack_size]

    def to_dict(self):
        info = {'address': self.__address, 'last_inst_addr': self.__last_inst_addr,
                'inst_list': self.__inst_list, 'size': self.__size,
                'stack_size': self.__stack_size, 'parameters': self.__parameters,
                'read_regs': self.__read_regs, 'write_regs': self.__write_regs}
        return info

    def add_parameter(self, param):
        self.__parameters.append(param)


class ROPChain:
    def __init__(self):
        self.__gadget_list = []

    @classmethod
    def from_json(cls, json_data):
        data_info = json.loads(json_data)
        obj = cls()
        for data in data_info:
            obj.__gadget_list.append(ROPGadget.from_dict(data))
        return obj

    def __str__(self):
        chain_str = ''
        for gadget in self.__gadget_list:
            chain_str += str(gadget)
            chain_str += '\n'
        return chain_str

    @property
    def inst_count(self):
        count = 0
        for gadget in self.__gadget_list:
            count += gadget.inst_count
        return count

    @property
    def stack_size(self):
        size = 0
        for gadget in self.__gadget_list:
            size += gadget.stack_size
        return size

    @property
    def raw_data(self):
        data = b''
        for gadget in self.__gadget_list:
            data += gadget.raw_data
        return data

    @property
    def gadget_list(self):
        return self.__gadget_list

    def add_gadget(self, gadget):
        self.__gadget_list.append(gadget)

    def to_json(self):
        data = []
        for gadget in self.__gadget_list:
            data.append(gadget.to_dict())
        return json.dumps(data)


if __name__ == "__main__":
    r1 = ROPGadget(0x1234, 0x1235, ['pop rdi;', 'ret;'], size=4, stack_size=16)
    r2 = ROPGadget(0x2234, 0x2235, ['pop rsi;', 'ret;'], size=4, stack_size=16)
    r1.add_parameter(0x4567)
    r2.add_parameter(0xabcd)
    # print(r1)
    # print(r2)
    R = ROPChain()
    R.add_gadget(r1)
    R.add_gadget(r2)
    # print(R)
    # print(R.inst_count)
    # print(R.stack_size)
    # print(R.raw_data)
    print(R.to_json())

    R2 = ROPChain.from_json(R.to_json())
    print(R2.raw_data)