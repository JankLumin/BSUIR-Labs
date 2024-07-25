import re
def find_switches(operators, operands, swift_code):
    pattern = r'\bswitch\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*{([^}]*)}'

    matches = re.findall(pattern, swift_code, re.DOTALL)

    switch_data = []

    for match in matches:
        operators['switch'] = operators.get('switch', 0) + 1
        switch_variable = match[0].strip()
        case_block = match[1]

        cases = re.findall(r'\bcase\s+([^:\n]+)', case_block)
        default_match = re.search(r'\bdefault\s*:', case_block)

        if default_match:
            operators['default'] = operators.get('default', 0) + 1

        switch_data.append({
            'switch_variable': switch_variable,
            'cases': cases,
            'has_default': bool(default_match),
        })

        operands[switch_variable] = operands.get(switch_variable, 0) + 1
        for case_value in cases:
            operands[case_value.strip()] = operands.get(case_value.strip(), 0) + 1
            operators['case'] = operators.get('case', 0) + 1
