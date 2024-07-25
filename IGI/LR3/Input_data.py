import random
import string

def Input_data(prompt, data_type, min_value=None, max_value=None):
    """
    Function to get user input with data type validation and optional value range constraints.

    Args:
    - prompt (str): The prompt message for the user.
    - data_type (type): The expected data type for user input (int, float, or str).
    - min_value (int/float, optional): The minimum allowed value (inclusive). Defaults to None.
    - max_value (int/float, optional): The maximum allowed value (inclusive). Defaults to None.

    Returns:
    - user_input (int/float/str): The validated user input.

    Raises:
    - ValueError: If the user input does not match the specified data type or falls outside the specified range.
    """

    while True:
        try:
            user_input = data_type(input(prompt))
            if min_value is not None and user_input < min_value:
                raise ValueError(f"Value must be at least {min_value}")
            if max_value is not None and user_input > max_value:
                raise ValueError(f"Value must be at most {max_value}")
            return user_input
        except ValueError as e:
            print(f"Error: {e}. Please enter a valid value.")

def Random_Input(data_type, min_value=None, max_value=None):
    """
    Function to generate random data based on the specified data type and optional value range constraints.

    Args:
    - data_type (type): The data type for the generated value (int, float, or str).
    - min_value (int/float, optional): The minimum allowed value (inclusive). Defaults to None.
    - max_value (int/float, optional): The maximum allowed value (inclusive). Defaults to None.

    Returns:
    - generated_value (int/float/str): The randomly generated value.

    Raises:
    - ValueError: If the specified data type is not supported (supported types: int, float, str).
    """

    if data_type == str:
        if min_value is None:
            min_value = 1
        if max_value is None:
            max_value = 10

        generated_value = ''.join(
            random.choices(string.ascii_letters + string.digits, k=random.randint(min_value, max_value)))
        return generated_value

    if min_value is None:
        min_value = float('-inf')
    if max_value is None:
        max_value = float('inf')

    if data_type == int:
        generated_value = random.randint(min_value, max_value)
    elif data_type == float:
        generated_value = random.uniform(min_value, max_value)
    else:
        raise ValueError("Unsupported data type. Supported types are int, float, and str.")

    return generated_value
