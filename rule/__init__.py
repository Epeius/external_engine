# -*- coding: utf-8 -*-
from rule.predicate import Predicate
from rule.argument_parser import ArgumentParser
class Rule:
    def __init__(self, rule_str):
        self._goal, self._conditions = self._init_from_str(rule_str)
        if self._goal !=None:
            self._rule_str = rule_str
        else:
            self._rule_str = ''

        return

    def _init_from_str(self, rule_str):
        comment_end = rule_str.find('#')
        if comment_end == -1:
            comment_end = rule_str.find('%')

        if comment_end != -1:
            rule_str = rule_str[0:comment_end]

        rule_str = rule_str.strip().rstrip('.').lstrip('-').strip()

        pos = rule_str.find(':-')
        if pos == -1:
            return Predicate(rule_str), []


        goal_str = rule_str[0:pos]
        goal = Predicate(goal_str)
        condition_str = rule_str[pos+2:]
        condition_str = condition_str.strip()
        if condition_str[0] == '(' and condition_str[-1] == ')':
            condition_str = condition_str[1:-1]
        conditions = ArgumentParser(condition_str).get_arguments()

        return goal, conditions

    def get_goal(self):
        return self._goal

    def get_conditions(self):
        return self._conditions

    def is_valid(self):
        if self._goal == None:
            return  False
        return True

    def _is_symbolic_arg(self, arg_str):
        if arg_str[0].isupper():
            return True
        return False

    def get_conditions_str(self):
        return ', '.join(self._conditions)

    def __str__(self):
        if self._goal != None:
            if len(self._conditions) != 0:
                return "{} :- {}.".format(str(self._goal), ', '.join(self._conditions))
            else:
                return "{}.".format(str(self._goal))
        else:
            return ''
def main():
    s = "integer_to_4_bytes(Number, Bytes) :- B0 is Number /\ 255, B1 is (Number >> 8) /\ 255, B2 is (Number >> 16) /\ 255, B3 is (Number >> 24) /\ 255, Bytes = [B0, B1, B2, B3]."
    s = "a:-true"
    s = 'linux_get_shell:-(execute_func_by_symbol(system,[/bin/sh]):-(get_symbol_address(system,134517232):-(in_main_image(system):-semantics),(get_symbol_in_main_image(system,134517232):-(is_pie:-not_hold),(get_symbol_address_in_none_pie(system,134517232):-semantics))),(generate_args([/bin/sh],[arg(pointer,/bin/sh,3211817072)]):-(generate_arg(/bin/sh,arg(pointer,/bin/sh,3211817072)):-(string(/bin/sh):-builtin),(arg(pointer,/bin/sh,3211817072)=arg(pointer,/bin/sh,3211817072):-builtin)),(generate_args([],[]):-true)),(execute_func(134517232,[arg(pointer,/bin/sh,3211817072)]):-(direct_executed(134517232):-not_hold),(manipulate_args([arg(pointer,/bin/sh,3211817072)]):-(manipulate_arg(arg(pointer,/bin/sh,3211817072)):-(is_arg_ready(arg(pointer,/bin/sh,3211817072)):-not_hold),(prepare_arg(arg(pointer,/bin/sh,3211817072)):-(write_data_to_memory(/bin/sh,3211817072):-(existing_code_write_fixed_controllable_mem(134523562,3211817072):-semantics),(write_content_by_exec_code(134523562,3211817072,/bin/sh):-(code_reachable(134523562):-semantics),(string_to_bytes(/bin/sh,[47,98,105,110,47,115,104]):-(atom_chars(/bin/sh,[/,b,i,n,/,s,h]):-builtin),(char_list_to_integer_list([/,b,i,n,/,s,h],[47,98,105,110,47,115,104]):-(char_code(/,47):-builtin),(char_list_to_integer_list([b,i,n,/,s,h],[98,105,110,47,115,104]):-(char_code(b,98):-builtin),(char_list_to_integer_list([i,n,/,s,h],[105,110,47,115,104]):-(char_code(i,105):-builtin),(char_list_to_integer_list([n,/,s,h],[110,47,115,104]):-(char_code(n,110):-builtin),(char_list_to_integer_list([/,s,h],[47,115,104]):-(char_code(/,47):-builtin),(char_list_to_integer_list([s,h],[115,104]):-(char_code(s,115):-builtin),(char_list_to_integer_list([h],[104]):-(char_code(h,104):-builtin),(char_list_to_integer_list([],[]):-true))))))))),(generate_code_constraint(134523562):-(format(atom(Generating Code constraint for 0x804aaaa ),Generating Code constraint for 0x~|~`0t~16r~4+ ,[134523562]):-builtin),(write(Generating Code constraint for 0x804aaaa ):-builtin),(_1008:-builtin),true),(generate_data_constraint(3211817072,[47,98,105,110,47,115,104]):-(format(atom(Generating Data constraint for 0xbf707070 ),Generating Data constraint for 0x~|~`0t~16r~4+ ,[3211817072]):-builtin),(write(Generating Data constraint for 0xbf707070 ):-builtin),(_1074:-builtin),true))))),(manipulate_args([]):-true)),(extract_arg_values([arg(pointer,/bin/sh,3211817072)],[3211817072]):-(extract_arg_value(arg(pointer,/bin/sh,3211817072),3211817072):-(3211817072=3211817072:-builtin)),(extract_arg_values([],[]):-true)),(control_flow_to(134517232,[3211817072]):-(direct_flow_to(134517232):-not_hold),(hijack_control_flow_to(134517232,[3211817072]):-(has_stack_overflow(2152259245):-semantics),(hijack_cf_by_stack_of(2152259245,134517232,[3211817072]):-(can_overflow_ret(2152259245,2152267434,168430090):-semantics),(overflow_ret_by_stack_of(2152267434,168430090,134517232,[3211817072]):-(canary_enabled:-not_hold),(overflow_ret_by_stack_of_without_canary(2152267434,168430090,134517232,[3211817072]):-(nx_enabled:-not_hold),(write(Setting up args...):-builtin),(_1432:-builtin),(setup_args_for_inst(2152267434,[3211817072]):-(is_x86:-semantics),(generate_code_constraint(2152267434):-(format(atom(Generating Code constraint for 0x8048feaa ),Generating Code constraint for 0x~|~`0t~16r~4+ ,[2152267434]):-builtin),(write(Generating Code constraint for 0x8048feaa ):-builtin),(_1558:-builtin),true),(generate_data_constraint_for_stack_args(2152267434,[3211817072]):-(length([3211817072],1):-builtin),(4 is 1*4:-builtin),(2152267430 is 2152267434-4:-builtin),(integer_list_to_bytes(32,[3211817072],[112,112,112,191]):-(integer_to_4_bytes(3211817072,[112,112,112,191]):-(112 is 3211817072/\255:-builtin),(112 is 3211817072>>8/\255:-builtin),(112 is 3211817072>>16/\255:-builtin),(191 is 3211817072>>24/\255:-builtin),([112,112,112,191]=[112,112,112,191]:-builtin)),(first_element([112,112,112,191],112):-true),(tail_elements([112,112,112,191],[112,112,191]):-true),(integer_list_to_bytes(32,[],[]):-true),(append([112,112,191],[],[112,112,191]):-builtin)),(generate_data_constraint(2152267430,[112,112,112,191]):-(format(atom(Generating Data constraint for 0x8048fea6 ),Generating Data constraint for 0x~|~`0t~16r~4+ ,[2152267430]):-builtin),(write(Generating Data constraint for 0x8048fea6 ):-builtin),(_2004:-builtin),true))),(write(Overflow ret address...):-builtin),(_2028:-builtin),(overflow_ret_by_stack_of_without_canary_nx(2152267434,168430090,134517232):-(generate_code_constraint(2152267434):-(format(atom(Generating Code constraint for 0x8048feaa ),Generating Code constraint for 0x~|~`0t~16r~4+ ,[2152267434]):-builtin),(write(Generating Code constraint for 0x8048feaa ):-builtin),(_7918:-builtin),true),(generate_data_constraint(168430090,134517232):-(format(atom(Generating Data constraint for 0xa0a0a0a ),Generating Data constraint for 0x~|~`0t~16r~4+ ,[168430090]):-builtin),(write(Generating Data constraint for 0xa0a0a0a ):-builtin),(_8014:-builtin),true)))))))))'
    # s = 'prepare_arg(arg(_, _, X)) :- \+ var(X).'
    s = "predicate(1,2,4,[1,3,4,5],a(b),json([a=1,b=2,c=3,d=4,e=[321,123,0x44]]), [31,41,json([a=1,b=2]),[1,23,4]])"
    rule = Rule(s)
    print(rule.get_goal())
    print(rule.get_conditions())
    print(str(rule))
    return


if __name__ == "__main__":
    main()
