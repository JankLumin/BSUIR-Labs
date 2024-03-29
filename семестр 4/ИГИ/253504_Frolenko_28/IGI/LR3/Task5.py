import Input_data

def input_float_list():
    """
    Function to input a list of floating-point numbers.

    This function prompts the user for manual or automatic input of floating-point numbers.
    It returns a list containing the input numbers.

    Args: None

    Returns:
    - float_list (list): List of floating-point numbers.
    """

    float_list = []
    choice = Input_data.Input_data("Write 1 for manual input, 2 for automatic input: ", int, 1, 2)
    if choice == 1:
        while True:
            value = Input_data.Input_data("Enter a floating-point number (enter '0' to finish): ", float, None, None)
            if value == 0:
                break
            float_list.append(value)
    elif choice == 2:
        x = Input_data.Random_Input(int, 1, 15)
        while x > 0:
            value = Input_data.Random_Input(float, -100000, 100000)
            float_list.append(value)
            x -= 1
        print(float_list)
    return float_list


def find_max_absolute_value(float_list):
    """
    Function to find the maximum absolute value in a list of floating-point numbers.

    This function takes a list of floating-point numbers as input and returns the maximum absolute value.

    Args:
    - float_list (list): List of floating-point numbers.

    Returns:
    - max_absolute_value (float): Maximum absolute value in the list.
    """

    if not float_list:
        return None
    return max(float_list, key=abs)


def sum_before_last_positive(float_list):
    """
    Function to calculate the sum of elements before the last positive number in a list.

    This function takes a list of floating-point numbers as input and calculates the sum of elements
    before the last positive number in the list.

    Args:
    - float_list (list): List of floating-point numbers.

    Returns:
    - sum_before_last_pos (float): Sum of elements before the last positive number.
    """

    if not float_list:
        return 0
    last_positive_index = -1
    for i, num in enumerate(float_list):
        if num > 0:
            last_positive_index = i
    return sum(float_list[:last_positive_index])


def Task5():
    """
    Function to perform tasks on a list of floating-point numbers.

    This function inputs a list of floating-point numbers, finds the maximum absolute value,
    and calculates the sum of elements before the last positive number in the list.

    Args: None

    Returns: None
    """

    numbers = input_float_list()

    if not numbers:
        print("Error: The list is empty.")
        return

    max_absolute_value = find_max_absolute_value(numbers)
    print("Maximum absolute value in the list: ", max_absolute_value)

    sum_before_last_pos = sum_before_last_positive(numbers)
    print("Sum of elements in the list before the last positive element: ", sum_before_last_pos)
