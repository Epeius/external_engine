# -*- coding: utf-8 -*-

import requests

# 目标URL，这里假设您的本地服务器在http://localhost:8080 上监听
url = 'http://127.0.0.1:5000/external_module_engine'

# 要发送的数据，可以是一个字典或JSON格式的字符串，这里使用字典示例
query_data = {
    'query_name': 'generate_rop_data',
    'args': [
        {'type': 'string', 'value': ""},  # input_name
        {'type': 'json', 'value': ""}, # state_list
        {'type': 'int', 'value': 0},  # rop_type: DISABLE_NX
        {'type': 'int', 'value': 3735928559},  # mem_start
        {'type': 'int', 'value': 1024},  # mem_len
        {'type': 'string', 'value': ''}
    ]
}
query_data = {
    'query_name': 'generate_rop_data',
    'args': [
        {'type': 'string', 'value': ""},  # input_name
        {'type': 'json', 'value': ""}, # state_list
        {'type': 'int', 'value': 1},  # rop_type: WRTIE_SHELLCODE
        {'type': 'int', 'value': 3735928559},  # mem_start
        {'type': 'string', 'value': 'ABCDEFG'},
        # mem_len
        {'type': 'string', 'value': ''}
    ]
}
data = {'session_id': '1', 'query': query_data}

# 发送POST请求
response = requests.post(url, json=data)

# 检查响应
if response.status_code == 200:
    print("POST请求成功！")
    print("响应内容：", response.text)
else:
    print("POST请求失败，状态码：", response.status_code)
