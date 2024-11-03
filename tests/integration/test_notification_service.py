# tests/integration/test_notification_service.py

import unittest
import requests

class TestNotificationService(unittest.TestCase):
    BASE_URL = 'http://localhost:5003/notify'

    def test_send_email_notification(self):
        response = requests.post(self.BASE_URL, json={
            'type': 'email',
            'recipient': 'test@example.com',
            'message': 'Test email notification'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('status', data)

    def test_send_sms_notification(self):
        response = requests.post(self.BASE_URL, json={
            'type': 'sms',
            'recipient': '+1234567890',
            'message': 'Test SMS notification'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('status', data)

if __name__ == '__main__':
    unittest.main()
