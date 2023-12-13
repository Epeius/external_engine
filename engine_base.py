# -*- coding: utf-8 -*-
from helper import gen_hash

class Engine:
    def __init__(self):
        self._dispatch_table = {}
        return



    def dispatch_funcion(self, function, session_id, goal):
        if function.lower() in self._dispatch_table:
            try:
                status, res = self._dispatch_table[function.lower()]['handler'](session_id, goal)
            except Exception as e:
                return False, "Execute `{}({})` exception :`{}`".format(function, goal, str(e))

            return status, res
        else:
            return False, "No handler for `{}({})`".format(function, goal)


    def get_hash(self, goal):
        return gen_hash(goal)

    def register_request_handler(self, key_string, callback_func, comment=''):
        self._dispatch_table[key_string] = {'handler':callback_func, 'comment':comment}
        return



    def return_error_response(self, info):
        return {'status':0, 'info':info, 'data':{'valid':0, 'args':[]}}

    def return_response(self, status, data):
        return {'status':1 if status==True else 0, 'data':data, 'info':''}


    def _extract_knowledge_predicate(self, query):
        '''
        从query中抽取具体的参数
        :param query: 形如function(args)的字符串
        :return:    提取的参数信息，function作为goal返回，args作为arguments_str返回
        '''
        if 'query_name' in query:
            goal = query['query_name']
        else:
            goal = ''

        if 'args' in query and len(query['args']) > 0:
            arguments_str = query['args'][0]['value'].strip('"')
        else:
            arguments_str = ''


        # goal_end_pos = query.find("(")
        # arguments_end = query.find(")")
        # if goal_end_pos != -1 and arguments_end != -1 and arguments_end < goal_end_pos:
        #     return None,None
        #
        # if query.find('(', goal_end_pos + 1) != -1:
        #     return None,None
        # if query.find(")", arguments_end + 1) != -1:
        #     return None,None
        #
        # goal = query[0:goal_end_pos].strip()
        # arguments_str = query[goal_end_pos + 1:arguments_end]
        return goal, arguments_str


