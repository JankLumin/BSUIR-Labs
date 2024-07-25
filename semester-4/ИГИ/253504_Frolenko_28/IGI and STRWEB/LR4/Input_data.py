def input_data(prompt, data_type, min_value=None, max_value=None):
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
