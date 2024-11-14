// BACK/models/Client.js
const db = require("../config/db");

// Создаем таблицу клиентов, если она еще не создана
db.run(
  `CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    contact TEXT
  )`,
  (err) => {
    if (err) {
      console.error("Ошибка создания таблицы clients:", err.message);
    } else {
      console.log("Таблица clients готова.");
    }
  },
);

module.exports = db;
