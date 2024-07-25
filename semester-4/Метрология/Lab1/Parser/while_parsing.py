import re
def find_while_loops(operators, swift_code):
    pattern = r'\bwhile\s+([^{\n]+)\s*{([^}]*)}'

    matches = re.findall(pattern, swift_code, re.DOTALL)

    while_loop_data = []

    for match in matches:
        operators['while'] = operators.get('while', 0) + 1
        condition = match[0].strip()
        loop_body = match[1]

        while_loop_data.append({
            'condition': condition,
            'loop_body': loop_body,
        })

    return while_loop_data
