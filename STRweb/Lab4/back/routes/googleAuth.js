// BACK/routes/googleAuth.js
const express = require("express");
const passport = require("passport");
const router = express.Router();

// Маршрут для перенаправления на Google для авторизации
router.get("/google", passport.authenticate("google", { scope: ["profile", "email"] }));

module.exports = router;
