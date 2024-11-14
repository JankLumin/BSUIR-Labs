// BACK/config/passport.js
const GoogleStrategy = require("passport-google-oauth20").Strategy;
const passport = require("passport");
const db = require("../models/User");
const dotenv = require("dotenv");

dotenv.config();

module.exports = function (passport) {
  // Сериализация пользователя
  passport.serializeUser((user, done) => {
    done(null, user.id);
  });

  // Десериализация пользователя
  passport.deserializeUser((id, done) => {
    db.get("SELECT * FROM users WHERE id = ?", [id], (err, user) => {
      if (err) {
        return done(err);
      }
      return done(null, user);
    });
  });

  // Google Strategy
  passport.use(
    new GoogleStrategy(
      {
        clientID: process.env.GOOGLE_CLIENT_ID,
        clientSecret: process.env.GOOGLE_CLIENT_SECRET,
        callbackURL: "/auth/google/callback", // Используем относительный путь
      },
      (accessToken, refreshToken, profile, done) => {
        const googleId = profile.id;
        const username = profile.displayName;

        // Проверяем, существует ли пользователь с данным Google ID
        db.get("SELECT * FROM users WHERE googleId = ?", [googleId], (err, user) => {
          if (err) {
            return done(err);
          }
          if (user) {
            return done(null, user);
          } else {
            // Создаем нового пользователя
            db.run(
              "INSERT INTO users (username, googleId) VALUES (?, ?)",
              [username, googleId],
              function (err) {
                if (err) {
                  return done(err);
                }
                // Получаем новосозданного пользователя из базы данных
                db.get("SELECT * FROM users WHERE id = ?", [this.lastID], (err, newUser) => {
                  if (err) {
                    return done(err);
                  }
                  return done(null, newUser);
                });
              },
            );
          }
        });
      },
    ),
  );
};
