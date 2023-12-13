# -*- coding: utf-8 -*-

import requests
from config import INPUT_GENERATOR_URL
from utils.io import *


class InputGenQuerior:
    def __init__(self, is_local=False):
        self.url = INPUT_GENERATOR_URL
        self.is_local = is_local

    def query_input(self, session_id, query_name, args):
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

    def check_memory_writable_and_solvable(self, session_id, input_name, state_list, target_addr, offset,
                                           data_to_write, write_size):
        """
        Check if data `data_to_write` can be write to memory at `target_addr`.
        :param session_id: session ID
        :param input_name: input name
        :param state_list: program_state list
        :param target_addr: memory to write
        :param offset: offset from memory pointed by `reg_name`
        :param data_to_write: data to write
        :param write_size: size to write
        :return: True if write success otherwise False. post_input_name & post_state_list
        """

        return True, None, None

    def check_memory_pointed_by_register_writable_and_solvable(self, session_id, input_name, state_list, reg_name,
                                                               offset, data_to_write, write_size):
        """
        Check if data `data_to_write` can be write to memory pointed by register `reg_name`.
        :param session_id: session ID
        :param input_name: input name
        :param state_list: program_state list
        :param reg_name: register name
        :param offset: offset from memory pointed by `reg_name`
        :param data_to_write: data to write
        :param write_size: size to write
        :return: True if write success otherwise False. post_input_name & post_state_list
        """

        return True, None, None
