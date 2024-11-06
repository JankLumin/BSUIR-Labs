document.addEventListener("DOMContentLoaded", function () {
  document.addEventListener("click", function (e) {
    const target = e.target.closest("a.page-link");
    if (target) {
      e.preventDefault();
      const url = target.href;

      fetch(url, {
        headers: { "X-Requested-With": "XMLHttpRequest" },
      })
        .then((response) => response.text())
        .then((html) => {
          const parser = new DOMParser();
          const doc = parser.parseFromString(html, "text/html");
          const newContent = doc.querySelector("#productListContainer").innerHTML;
          document.querySelector("#productListContainer").innerHTML = newContent;
        })
        .catch((error) => console.error("Error loading page:", error));
    }
  });
});
