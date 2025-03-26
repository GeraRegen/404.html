import os
from flask import Flask, request, jsonify
import random
import smtplib
from email.mime.text import MIMEText
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)  # Разрешаем CORS для всех доменов

# Конфигурация SendGrid
SMTP_SERVER = "smtp.sendgrid.net"
SMTP_PORT = 587
SMTP_USERNAME = "apikey"
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')  # Ключ из переменных окружения
SENDER_EMAIL = "no-reply@example.com"  # Замените на реальный email

# Временное хранилище (в продакшене используйте БД)
users_db = {}
verification_codes = {}
sessions = {}

# Максимальное время жизни кода подтверждения (10 минут)
CODE_EXPIRATION = timedelta(minutes=10)

def send_verification_email(email, code):
    """Отправка email с кодом подтверждения"""
    try:
        msg = MIMEText(f"""
        Ваш код подтверждения: {code}
        Код действителен в течение 10 минут.
        """)
        msg['Subject'] = 'Подтверждение регистрации'
        msg['From'] = SENDER_EMAIL
        msg['To'] = email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        app.logger.error(f"Ошибка отправки email: {str(e)}")
        return False

@app.route('/register', methods=['POST'])
def register():
    """Обработка регистрации"""
    try:
        data = request.get_json()  # Явно парсим JSON
        if not data:
            return jsonify({"success": False, "message": "Неверный формат данных"}), 400

        email = data.get('email', '').strip().lower()
        password = data.get('password', '')

        # Валидация
        if not email or not password:
            return jsonify({"success": False, "message": "Заполните все поля"}), 400

        if '@' not in email or '.' not in email:
            return jsonify({"success": False, "message": "Некорректный email"}), 400

        if len(password) < 6:
            return jsonify({"success": False, "message": "Пароль должен содержать минимум 6 символов"}), 400

        if email in users_db:
            return jsonify({"success": False, "message": "Email уже зарегистрирован"}), 400

        # Генерация и сохранение кода
        code = str(random.randint(100000, 999999))
        verification_codes[email] = {
            "code": code,
            "password": password,
            "created_at": datetime.now()
        }

        # Отправка email
        if not send_verification_email(email, code):
            return jsonify({"success": False, "message": "Ошибка отправки кода подтверждения"}), 500

        return jsonify({
            "success": True,
            "message": "Код подтверждения отправлен на email",
            "email": email  # Возвращаем email для фронтенда
        })

    except Exception as e:
        app.logger.error(f"Ошибка регистрации: {str(e)}")
        return jsonify({"success": False, "message": "Внутренняя ошибка сервера"}), 500

@app.route('/verify', methods=['POST'])
def verify():
    """Подтверждение кода"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        code = data.get('code', '').strip()

        if not email or not code:
            return jsonify({"success": False, "message": "Введите email и код"}), 400

        # Проверка существования email и кода
        if email not in verification_codes:
            return jsonify({"success": False, "message": "Неверный email или код устарел"}), 400

        # Проверка срока действия кода
        code_data = verification_codes[email]
        if datetime.now() - code_data["created_at"] > CODE_EXPIRATION:
            del verification_codes[email]
            return jsonify({"success": False, "message": "Срок действия кода истёк"}), 400

        # Проверка кода
        if code != code_data["code"]:
            return jsonify({"success": False, "message": "Неверный код подтверждения"}), 400

        # Регистрация пользователя
        users_db[email] = {
            "password": code_data["password"],
            "verified": True,
            "registered_at": datetime.now()
        }
        del verification_codes[email]

        return jsonify({
            "success": True,
            "message": "Регистрация завершена!",
            "email": email
        })

    except Exception as e:
        app.logger.error(f"Ошибка верификации: {str(e)}")
        return jsonify({"success": False, "message": "Внутренняя ошибка сервера"}), 500

@app.route('/login', methods=['POST'])
def login():
    """Аутентификация пользователя"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')

        if not email or not password:
            return jsonify({"success": False, "message": "Введите email и пароль"}), 400

        if email not in users_db:
            return jsonify({"success": False, "message": "Пользователь не найден"}), 404

        if users_db[email]["password"] != password:
            return jsonify({"success": False, "message": "Неверный пароль"}), 401

        # Генерация сессии (в продакшене используйте JWT)
        session_token = os.urandom(24).hex()
        sessions[session_token] = {
            "email": email,
            "created_at": datetime.now()
        }

        return jsonify({
            "success": True,
            "message": "Вход выполнен успешно",
            "token": session_token,
            "email": email
        })

    except Exception as e:
        app.logger.error(f"Ошибка входа: {str(e)}")
        return jsonify({"success": False, "message": "Внутренняя ошибка сервера"}), 500

@app.route('/protected', methods=['GET'])
def protected():
    """Пример защищённого роута"""
    token = request.headers.get('Authorization')
    if not token or token not in sessions:
        return jsonify({"success": False, "message": "Не авторизован"}), 401
    
    return jsonify({
        "success": True,
        "message": "Добро пожаловать в защищённую зону",
        "user": sessions[token]["email"]
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
