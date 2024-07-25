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
        print("МЕНЮ")
        print("1. Задание 1")
        print("2. Задание 2")
        print("3. Задание 3")
        print("4. Задание 4")
        print("5. Задание 5")
        print("0. Выход")

        choice = Input_data.input_data("Введите номер задания: ", int, 0, 5)
        print()

        if choice == 1:
            Task1.task1()
        elif choice == 2:
            Task2.task2()
        elif choice == 3:
            Task3.task3()
        elif choice == 4:
            Task4.task4()
        elif choice == 5:
            Task5.task5()
        elif choice == 0:
            print("Завершение программы...")
            break
