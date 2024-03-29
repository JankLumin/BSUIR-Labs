import re
def find_operators(operators, swift_code):
    operators_data = []

    arrow_count = swift_code.count('->')

    operators_to_exclude = ['->']

    pattern = r'(\+\+|--|\+\=|\-\=|\*\*|\/=|==|!=|<=|>=|<<|>>|&&|\|\||[+\-*/%!=<>&|^-]|\(|\))'

    matches = re.findall(pattern, swift_code)

    for operator in matches:
        if operator not in operators_to_exclude:
            operators[operator] = operators.get(operator, 0) + 1

            if operator == '-' and '->' in swift_code:
                operators['->'] = arrow_count

            operators_data.append({
                'operator': operator,
            })

    operators['-'] -= arrow_count
    operators['>'] -= arrow_count
    if operators['-'] == 0:
        del operators['-']
    if operators['>'] == 0:
        del operators['>']
    return operators_data