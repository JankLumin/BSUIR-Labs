function Person(lastName, city) {
  this.lastName = lastName;
  this.city = city;
}

Person.prototype.getLastName = function () {
  return this.lastName;
};

Person.prototype.setLastName = function (lastName) {
  this.lastName = lastName;
};

Person.prototype.getCity = function () {
  return this.city;
};

Person.prototype.setCity = function (city) {
  this.city = city;
};

function Resident(lastName, city, street, houseNumber, apartmentNumber) {
  Person.call(this, lastName, city);
  this.street = street;
  this.houseNumber = houseNumber;
  this.apartmentNumber = apartmentNumber;
}

Resident.prototype = Object.create(Person.prototype);
Resident.prototype.constructor = Resident;

Resident.prototype.getStreet = function () {
  return this.street;
};

Resident.prototype.setStreet = function (street) {
  this.street = street;
};

Resident.prototype.getHouseNumber = function () {
  return this.houseNumber;
};

Resident.prototype.setHouseNumber = function (houseNumber) {
  this.houseNumber = houseNumber;
};

Resident.prototype.getApartmentNumber = function () {
  return this.apartmentNumber;
};

Resident.prototype.setApartmentNumber = function (apartmentNumber) {
  this.apartmentNumber = apartmentNumber;
};

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
  list.innerHTML = "";
  residents.forEach((resident, index) => {
    const listItem = document.createElement("li");
    listItem.textContent = `${resident.getLastName()} из ${resident.getCity()}, ${resident.getStreet()} дом ${resident.getHouseNumber()}, кв. ${resident.getApartmentNumber()}`;
    list.appendChild(listItem);
  });
}

function findMatchingResidents() {
  let matches = [];

  for (let i = 0; i < residents.length; i++) {
    for (let j = i + 1; j < residents.length; j++) {
      if (
        residents[i].city !== residents[j].city &&
        residents[i].street === residents[j].street &&
        residents[i].houseNumber === residents[j].houseNumber &&
        residents[i].apartmentNumber === residents[j].apartmentNumber
      ) {
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
