# config.py

import os


class Config:
    SECRET_KEY = (
        os.environ.get("SECRET_KEY") or "your_very_secure_secret_key_for_development"
    )
    JWT_SECRET_KEY = (
        os.environ.get("JWT_SECRET_KEY") or "your_jwt_secret_key_for_development"
    )  # Замените на безопасный ключ
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # Токен истекает через 1 час
    CORS_HEADERS = "Content-Type"
