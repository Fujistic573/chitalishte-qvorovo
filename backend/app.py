import os
import smtplib
from email.mime.text import MIMEText
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app) 

# --- EMAIL CONFIGURATION ---
# Тези променливи се четат от терминала
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

# --- ТОВА Е ЛИПСВАЩИЯТ РЕД, КОЙТО ТРЯБВА ДА ДОБАВИШ ---
RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL', EMAIL_ADDRESS)

# Проверка дали основните данни са зададени
if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
    print("ГРЕШКА: Данните за имейл (EMAIL_ADDRESS, EMAIL_PASSWORD) не са зададени като променливи на средата.")

@app.route('/send-email', methods=['POST'])
def send_email():
    if not RECIPIENT_EMAIL:
        return jsonify({
            "status": "error",
            "message": "Сървърът не е конфигуриран с имейл на получател."
        }), 500

    try:
        # Вземи данните от формата
        name = request.form['name']
        visitor_email = request.form['email']
        message = request.form['message']

        # Създай съдържанието на имейла
        subject = f"Ново съобщение от сайта от {name}"
        body = f"""
        Име: {name}
        Имейл: {visitor_email}
        
        Съобщение:
        {message}
        """

        msg = MIMEText(body, 'plain', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = f"Сайт на с. Яворово <{EMAIL_ADDRESS}>"
        msg['To'] = RECIPIENT_EMAIL
        msg['Reply-To'] = visitor_email

        # Изпрати имейла
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(EMAIL_ADDRESS, EMAIL_PASSWORD
)
            smtp_server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())

        return jsonify({
            "status": "success",
            "message": "Съобщението е изпратено успешно!"
        })

    except Exception as e:
        print(f"Възникна грешка: {e}") # Отпечатва грешката в терминала за дебъгване
        return jsonify({
            "status": "error",
            "message": "Възникна грешка при изпращането на съобщението."
        }), 500

if __name__ == '__main__':
    app.run(debug=True)