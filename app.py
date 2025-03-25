import os
from flask import Flask, request, jsonify
import random
import smtplib
from email.mime.text import MIMEText
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Конфигурация SendGrid
SMTP_SERVER = "smtp.sendgrid.net"
SMTP_PORT = 587
SMTP_USERNAME = "apikey"  # Оставить без изменений
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')  # Безопасное хранение ключа
SENDER_EMAIL = "no-reply@example.com"  # Должен быть подтвержден в SendGrid

# Временные хранилища (в продакшене используйте БД)
users_db = {}
verification_codes = {}


def send_verification_email(email, code):
    """Функция отправки email с кодом подтверждения"""
    try:
        msg = MIMEText(f"Ваш код подтверждения: {code}")
        msg['Subject'] = 'Подтверждение регистрации'
        msg['From'] = SENDER_EMAIL
        msg['To'] = email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Шифрование соединения
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Ошибка отправки: {e}")
        return False


@app.route('/register', methods=['POST'])
def register():
    """Обработка регистрации"""
    data = request.json
    email = data.get('email', '').strip()
    password = data.get('password', '')

    # Валидация
    if not email or not password:
        return jsonify({"success": False, "message": "Заполните все поля"}), 400

    if '@' not in email or '.' not in email:
        return jsonify({"success": False, "message": "Некорректный email"}), 400

    if len(password) < 6:
        return jsonify({"success": False, "message": "Пароль слишком короткий"}), 400

    if email in users_db:
        return jsonify({"success": False, "message": "Email уже занят"}), 400

    # Генерация и отправка кода
    code = str(random.randint(100000, 999999))
    verification_codes[email] = {"code": code, "password": password}

    if not send_verification_email(email, code):
        return jsonify({"success": False, "message": "Ошибка отправки кода"}), 500

    return jsonify({"success": True, "message": "Код отправлен на email"})


@app.route('/verify', methods=['POST'])
def verify():
    """Подтверждение кода"""
    data = request.json
    email = data.get('email', '').strip()
    code = data.get('code', '')

    if not email or not code:
        return jsonify({"success": False, "message": "Введите код"}), 400

    if email not in verification_codes:
        return jsonify({"success": False, "message": "Сессия устарела"}), 400

    if verification_codes[email]["code"] != code:
        return jsonify({"success": False, "message": "Неверный код"}), 400

    # Регистрация пользователя
    users_db[email] = {"password": verification_codes[email]["password"]}
    del verification_codes[email]

    return jsonify({"success": True, "message": "Аккаунт активирован!"})


@app.route('/login', methods=['POST'])
def login():
    """Авторизация"""
    data = request.json
    email = data.get('email', '').strip()
    password = data.get('password', '')

    if email not in users_db or users_db[email]["password"] != password:
        return jsonify({"success": False, "message": "Неверные данные"}), 401

    return jsonify({"success": True, "message": "Добро пожаловать!"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))