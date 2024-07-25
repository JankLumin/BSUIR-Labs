import re
def count_if_else_constructs(operators, swift_code):
    else_if_pattern = r'\belse if\b'

    if_pattern = r'\bif\b'

    else_pattern = r'\belse\b'

    else_if_count = len(re.findall(else_if_pattern, swift_code))

    if_count = len(re.findall(if_pattern, swift_code))

    else_count = len(re.findall(else_pattern, swift_code))

    if_count -= else_if_count
    else_count -= else_if_count

    operators['if'] = if_count
    operators['else if'] = else_if_count
    operators['else'] = else_count
