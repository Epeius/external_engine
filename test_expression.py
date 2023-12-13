from program_state.expressions import *
from program_state.constraint import *
from program_state.variables import *
c = ConstExpression(1)
vim = VIMExpression(ConstExpression(0x1234), 1, 16)
add = AddExpression(c,  vim)
vir = VIRExpression('rbx', 0, 8)
add_2 = AddExpression(add, vir)
final = GeExpression(add_2, ConstExpression(0x41))
print(final)
print('----------------------------------------')
final.visit(print)
print('----------------------------------------')
print(final.to_json)
#
# new_expr = construct_expression_from_json(final.to_json)
# print(new_expr)
#
#
# cons = Constraint()
# cons.add_expression(final)
# cons.add_expression(GeExpression(c, get_int_from_memory(ConstExpression(1233455566), 1, 16)))
# print(cons)
# new_cons = Constraint()
# new_cons.from_json(cons.to_json)
# print(new_cons)



