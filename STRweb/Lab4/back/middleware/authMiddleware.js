// BACK/middleware/authMiddleware.js
const jwt = require("jsonwebtoken");

function authenticateToken(req, res, next) {
  const authHeader = req.headers["authorization"];
  const token = authHeader && authHeader.split(" ")[1]; // Ожидаем формат "Bearer TOKEN"

  if (token == null) {
    return res.status(401).json({ error: "Токен отсутствует" });
  }

  jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
    if (err) {
      return res.status(403).json({ error: "Токен недействителен" });
    }
    req.user = user;
    next();
  });
}

module.exports = authenticateToken;
