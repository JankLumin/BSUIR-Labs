import re
def find_for_loops(operators, operands, swift_code):
    pattern = r'\bfor\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+in\s+([^{\n]+)\s*{([^}]*)}'

    matches = re.findall(pattern, swift_code, re.DOTALL)

    for_loop_data = []

    for match in matches:
        operators['for'] = operators.get('for', 0) + 1
        loop_variable = match[0].strip()
        iterable = match[1].strip()
        loop_body = match[2]

        for_loop_data.append({
            'loop_variable': loop_variable,
            'iterable': iterable,
            'loop_body': loop_body,
        })

        operands[loop_variable] = operands.get(loop_variable, 0) + 1
        operands[iterable] = operands.get(iterable, 0) + 1

    return for_loop_data