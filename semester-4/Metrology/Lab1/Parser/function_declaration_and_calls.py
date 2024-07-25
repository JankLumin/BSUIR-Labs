import re
def find_function_declaration2(operators, operands, swift_code):
    pattern = r'\bfunc\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\)(?:\s*->\s*([^\n{]*))?(\s*\{([^}]+)\})?'

    matches = re.finditer(pattern, swift_code, re.DOTALL)

    for match in matches:
        function_name = match.group(1)
        parameters = match.group(2)
        return_type = match.group(3) if match.group(3) else None
        function_body = match.group(5)

        operators[function_name] = operators.get(function_name, 0) + 1
        operators['func'] += 1
        if return_type:
            operators[return_type.strip()] = operators.get(return_type.strip(), 0) + 1

        if parameters:
            parameter_list = re.findall(r'\b(\w+)\s*:\s*([^,]+)', parameters)
            for param_name, param_type in parameter_list:
                operands[param_name] = operands.get(param_name, 0) + 1
                operators[param_type] = operators.get(param_type, 0) + 1

def find_function_calls(operators, operands, swift_code):
    pattern = r'\b(?<!func\s)([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\)'

    matches = re.finditer(pattern, swift_code)

    for match in matches:
        function_name = match.group(1) + '()'
        parameters = match.group(2)

        operators[function_name] = operators.get(function_name, 0) + 1

        if parameters:
            parameters_list = [param.strip() for param in parameters.split(',')]
            for param in parameters_list:
                operands[param] = operands.get(param, 0) + 1