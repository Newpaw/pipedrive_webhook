import unittest
from unittest.mock import patch
from app import app

class BasicTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'ok')

    @patch('app.webhook')
    def test_webhook_correct_url(self, mock_process_data):
        mock_process_data.return_value = None
        app.config['WEBHOOK_URL'] = 'test_webhook'  # přidáno nastavení proměnné
        response = self.app.post('/test_webhook', json={"key": "value"})
        self.assertEqual(response.status_code, 200)
        mock_process_data.assert_called_once_with({"key": "value"})


    def test_webhook_incorrect_url(self):
        response = self.app.post('/incorrect_url', json={"key": "value"})
        self.assertEqual(response.status_code, 404)

    def test_webhook_bad_request(self):
        response = self.app.post('/test_webhook')
        self.assertEqual(response.status_code, 400)
