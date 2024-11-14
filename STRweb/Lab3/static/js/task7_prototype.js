class Person {
  constructor(lastName, city) {
    this.lastName = lastName;
    this.city = city;
  }

  getLastName() {
    return this.lastName;
  }

  setLastName(lastName) {
    this.lastName = lastName;
  }

  getCity() {
    return this.city;
  }

  setCity(city) {
    this.city = city;
  }
}

class Resident extends Person {
  constructor(lastName, city, street, houseNumber, apartmentNumber) {
    super(lastName, city);
    this.street = street;
    this.houseNumber = houseNumber;
    this.apartmentNumber = apartmentNumber;
  }

  getStreet() {
    return this.street;
  }

  setStreet(street) {
    this.street = street;
  }

  getHouseNumber() {
    return this.houseNumber;
  }

  setHouseNumber(houseNumber) {
    this.houseNumber = houseNumber;
  }

  getApartmentNumber() {
    return this.apartmentNumber;
  }

  setApartmentNumber(apartmentNumber) {
    this.apartmentNumber = apartmentNumber;
  }
}

let residents = [];

function addResident() {
  const lastName = document.getElementById("lastName").value;
  const city = document.getElementById("city").value;
  const street = document.getElementById("street").value;
  const houseNumber = document.getElementById("houseNumber").value;
  const apartmentNumber = document.getElementById("apartmentNumber").value;

  const resident = new Resident(lastName, city, street, houseNumber, apartmentNumber);
  residents.push(resident);
  displayResidents();
}

function displayResidents() {
  const list = document.getElementById("residentsList");
  list.innerHTML = ""; // очищаем список перед обновлением
  residents.forEach((resident, index) => {
    const listItem = document.createElement("li");
    listItem.textContent = `${resident.getLastName()} из ${resident.getCity()}, ${resident.getStreet()} дом ${resident.getHouseNumber()}, кв. ${resident.getApartmentNumber()}`;
    list.appendChild(listItem);
  });
}

function findMatchingResidents() {
  let matches = []; // Массив для хранения всех совпадений

  for (let i = 0; i < residents.length; i++) {
    for (let j = i + 1; j < residents.length; j++) {
      if (
        residents[i].city !== residents[j].city &&
        residents[i].street === residents[j].street &&
        residents[i].houseNumber === residents[j].houseNumber &&
        residents[i].apartmentNumber === residents[j].apartmentNumber
      ) {
        // Добавляем совпадение в массив
        matches.push(
          `${residents[i].getLastName()} и ${residents[
            j
          ].getLastName()} живут по адресу: ${residents[i].getStreet()} дом ${residents[
            i
          ].getHouseNumber()}, кв. ${residents[i].getApartmentNumber()} в разных городах.`,
        );
      }
    }
  }

  const matchElement = document.getElementById("matchingResidents");
  if (matches.length > 0) {
    matchElement.innerHTML = matches.join("<br>");
  } else {
    matchElement.innerHTML = "Совпадений не найдено.";
  }
}
