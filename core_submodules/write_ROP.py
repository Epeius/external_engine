from utils.io import *
import json
from other_engine_interfaces.semantic_interface import SemanticQuerior
from other_engine_interfaces.input_generator_interface import InputGenQuerior
from gadgets.rop_gadget import ROPChain, ROPGadget


def write_ROP_data():
    print("Not implemented!")
    return ['', False]


class WriteROPArgsVerifier:
    def __init__(self):
        pass

    @staticmethod
    def verify(arguments):
        if len(arguments) < 6:
            FATAL("Arguments number should NOT be less than 5 for writing ROP data! "
                  "The arguments should be: [input, program_state, rop_start_info, rop_chain_list_json, post_input, post_state]")
            return {'args': None, 'info': "Arguments number should NOT be less than 5 for writing ROP data! "
                                          "The arguments should be: [input, program_state, rop_start_info, rop_chain_list_json, "
                                          "post_input, post_state]."}
        input_name = arguments[0]['value']
        state_list = arguments[1]['value']
        rop_start_info = arguments[2]
        is_rop_start_by_reg = False
        if rop_start_info['type'] == 'str':
            rop_start = rop_start_info['value']  # register
            is_rop_start_by_reg = True
        elif rop_start_info['type'] == 'int':
            rop_start = int(rop_start_info['value'])  # address
        else:
            return {'args': None, 'info': ''}

        rop_chain_list_json = arguments[3]['value']

        args = {'input_name': input_name, 'state_list': state_list, 'rop_start': rop_start,
                'rop_chain_list_json': rop_chain_list_json, 'is_rop_start_by_reg': is_rop_start_by_reg}
        return {'args': args, 'info': ''}


class ROPWriter:
    def __init__(self, session_id, args):
        self.session_id = session_id
        self.args = args
        self.semantic_querior = SemanticQuerior(is_local=True)
        self.input_gen_querior = InputGenQuerior(is_local=True)
        self.gadgets_list = []
        self.is_rop_start_by_reg = args['is_rop_start_by_reg']
        if self.is_rop_start_by_reg:
            self.rop_start_reg_name = args['rop_start']
        else:
            self.rop_start_memory_addr = int(args['rop_start'])

    def recover_gadgets_list(self):
        rop_chain_list_json = self.args['rop_chain_list_json']
        rop_chain_list_info = json.loads(rop_chain_list_json)
        for each_json_info in rop_chain_list_info:
            rop_chain = ROPChain.from_json(each_json_info)
            self.gadgets_list += rop_chain.gadget_list

        return

    def find_suitable_position_for_gadget(self, gadget, write_offset, controllable_size, all_add_rsp_gadgets):
        raw_data = gadget.raw_data
        stack_size = gadget.stack_size

        current_offset = write_offset
        while current_offset < controllable_size:
            if self.is_rop_start_by_reg:
                success, post_input_name, post_state_list = self.input_gen_querior. \
                    check_memory_pointed_by_register_writable_and_solvable(self.session_id, self.args['input_name'],
                                                                           self.args['state_list'],
                                                                           self.rop_start_reg_name, current_offset,
                                                                           raw_data, stack_size)
            else:
                success, post_input_name, post_state_list = self.input_gen_querior. \
                    check_memory_writable_and_solvable(self.session_id, self.args['input_name'],
                                                       self.args['state_list'],
                                                       self.rop_start_memory_addr, current_offset, raw_data, stack_size)
            if success:
                return True, current_offset, post_input_name, post_state_list
            else:
                for add_rsp_offset in all_add_rsp_gadgets.keys():
                    for add_rsp_gadget in all_add_rsp_gadgets[add_rsp_offset]:
                        add_rsp_gadget_raw_data = add_rsp_gadget.raw_data
                        add_rsp_gadget_stack_size = add_rsp_gadget.stack_size
                        # first check if we can write add rsp gadget to current offset
                        if self.is_rop_start_by_reg:
                            add_rsp_success, post_input_name, post_state_list = self.input_gen_querior. \
                                check_memory_pointed_by_register_writable_and_solvable(self.session_id,
                                                                                       self.args['input_name'],
                                                                                       self.args['state_list'],
                                                                                       self.rop_start_reg_name,
                                                                                       current_offset,
                                                                                       add_rsp_gadget_raw_data,
                                                                                       add_rsp_gadget_stack_size)
                        else:
                            add_rsp_success, post_input_name, post_state_list = self.input_gen_querior. \
                                check_memory_writable_and_solvable(self.session_id, self.args['input_name'],
                                                                   self.args['state_list'],
                                                                   self.rop_start_memory_addr, current_offset,
                                                                   add_rsp_gadget_stack_size,
                                                                   add_rsp_gadget_stack_size)
                        if add_rsp_success:
                            # then check if we can write target gadget to memory adding the add_rsp_offset
                            new_offset = current_offset + add_rsp_offset
                            if self.is_rop_start_by_reg:
                                new_success, post_input_name, post_state_list = self.input_gen_querior. \
                                    check_memory_pointed_by_register_writable_and_solvable(self.session_id,
                                                                                           self.args['input_name'],
                                                                                           self.args['state_list'],
                                                                                           self.rop_start_reg_name,
                                                                                           new_offset,
                                                                                           raw_data, stack_size)
                            else:
                                new_success, post_input_name, post_state_list = self.input_gen_querior. \
                                    check_memory_writable_and_solvable(self.session_id, self.args['input_name'],
                                                                       self.args['state_list'],
                                                                       self.rop_start_memory_addr, new_offset,
                                                                       raw_data, stack_size)
                            if new_success:
                                return True, new_offset, post_input_name, post_state_list

        return False, 0, None, None

    def write_to_memory(self):
        if self.is_rop_start_by_reg:
            controllable_size = self.semantic_querior. \
                get_controllable_memory_size_pointed_by_register(self.session_id, self.args['input_name'],
                                                                 self.args['state_list'], self.rop_start_reg_name)
        else:
            controllable_size = self.semantic_querior. \
                get_controllable_memory_size_at_address(self.session_id, self.args['input_name'],
                                                        self.args['state_list'], self.rop_start_memory_addr)
        if controllable_size is None:
            FATAL("Cannot find any controllable memory!")
            return [None, False]

        gadgets_stack_size = 0
        for gadget in self.gadgets_list:
            gadgets_stack_size += gadget.stack_size

        if gadgets_stack_size > controllable_size:  # quickly return if size is not compatible
            return [None, False]

        all_add_rsp_gadgets = self.semantic_querior.get_all_add_rsp_gadgets(self.session_id, self.args['input_name'],
                                                                            self.args['state_list'])

        write_offset = 0
        for gadget in self.gadgets_list:
            success, offset, post_input_name, post_state_list = \
                self.find_suitable_position_for_gadget(gadget, write_offset, controllable_size, all_add_rsp_gadgets)
            if not success:
                FATAL("Failed to write gadget!")
                break
            write_offset += offset

        return [None, True]
