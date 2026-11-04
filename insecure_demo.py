import hashlib
import os
import secrets
import sqlite3
import subprocess
from typing import Any, Tuple
import requests
import yaml

DB_PASSWORD: str = os.environ["DB_PASSWORD"]


def get_user(username: str) -> list[Any]:
    """Получение пользователя из БД с использованием параметризованного запроса."""
    conn = sqlite3.connect("app.db")
    try:
        return conn.execute(
            "SELECT * FROM users WHERE name = ?", (username,)
        ).fetchall()
    finally:
        conn.close()


def ping(host: str) -> subprocess.CompletedProcess[bytes]:
    """Безопасный вызов ping без shell и с передачей аргументов списком."""
    return subprocess.run(["ping", "-c", "1", host], check=False)


def hash_password(password: str, salt: bytes | None = None) -> Tuple[bytes, bytes]:
    """Хэширование пароля с использованием scrypt."""
    salt = salt or os.urandom(16)
    digest = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)
    return salt, digest


def make_reset_token() -> str:
    """Генерация криптостойкого токена для сброса."""
    return secrets.token_urlsafe(32)


def load_config(text: str) -> Any:
    """Безопасная загрузка конфигурации YAML."""
    return yaml.safe_load(text)


def fetch(url: str) -> requests.Response:
    """Запрос по URL с установленным таймаутом."""
    return requests.get(url, timeout=10)