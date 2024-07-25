from function_declaration_and_calls import *
from switch_case_parsing import *
from for_loops_parsing import *
from arithmetic_and_logic_parsing import *
from while_parsing import *
from condition_parsing import *
from var_declaration import *

operands = {

}
operators = {

    'func': 0,
}

def calculate_metrics():
    swift_code = open('swift_code.swift').read()
    find_function_declaration2(operators, operands, swift_code)
    find_function_calls(operators, operands, swift_code)
    find_switches(operators, operands, swift_code)
    find_for_loops(operators, operands, swift_code)
    find_while_loops(operators, swift_code)
    find_operators(operators, swift_code)
    count_if_else_constructs(operators, swift_code)
    parse_swift_variable_declarations(operators, operands, swift_code)

if __name__ == '__main__':
    calculate_metrics()

    print('operands', operands)
    print('operators', operators)
