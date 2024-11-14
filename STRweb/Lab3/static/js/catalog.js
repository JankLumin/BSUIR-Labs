document.addEventListener("DOMContentLoaded", () => {
  // URL ваших API для разных категорий недвижимости
  const API_URLS = [
    "/api/apartments/",
    "/api/houses/",
    "/api/commercial_properties/",
    "/api/garages/",
  ];

  const itemsPerPage = 3;
  let currentPage = 1;
  let totalPages = 1;
  let properties = [];

  const catalogContainer = document.getElementById("catalog-container");
  const prevButton = document.getElementById("prev-page");
  const nextButton = document.getElementById("next-page");
  const pageNumbersContainer = document.getElementById("page-numbers");

  // Соответствие типов недвижимости к URL-путям
  const typeToURL = {
    apartment: "apartments",
    house: "houses",
    commercial_property: "commercial_properties",
    garage: "garages",
  };

  // Функция для получения данных из одного API
  async function fetchFromAPI(url) {
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Ошибка при загрузке ${url}: ${response.status}`);
      }
      const data = await response.json();
      // Предполагается, что API возвращает массив объектов
      // Если ваш API возвращает объект с ключом 'results', используйте data.results
      return Array.isArray(data) ? data : data.results || [];
    } catch (error) {
      console.error(error);
      return [];
    }
  }

  // Функция для получения данных из всех API и объединения их в один массив
  async function fetchAllProperties() {
    const fetchPromises = API_URLS.map((url) => fetchFromAPI(url));
    const results = await Promise.all(fetchPromises);
    // Объединяем все массивы в один
    properties = results.flat();

    // Добавляем поле detail_url для каждой недвижимости
    properties = properties.map((property) => {
      let detail_url = "#";
      const urlPath = typeToURL[property.property_type];
      if (urlPath && property.id) {
        detail_url = `/webpages/${urlPath}/${property.id}/`;
      }
      return { ...property, detail_url };
    });

    totalPages = Math.ceil(properties.length / itemsPerPage);
    renderCatalog(currentPage);
    renderPagination();
  }

  // Функция для рендеринга каталога
  function renderCatalog(page) {
    catalogContainer.innerHTML = "";

    const start = (page - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const paginatedItems = properties.slice(start, end);

    if (paginatedItems.length === 0) {
      catalogContainer.innerHTML = "<p>Нет доступных объектов недвижимости.</p>";
      return;
    }

    paginatedItems.forEach((property) => {
      const cardWrapper = document.createElement("div");
      cardWrapper.classList.add("card-wrapper");
      cardWrapper.setAttribute("data-aos", "fade-up");

      // Вся карточка является ссылкой
      const cardLink = document.createElement("a");
      cardLink.classList.add("card", "property-card");
      cardLink.href = property.detail_url;

      // Добавление изображения недвижимости
      let img;
      if (property.photos_read && property.photos_read.length > 0) {
        img = document.createElement("img");
        img.src =
          property.photos_read[0].image || "https://via.placeholder.com/300x200?text=No+Image";
        img.alt = property.title;
        img.classList.add("property-image");
      } else {
        const noImageDiv = document.createElement("div");
        noImageDiv.classList.add("no-image");
        noImageDiv.textContent = "Фото отсутствует";
        img = noImageDiv;
      }

      // Добавление контента карточки
      const cardContent = document.createElement("div");
      cardContent.classList.add("card-content");

      const title = document.createElement("h3");
      title.classList.add("property-title");
      title.textContent = property.title;

      const description = document.createElement("p");
      description.classList.add("property-description");
      description.textContent = property.description;

      const price = document.createElement("p");
      price.classList.add("property-price");
      price.textContent = `Цена: ${property.price}`;

      // Удалена кнопка "Подробнее"

      cardContent.appendChild(title);
      cardContent.appendChild(description);
      cardContent.appendChild(price);
      // Удалена строка с добавлением кнопки detailsButton

      cardLink.appendChild(img);
      cardLink.appendChild(cardContent);
      cardWrapper.appendChild(cardLink);

      catalogContainer.appendChild(cardWrapper);
    });

    AOS.refresh(); // Обновляем AOS после динамического добавления контента
    updatePaginationButtons();
  }

  // Функция для рендеринга навигации
  function renderPagination() {
    pageNumbersContainer.innerHTML = "";

    for (let i = 1; i <= totalPages; i++) {
      const pageButton = document.createElement("button");
      pageButton.textContent = i;
      pageButton.classList.add("page-number");
      if (i === currentPage) {
        pageButton.classList.add("active");
      }
      pageButton.addEventListener("click", () => {
        currentPage = i;
        renderCatalog(currentPage);
        renderPagination();
        scrollToCatalog();
      });
      pageNumbersContainer.appendChild(pageButton);
    }
  }

  // Обновление состояния кнопок "Предыдущая" и "Следующая"
  function updatePaginationButtons() {
    prevButton.disabled = currentPage === 1;
    nextButton.disabled = currentPage === totalPages;
  }

  // Обработчики событий для кнопок навигации
  prevButton.addEventListener("click", () => {
    if (currentPage > 1) {
      currentPage--;
      renderCatalog(currentPage);
      renderPagination();
      scrollToCatalog();
    }
  });

  nextButton.addEventListener("click", () => {
    if (currentPage < totalPages) {
      currentPage++;
      renderCatalog(currentPage);
      renderPagination();
      scrollToCatalog();
    }
  });

  // Прокрутка к каталогу при смене страницы
  function scrollToCatalog() {
    window.scrollTo({
      top: catalogContainer.offsetTop - 100, // Регулируйте значение по необходимости
      behavior: "smooth",
    });
  }

  // Инициализация
  fetchAllProperties();
});
