import re
def parse_swift_variable_declarations(operators, operands, swift_code):
    pattern = r'\b(var|let)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*(=\s*([^;]*))?\s*;'

    matches = re.finditer(pattern, swift_code)

    for match in matches:
        var_type = match.group(3)
        var_name = match.group(2)
        var_value = match.group(5)

        operands[var_name] = operands.get(var_name, 0) + 1
        operands[var_value] = operands.get(var_value, 0) + 1
        operators[var_type] = operators.get(var_type, 0) + 1
