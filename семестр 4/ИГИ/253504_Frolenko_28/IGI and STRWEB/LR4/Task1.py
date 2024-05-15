import csv
import pickle
import Input_data

class Applicant:
    # Class representing an applicant
    def __init__(self, surname, instrument):
        self._surname = surname
        self._instrument = instrument

    @property
    def surname(self):
        return self._surname

    @surname.setter
    def surname(self, value):
        self._surname = value

    @property
    def instrument(self):
        return self._instrument

    @instrument.setter
    def instrument(self, value):
        self._instrument = value


class Musician(Applicant):
    # Class representing a musician, inheriting from Applicant
    def __init__(self, surname, instrument):
        super().__init__(surname, instrument)
        self._speciality = instrument

    @property
    def speciality(self):
        return self._speciality

    @speciality.setter
    def speciality(self, value):
        self._speciality = value

    def get_info(self):
        # Prints information about the musician
        print("Фамилия:", self.surname)
        print("Инструмент:", self.instrument)
        print("----------------------")

    @staticmethod
    def sort_by_surname(musicians):
        # Sorts a list of musicians by surname
        musicians.sort(key=lambda x: x.surname)


def save_to_csv(musician_list):
    # Saves musician data to a CSV file
    with open("musician.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Фамилия", "Инструмент", "Специальность"])
        for musician in musician_list:
            writer.writerow([musician.surname, musician.instrument, musician.speciality])
    print("Данные успешно сохранены в файл musician.csv.")


def load_from_csv():
    # Loads musician data from a CSV file
    musician_list = []
    with open("musician.csv", mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Пропуск заголовка
        for row in reader:
            musician = Musician(row[0], row[1])
            musician.speciality = row[2]
            musician_list.append(musician)
    return musician_list


def save_to_pickle(musician_list):
    # Saves musician data to a pickle file
    with open("musician.pickle", mode="wb") as file:
        pickle.dump(musician_list, file)
    print("Данные успешно сохранены в файл musician.pickle.")


def load_from_pickle():
    # Loads musician data from a pickle file
    with open("musician.pickle", mode="rb") as file:
        musician_list = pickle.load(file)
    return musician_list


def task1():
    # Main function for the task
    musician_list = []

    while True:
        print("Меню")
        print("1. Добавить музыканта")
        print("2. Вывести список музыкантов")
        print("3. Отсортировать список музыкантов")
        print("4. Вывести музыкантов определенной специальности")
        print("5. Сохранить данные в файл CSV")
        print("6. Загрузить данные из файла CSV")
        print("7. Сохранить данные в файл pickle")
        print("8. Загрузить данные из файла pickle")
        print("0. Выход")

        choice = Input_data.input_data("Выберите пункт меню: ", int, 0, 8)

        if choice == 1:
            musician_data = {"surname": Input_data.input_data("Введите фамилию музыканта: ", str),
                             "instrument": Input_data.input_data("Введите инструмент музыканта: ", str)}

            musician = Musician(musician_data["surname"], musician_data["instrument"])
            musician.get_info()

            musician_list.append(musician)
            print("Музыкант успешно добавлен!")

        elif choice == 2:
            print("Список музыкантов:")
            for musician in musician_list:
                print("Фамилия:", musician.surname)
                print("Инструмент:", musician.instrument)
                print("----------------------")

        elif choice == 3:
            Musician.sort_by_surname(musician_list)
            print("Список музыкантов отсортирован по фамилии.")

        elif choice == 4:
            speciality = input("Введите специальность: ")
            print("Музыканты с заданной специальностью:")
            for musician in musician_list:
                if musician.speciality == speciality:
                    musician.get_info()

        elif choice == 5:
            save_to_csv(musician_list)

        elif choice == 6:
            musician_list = load_from_csv()

        elif choice == 7:
            save_to_pickle(musician_list)

        elif choice == 8:
            musician_list = load_from_pickle()

        elif choice == 0:
            print("Программа завершена.")
            break
