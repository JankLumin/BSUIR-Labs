// static/js/reset_storage.js

document.addEventListener("DOMContentLoaded", function () {
  const resetButton = document.getElementById("reset-storage");

  if (resetButton) {
    resetButton.addEventListener("click", function () {
      // Очищаем localStorage
      localStorage.clear();

      // Перезагружаем страницу, чтобы изменения вступили в силу
      location.reload();
    });
  }
});
