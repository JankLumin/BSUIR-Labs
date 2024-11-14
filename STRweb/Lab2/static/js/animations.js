// animation.js

document.addEventListener("DOMContentLoaded", function () {
  const overlay = document.getElementById("animation-overlay");

  // Проверяем, существует ли оверлей
  if (overlay) {
    // Добавляем слушатель события окончания анимации fadeOutOverlay
    overlay.addEventListener("animationend", function (event) {
      if (event.animationName === "fadeOutOverlay") {
        overlay.style.display = "none";
      }
    });
  }
});
