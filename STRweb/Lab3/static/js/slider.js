class Slider {
  constructor(sliderSelector) {
    this.currentSlide = 0; // Текущий слайд
    this.slides = document.querySelectorAll(`${sliderSelector} .slide`); // Все слайды
    this.counterElement = document.querySelector(`${sliderSelector} .slide-counter`); // Нумерация
    this.paginationContainer = document.querySelector(`${sliderSelector} .pagination`); // Пагинация
    this.totalSlides = this.slides.length; // Общее количество слайдов
    this.rotationInterval = 3000; // Интервал автопрокрутки
    this.rotationTimer = null; // Таймер автопрокрутки
    this.initSlider(sliderSelector); // Запуск слайдера
    this.startRotation(); // Старт автопрокрутки
  }

  initSlider(sliderSelector) {
    this.showSlide(this.currentSlide); // Показать первый слайд

    // Обработчики кнопок "назад" и "вперед"
    document
      .querySelector(`${sliderSelector} .prev-zone`)
      .addEventListener("click", () => this.prevSlide());
    document
      .querySelector(`${sliderSelector} .next-zone`)
      .addEventListener("click", () => this.nextSlide());

    this.createPagination(); // Создание пагинации
    this.updateCounter(); // Обновление нумерации

    // Клик по слайду для перехода на URL
    this.slides.forEach((slide) => {
      slide.addEventListener("click", () => {
        const url = slide.getAttribute("data-url");
        if (url) window.open(url, "_blank");
      });
    });
  }

  showSlide(index) {
    // Показать только текущий слайд
    this.slides.forEach((slide, i) => {
      slide.style.display = i === index ? "block" : "none";
    });
    this.updateCounter(); // Обновить нумерацию
    this.updatePagination(); // Обновить активную точку
  }

  nextSlide() {
    // Переход к следующему слайду
    this.currentSlide = (this.currentSlide + 1) % this.totalSlides;
    this.showSlide(this.currentSlide);
  }

  prevSlide() {
    // Переход к предыдущему слайду
    this.currentSlide = (this.currentSlide - 1 + this.totalSlides) % this.totalSlides;
    this.showSlide(this.currentSlide);
  }

  createPagination() {
    this.paginationContainer.innerHTML = ""; // Очистить пагинацию
    for (let i = 0; i < this.totalSlides; i++) {
      const dot = document.createElement("div");
      dot.classList.add("dot");
      if (i === this.currentSlide) dot.classList.add("active"); // Активная точка
      dot.addEventListener("click", () => this.goToSlide(i)); // Переход на слайд
      this.paginationContainer.appendChild(dot);
    }
  }

  updatePagination() {
    // Обновить активную точку пагинации
    const dots = this.paginationContainer.querySelectorAll(".dot");
    dots.forEach((dot, index) => {
      dot.classList.toggle("active", index === this.currentSlide);
    });
  }

  goToSlide(index) {
    // Переход к конкретному слайду
    this.currentSlide = index;
    this.showSlide(this.currentSlide);
  }

  updateCounter() {
    // Обновить нумерацию слайдов
    this.counterElement.textContent = `${this.currentSlide + 1} / ${this.totalSlides}`;
  }

  startRotation() {
    // Запуск автопрокрутки
    this.stopRotation(); // Остановить предыдущий таймер
    this.rotationTimer = setInterval(() => this.nextSlide(), this.rotationInterval);
  }

  stopRotation() {
    // Остановка автопрокрутки
    if (this.rotationTimer) {
      clearInterval(this.rotationTimer);
      this.rotationTimer = null;
    }
  }

  updateInterval() {
    // Обновить интервал автопрокрутки
    const intervalInput = document.getElementById("rotation-interval");
    const newInterval = parseInt(intervalInput.value);
    if (newInterval >= 1000) {
      this.rotationInterval = newInterval;
      this.startRotation(); // Перезапуск с новым интервалом
    } else {
      alert("Интервал должен быть не менее 1000 мс.");
    }
  }
}

// Инициализация слайдера при загрузке страницы
document.addEventListener("DOMContentLoaded", () => {
  window.slider = new Slider(".photo-slider");
});
