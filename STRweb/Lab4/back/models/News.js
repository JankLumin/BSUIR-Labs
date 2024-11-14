// BACK/models/News.js
const db = require("../config/db");

// Создаем таблицу новостей, если она еще не создана
db.run(
  `CREATE TABLE IF NOT EXISTS news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    content TEXT,
    date TEXT
  )`,
  (err) => {
    if (err) {
      console.error("Ошибка создания таблицы news:", err.message);
    } else {
      console.log("Таблица news готова.");
    }
  },
);

module.exports = db;
