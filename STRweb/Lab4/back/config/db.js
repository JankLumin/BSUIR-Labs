// BACK/config/db.js
const sqlite3 = require("sqlite3").verbose();
const path = require("path");

// Путь к базе данных
const dbPath = path.resolve(__dirname, "../database.sqlite");

// Создаем подключение к базе данных
const db = new sqlite3.Database(dbPath, (err) => {
  if (err) {
    console.error("Ошибка подключения к базе данных:", err.message);
  } else {
    console.log("Подключение к базе данных SQLite успешно установлено.");
  }
});

module.exports = db;
