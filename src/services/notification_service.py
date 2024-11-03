# services/notification_service.py

import smtplib
from flask import Flask, jsonify, request
from twilio.rest import Client

app = Flask(__name__)

class NotificationService:
    def __init__(self, email_config, sms_config):
        self.email_config = email_config
        self.sms_config = sms_config

    def send_email(self, to_email, subject, message):
        """Send an email notification."""
        with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
            server.starttls()
            server.login(self.email_config['username'], self.email_config['password'])
            email_message = f"Subject: {subject}\n\n{message}"
            server.sendmail(self.email_config['from_email'], to_email, email_message)

    def send_sms(self, to_phone, message):
        """Send an SMS notification."""
        client = Client(self.sms_config['account_sid'], self.sms_config['auth_token'])
        client.messages.create(
            body=message,
            from_=self.sms_config['from_phone'],
            to=to_phone
        )

notification_service = NotificationService(
    email_config={
        'smtp_server': 'smtp.example.com',
        'smtp_port': 587,
        'username': 'your_email@example.com',
        'password': 'your_password',
        'from_email': 'your_email@example.com'
    },
    sms_config={
        'account_sid': 'your_twilio_account_sid',
        'auth_token': 'your_twilio_auth_token',
        'from_phone': '+1234567890'
    }
)

@app.route('/notify', methods=['POST'])
def notify():
    """API endpoint to send notifications."""
    data = request.json
    notification_type = data.get('type')
    recipient = data.get('recipient')
    message = data.get('message')

    try:
        if notification_type == 'email':
            notification_service.send_email(recipient, "Transaction Notification", message)
        elif notification_type == 'sms':
            notification_service.send_sms(recipient, message)
        else:
            return jsonify({'error': 'Invalid notification type'}), 400

        return jsonify({'status': ' Notification sent successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(port=5003)
