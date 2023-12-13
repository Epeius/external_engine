# -*- coding: utf-8 -*-
import json
from config import VERIFY_CONNECTION_COMMAND
from engine_base import Engine
from rule.predicate import *
from core_submodules.sub_module_list import EXT_MODULES
from core_submodules.generate_ROP import ROPArgsVerifier, ROPGenerator, SURPPOT_ROP_TYPE
from utils.io import *
from state_modifier.interface_planer import SUPPORTED_ACTIONS, StateModifier


class ExternalModuleEngine(Engine):
    """
    外部模块引擎
    """

    def __init__(self):
        super(ExternalModuleEngine, self).__init__()
        self._cache_for_session_id = {}
        self._columns_for_goal = {}
        self._finished_for_session_id = {}
        self.engine_type_str = "External Module Engine"
        self.query_predicate_str = "query_external_modules"
        return

    def process_command(self, cmd):
        """
        处理前端发来的命令
        :param cmd: dict格式的命令，'session_id'键对应会话id，'query'对应用户的查询信息
        :param engine_type: MUST defined in engines.engine_types.
        :return:
        """
        if 'session_id' in cmd:
            session_id = cmd['session_id']
        else:
            return self.return_error_response('Must contain `session_id` argument')

        if 'query' in cmd:
            predicate = cmd['query']
        else:
            return self.return_error_response('Must contain `query` argument')

        if 'index' in cmd:
            try:
                index = int(cmd['index'])
            except:
                index = 0
        else:
            index = 0

        try:
            success, res = self.query_predicate(session_id, predicate, index)
        except Exception as e:
            return self.return_error_response('Exception occurred, exception is {}'.format(str(e)))

        if not success:
            return self.return_error_response(res)
        else:
            return self.return_response(True, res)

    def verify_connection(self, arguments):
        args = []
        for argument in arguments:
            arg = {}
            arg['value'] = argument['value']
            arg['type'] = argument['type']
            arg['concrete'] = 1 if argument['type'] != 'var' else '0'
            args.append(arg)

        return True, {'valid': 1, 'args': args}

    def query_predicate(self, session_id, predicate, index):
        """
        根据前端提交的请求，查询相应的语义
        :param session_id: 会话id
        :param predicate: 需要处理的请求
        :return: 一个二元组，第一个元素True表示执行成功，第二个元素为一个{'valid':0/1, 'args':[XXXX]}的值。'valid'表示该predicate是否成立，args表示使该predicate成立的具体参数。
                 当第一个元素为False时，表示执行失败，此时第二个元素为失败的具体信息。
                 需要特别注意的是，query_semantics请求是有状态的，即如果对应某一个session_id未调用reset_semantics请求，
                 对应同一个session_id和predicate，语义引擎应该返回不同的值（规划引擎会自动缓存之前的返回的结果）。
        """
        try:
            goal = predicate['query_name']
            arguments = predicate['args']
        except:
            return False, {'valid': 0, 'args': []}

        DEBUG("Get post function %s" % goal)
        DEBUG(str(arguments))
        if goal.lower() == VERIFY_CONNECTION_COMMAND.lower():
            DEBUG("[{}] <==> Processing `{}({})` in session `{}` with index={}".format(self.engine_type_str,
                                                                                       self.query_predicate_str,
                                                                                       arguments, session_id, index))
            return self.verify_connection(arguments)

        if goal.lower() == EXT_MODULES.MODULE_GEN_ROP.lower():
            return self.__process_generate_ROP_chain_request(session_id, arguments)

        if goal.lower() == EXT_MODULES.MODULE_WRITE_ROP.lower():
            return True, {'valid': 1, 'args': []}

        if goal.lower() in SUPPORTED_ACTIONS:
            self.__process_state_modify_request(session_id, arguments)

        return True, {'valid': 1, 'args': []}

    def __process_generate_ROP_chain_request(self, session_id, arguments):
        """
        处理产生ROP数据的请求
        :param arguments: arguments from POST request
        :return: ROP chain data if success otherwise None
        """
        verify_result = ROPArgsVerifier.verify(arguments)
        args = verify_result['args']
        if args is None:
            FATAL("ERROR: %s" % verify_result['info'])
            return {'valid': 0, 'args': []}

        generator = ROPGenerator(session_id, args)
        [rop_chain, success] = generator.generate()
        if not success:
            return {'valid': 0, 'args': []}

        ret_args = arguments
        if args['rop_type'] == SURPPOT_ROP_TYPE.DISABLE_NX:
            ret_args[5] = {'type': 'json', 'value': rop_chain.to_json()}
        if args['rop_type'] == SURPPOT_ROP_TYPE.WRTIE_SHELLCODE:
            ret_args[5] = {'type': 'json', 'value': rop_chain.to_json()}
        if args['rop_type'] == SURPPOT_ROP_TYPE.STACK_PIVOT:
            ret_args[4] = {'type': 'json', 'value': rop_chain.to_json()}

        OK("Generate ROP data success!")
        DEBUG(str(ret_args))
        return {'valid': 1, 'args': ret_args}

    def __process_state_modify_request(self, session_id, arguments):
        modifier = StateModifier(session_id, arguments)
        modifier.do_act()
        return {'valid': 1, 'args': ''}


    def _is_json_arg(self, arg):
        try:
            json.loads(arg)
        except:
            return False
        return True


def main():
    se = ExternalModuleEngine()
    # se._convert_to_mysql_json_object({'a':1,'b':2})
    return


if __name__ == "__main__":
    main()
