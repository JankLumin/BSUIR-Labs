const toggleLabel = document.createElement("label");
toggleLabel.textContent = "Показать настройки";
toggleLabel.htmlFor = "customization-toggle";

const toggleInput = document.createElement("input");
toggleInput.type = "checkbox";
toggleInput.id = "customization-toggle";

document.body.appendChild(toggleLabel);
document.body.appendChild(toggleInput);

const panel = document.createElement("div");
panel.id = "customization-panel";
panel.style.display = "none";

const fontSizeLabel = document.createElement("label");
fontSizeLabel.textContent = "Размер шрифта:";
fontSizeLabel.htmlFor = "font-size-slider";

const fontSizeSlider = document.createElement("input");
fontSizeSlider.type = "range";
fontSizeSlider.id = "font-size-slider";
fontSizeSlider.min = "10";
fontSizeSlider.max = "50";
fontSizeSlider.value = "16";

panel.appendChild(fontSizeLabel);
panel.appendChild(fontSizeSlider);

const textColorLabel = document.createElement("label");
textColorLabel.textContent = "Цвет текста:";
textColorLabel.htmlFor = "text-color-picker";

const textColorPicker = document.createElement("input");
textColorPicker.type = "color";
textColorPicker.id = "text-color-picker";

panel.appendChild(textColorLabel);
panel.appendChild(textColorPicker);

const bgColorLabel = document.createElement("label");
bgColorLabel.textContent = "Цвет фона:";
bgColorLabel.htmlFor = "background-color-picker";

const bgColorPicker = document.createElement("input");
bgColorPicker.type = "color";
bgColorPicker.id = "background-color-picker";

panel.appendChild(bgColorLabel);
panel.appendChild(bgColorPicker);

document.body.appendChild(panel);

toggleInput.addEventListener("change", function () {
  panel.style.display = this.checked ? "block" : "none";
});

fontSizeSlider.addEventListener("input", function () {
  document.body.style.fontSize = this.value + "px";
});

textColorPicker.addEventListener("input", function () {
  document.documentElement.style.setProperty("--text-color", this.value);
});

bgColorPicker.addEventListener("input", function () {
  document.body.style.backgroundColor = this.value;
});
