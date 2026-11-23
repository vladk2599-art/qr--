import io
import socket
import qrcode
from flask import Flask, send_file, request

app = Flask(__name__)

STATUS_TEXT = "Проект находится на стадии разработки"


def get_local_ip() -> str:
    """Определяет локальный IP компьютера в Wi-Fi сети."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()


@app.route("/qr.png")
def qr_image():
    base = request.host_url.rstrip("/")
    target = f"{base}/status"
    img = qrcode.make(target)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")


@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>QR-код проекта</title>
        <style>
            body {
                display: flex; flex-direction: column;
                align-items: center; justify-content: center;
                min-height: 100vh; margin: 0;
                font-family: Arial, sans-serif; background: #f4f4f4;
            }
            h1 { color: #333; }
            img { background: white; padding: 20px; border-radius: 12px;
                  box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        </style>
    </head>
    <body>
        <h1>Отсканируйте QR-код</h1>
        <img src="/qr.png" width="280" height="280" alt="QR-код">
    </body>
    </html>
    """


@app.route("/status")
def status():
    return f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Статус проекта</title>
        <style>
            body {{
                display: flex; align-items: center; justify-content: center;
                min-height: 100vh; margin: 0; padding: 20px; box-sizing: border-box;
                font-family: Arial, sans-serif; text-align: center;
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
            }}
            h1 {{ font-size: 2rem; line-height: 1.4; }}
        </style>
    </head>
    <body>
        <h1>{STATUS_TEXT}</h1>
    </body>
    </html>
    """


if __name__ == "__main__":
    ip = get_local_ip()
    print("Сервер запущен.")
    print(f"Страница с QR:    http://{ip}:8000/")
    print(f"Страница статуса: http://{ip}:8000/status")
    app.run(host="0.0.0.0", port=8000)