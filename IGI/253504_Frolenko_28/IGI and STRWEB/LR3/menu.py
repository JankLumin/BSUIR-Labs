import Task1
import Task2
import Task3
import Task4
import Task5
import Input_data

def main_menu():
    """
    Function to display the main menu and execute the selected task.

    The function displays a menu with options for each task and prompts the user for input.
    Based on the user's choice, it executes the corresponding task or exits the program.

    Args: None

    Returns: None
    """

    while True:
        print("MENU")
        print("1. Task 1")
        print("2. Task 2")
        print("3. Task 3")
        print("4. Task 4")
        print("5. Task 5")
        print("0. Exit")

        choice = Input_data.Input_data("Enter task number: ", int, 0, 5)

        if choice == 1:
            Task1.Task1()
        elif choice == 2:
            Task2.Task2()
        elif choice == 3:
            Task3.Task3()
        elif choice == 4:
            Task4.Task4()
        elif choice == 5:
            Task5.Task5()
        elif choice == 0:
            print("Exiting program...")
            break
