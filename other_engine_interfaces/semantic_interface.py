# -*- coding: utf-8 -*-

import requests
import json
from config import SEMANTIC_URL
from gadgets.rop_gadget import ROPGadget
from utils.io import *


class SemanticQuerior:
    def __init__(self, is_local=False):
        self.url = SEMANTIC_URL
        self.is_local = is_local

    def __query_semantic(self, session_id, query_name, args):
        query_data = {'query_name': query_name, 'args': args}
        data = {'session_id': session_id, 'query': query_data}
        # 发送POST请求
        response = requests.post(self.url, json=data)
        # 检查响应
        if response.status_code == 200:
            OK("POST请求成功！")
            DEBUG("响应内容：%s" % response.text)
        else:
            FATAL("POST请求失败，状态码：%d" % response.status_code)

        info = response.text
        try:
            processed = info['processed']
        except:
            FATAL("Cannot find processed key in response!")
            return None

        if processed == 0:  # failed
            WARN("Failed to process query: %s, error is %s" % (query_name, info['res']))
            return None

        if processed == 1:  # success
            DEBUG("Successfully processed query: %s" % query_name)
            res_info = info['res']
            if res_info['status'] != 1:
                WARN("Error triggered when processing query: %s" % query_name)
                return None
            return res_info['data']

        if processed == 2:  # pending
            task_id = info['res']
            DEBUG("Pending to process query: %s with task id: %s" % (query_name, task_id))
            return None

        return None

    def get_pop_reg_gadget(self, session_id, input_name, state_list, reg_name):
        """
        Get gadget for pop reg_name.
        :param session_id: session ID
        :param input_name: input name
        :param state_list: program_state list
        :param reg_name: register name
        :return: gadget object if found, otherwise None.
        """
        if self.is_local:
            return ROPGadget.from_dict({'address': 0x1234, 'last_inst_addr': 0x1235,
                                        'inst_list': ['pop %s;' % reg_name, 'ret;'],
                                        'size': 8, 'stack_size': 8})
        query_name = 'get_pop_reg_address',
        args = [
            {'type': 'string', 'value': input_name},  # input_name
            {'type': 'json', 'value': state_list},  # state_list
            {'type': 'str', 'value': reg_name.lower()},  # reg_name
            {'type': 'json', 'value': {}},  # gadget
        ]
        res = self.__query_semantic(session_id, query_name=query_name, args=args)
        if res is None:
            FATAL("Semantic engine failed to find pop %s address" % reg_name)
            return None

        gadget_info = res[3]
        return ROPGadget.from_dict(gadget_info['value'])

    def get_move_reg_to_memory_pointed_by_reg_gadget(self, session_id, input_name, state_list):
        """
        Get gadget for writing memory through mov qword ptr[xxx], xxx.
        :param session_id: session ID
        :param input_name: input name
        :param state_list: program_state list
        :return: gadget, ptr_reg, data_reg.
        """
        if self.is_local:
            return ROPGadget.from_dict({'address': 0x4234, 'last_inst_addr': 0x4235,
                                        'inst_list': ['mov qword ptr[rsi], rdx;', 'ret;'],
                                        'size': 8, 'stack_size': 4}), 'rsi', 'rdx'
        query_name = 'get_move_reg_to_memory_pointed_by_reg_address',
        args = [
            {'type': 'string', 'value': input_name},  # input_name
            {'type': 'json', 'value': state_list},  # state_list
            {'type': 'str', 'value': ''},  # ptr_reg
            {'type': 'str', 'value': ''},  # data_reg
            {'type': 'json', 'value': {}},  # gadget
        ]
        res = self.__query_semantic(session_id, query_name=query_name, args=args)
        if res is None:
            FATAL("Semantic engine failed to find any gadget like writing memory through mov qword ptr[xxx], xxx")
            return None, '', ''

        ptr_reg = res[2]['value']
        data_reg = res[3]['value']
        gadget_info = res[4]
        return ROPGadget.from_dict(gadget_info['value']), ptr_reg, data_reg

    def get_func_plt_address(self, session_id, input_name, state_list, func_name):
        """
        Get PLT table address for function with name func_name.
        :param session_id: session ID
        :param input_name: input name
        :param state_list: program_state list
        :param func_name: function name
        :return: address if found, otherwise None.
        """
        if self.is_local:
            return 0x22345678
        query_name = 'get_func_plt_address',
        args = [
            {'type': 'string', 'value': input_name},  # input_name
            {'type': 'json', 'value': state_list},  # state_list
            {'type': 'str', 'value': func_name.lower()},  # func_name
            {'type': 'int', 'value': 0},  # address
        ]
        res = self.__query_semantic(session_id, query_name=query_name, args=args)
        if res is None:
            FATAL("Semantic engine failed to find func_name %s PLT address" % func_name)
            return None

        address_info = res[3]
        addr = int(address_info['value'])
        return addr

    def get_stack_pivot_address(self, session_id, input_name, state_list, reg_name):
        """
        Get gadget address for exchanging two registers.
        :param session_id: session ID
        :param input_name: input name
        :param state_list: program_state list
        :param reg_name: name of register
        :return: address if found, otherwise None.
        """
        if self.is_local:
            return 0x32345678
        query_name = 'get_stack_pivot_address',
        args = [
            {'type': 'string', 'value': input_name},  # input_name
            {'type': 'json', 'value': state_list},  # state_list
            {'type': 'str', 'value': reg_name.lower()},  # reg_name
            {'type': 'int', 'value': 0},  # address
        ]
        res = self.__query_semantic(session_id, query_name=query_name, args=args)
        if res is None:
            FATAL("Semantic engine failed to pivot to register %s address" % reg_name)
            return None

        address_info = res[3]
        addr = int(address_info['value'])
        return addr

    def get_controllable_memory_size_pointed_by_register(self, session_id, input_name, state_list, reg_name):
        """
        Get size of the controllable memory pointed by register `reg_name`.
        :param session_id: session ID
        :param input_name: input name
        :param state_list: program_state list
        :param reg_name: name of register
        :return: size if found, otherwise None.
        """
        if self.is_local:
            return 1024

        query_name = 'get_controllable_memory_size_pointed_by_register'
        args = [
            {'type': 'string', 'value': input_name},  # input_name
            {'type': 'json', 'value': state_list},  # state_list
            {'type': 'str', 'value': reg_name.lower()},  # reg_name
            {'type': 'int', 'value': 0},  # size
        ]
        res = self.__query_semantic(session_id, query_name=query_name, args=args)
        if res is None:
            FATAL("Semantic engine failed to process controllable memory size pointed by %s" % reg_name)
            return None

        size_info = res[3]
        size = int(size_info['value'])
        return size

    def get_controllable_memory_size_at_address(self, session_id, input_name, state_list, address):
        """
        Get size of the controllable memory at `address`.
        :param session_id: session ID
        :param input_name: input name
        :param state_list: program_state list
        :param address: start of memory
        :return: size if found, otherwise None.
        """
        if self.is_local:
            return 1024

        query_name = 'get_controllable_memory_size_pointed_by_register'
        args = [
            {'type': 'string', 'value': input_name},  # input_name
            {'type': 'json', 'value': state_list},  # state_list
            {'type': 'int', 'value': address},  # address
            {'type': 'int', 'value': 0},  # size
        ]
        res = self.__query_semantic(session_id, query_name=query_name, args=args)
        if res is None:
            FATAL("Semantic engine failed to process controllable memory size at 0x%x" % address)
            return None

        size_info = res[3]
        size = int(size_info['value'])
        return size

    def get_all_add_rsp_gadgets(self, session_id, input_name, state_list):
        """
        Get add rsp, 0x58; ret; gadget.
        :param session_id: session ID
        :param input_name: input name
        :param state_list: program_state list
        :return: gadget object sorted by offset if found, otherwise None.
        """
        if self.is_local:
            r1 = ROPGadget.from_dict({'address': 0x4234, 'last_inst_addr': 0x4235,
                                      'inst_list': ['add rsp 0x58;', 'ret;'],
                                      'size': 8, 'stack_size': 4})
            r2 = ROPGadget.from_dict({'address': 0x4234, 'last_inst_addr': 0x4235,
                                      'inst_list': ['add rsp 0x20;', 'ret;'],
                                      'size': 8, 'stack_size': 4})
            return {0x58: [r1], 0x20: [r2]}

        query_name = 'get_all_add_rsp_gadget'
        args = [
            {'type': 'string', 'value': input_name},  # input_name
            {'type': 'json', 'value': state_list},  # state_list
            {'type': 'json', 'value': ''}  # gadgets json list
        ]
        res = self.__query_semantic(session_id, query_name=query_name, args=args)
        if res is None:
            FATAL("Semantic engine failed to find add RSP gadgets.")
            return None

        all_gadgets_info = json.loads(args[2]['value'])

        all_gadgets = {}
        for gadget_info in all_gadgets_info:
            gadget_dict = gadget_info['gadget']
            gadget = ROPGadget.from_dict(gadget_dict)
            offset = gadget_info['offset']
            if offset not in all_gadgets:
                all_gadgets[offset] = []
            all_gadgets[offset].append(gadget)

        return all_gadgets

