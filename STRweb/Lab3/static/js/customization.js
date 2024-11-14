// Обработчик для переключателя настроек
document.getElementById("customization-toggle").addEventListener("change", function () {
  const panel = document.getElementById("customization-panel");
  panel.style.display = this.checked ? "block" : "none";
});

// Изменение размера шрифта
document.getElementById("font-size-slider").addEventListener("input", function () {
  document.body.style.fontSize = this.value + "px";
});

// Изменение цвета текста
document.getElementById("text-color-picker").addEventListener("input", function () {
  document.documentElement.style.setProperty("--text-color", this.value);
});

// Изменение цвета фона
document.getElementById("background-color-picker").addEventListener("input", function () {
  document.body.style.backgroundColor = this.value;
});
