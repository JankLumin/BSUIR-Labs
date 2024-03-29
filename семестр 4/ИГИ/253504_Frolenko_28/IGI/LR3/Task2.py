import Input_data

def Task2():
    """
    Function to find the smallest number among user-provided or randomly generated integers.

    This function prompts the user for manual or automatic input of integers.
    It then finds and displays the smallest number among the provided integers.

    Args: None

    Returns: None
    """

    minimum_number = None
    choice = Input_data.Input_data("Write 1 for manual input, 2 for automatic input: ", int, 1, 2)
    if choice == 1:
        while True:
            num = Input_data.Input_data("Enter an integer (enter 1 to finish): ", int, None, None)

            if num == 1:
                break

            if minimum_number is None:
                minimum_number = num
            else:
                if num < minimum_number:
                    minimum_number = num
    elif choice == 2:
        x = Input_data.Random_Input(int, 1, 25)
        while x > 0:
            num = Input_data.Random_Input(int, -100000, 100000)
            if num == 1:
                break
            print(num)
            if minimum_number is None:
                minimum_number = num
            else:
                if num < minimum_number:
                    minimum_number = num
            x -= 1

    print("Smallest number:", minimum_number)
