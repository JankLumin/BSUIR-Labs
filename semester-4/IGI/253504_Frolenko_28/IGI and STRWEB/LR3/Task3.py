import Input_data

def Task3():
    """
    Function to count the number of lowercase letters and digits in a string.

    This function prompts the user for manual or automatic input of a string.
    It then counts and displays the number of lowercase letters and digits in the string.

    Args: None

    Returns: None
    """

    global user_input
    choice = Input_data.Input_data("Write 1 for manual input, 2 for automatic input: ", int, 1, 2)
    if choice == 1:
        user_input = Input_data.Input_data("Enter a string: ", str, None, None)
    elif choice == 2:
        user_input = Input_data.Random_Input(str, 10, 50)
        print(user_input)

    lowercase_count = 0
    digit_count = 0

    for char in user_input:
        if char.islower():
            lowercase_count += 1
        elif char.isdigit():
            digit_count += 1

    print("Number of lowercase letters: ", lowercase_count)
    print("Number of digits: ", digit_count)
