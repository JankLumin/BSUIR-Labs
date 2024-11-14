// static/js/age_verification.js

document.addEventListener("DOMContentLoaded", function () {
  // Проверяем, была ли уже выполнена проверка возраста
  if (!localStorage.getItem("ageVerified")) {
    // Функция для запроса и обработки даты рождения
    function verifyAge() {
      let dobInput = prompt("Пожалуйста, введите вашу дату рождения в формате ДД.ММ.ГГГГ:");

      if (dobInput) {
        // Разбиваем введенную строку на части
        let parts = dobInput.split(".");
        if (parts.length === 3) {
          let day = parseInt(parts[0], 10);
          let month = parseInt(parts[1], 10) - 1; // Месяцы в JavaScript начинаются с 0
          let year = parseInt(parts[2], 10);

          let birthDate = new Date(year, month, day);
          let today = new Date();

          // Проверяем корректность даты
          if (
            birthDate.getFullYear() !== year ||
            birthDate.getMonth() !== month ||
            birthDate.getDate() !== day
          ) {
            alert("Введена некорректная дата. Пожалуйста, попробуйте снова.");
            verifyAge();
            return;
          }

          // Рассчитываем возраст
          let age = today.getFullYear() - birthDate.getFullYear();
          let monthDifference = today.getMonth() - birthDate.getMonth();
          if (
            monthDifference < 0 ||
            (monthDifference === 0 && today.getDate() < birthDate.getDate())
          ) {
            age--;
          }

          if (age >= 18) {
            // Получаем день недели рождения
            let options = { weekday: "long" };
            let dayOfWeek = birthDate.toLocaleDateString("ru-RU", options);
            alert(`Вам ${age} лет. День недели вашего рождения: ${dayOfWeek}.`);
          } else {
            alert("Для использования сайта необходимо разрешение родителей.");
          }

          // Сохраняем факт прохождения проверки в localStorage
          localStorage.setItem("ageVerified", "true");
        } else {
          alert("Неверный формат даты. Пожалуйста, используйте формат ДД.ММ.ГГГГ.");
          verifyAge();
        }
      } else {
        alert("Для использования сайта необходимо ввести дату рождения.");
        verifyAge();
      }
    }

    // Вызываем функцию проверки возраста
    verifyAge();
  }
});
