from application import application
from testMessages import *
import unittest


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.app = application.test_client()

    def testIndex(self):
        response = self.app.get('/')
        assert response.status_code == 200

    def test_post(self):
        result = self.app.post('/', data=valid_message)
        assert result.status_code == 200
        assert "Email sent successfully!" in result.data

    def test_send_email_error(self):
        result = self.app.post('/', data=message_with_empty_to_email)
        assert "invalid recipient email" in result.data

        result = self.app.post('/', data=message_with_invalid_to_email)
        assert "invalid recipient email" in result.data

        result = self.app.post('/', data=message_with_empty_from_email)
        assert "invalid sender email" in result.data

        result = self.app.post('/', data=message_with_invalid_from_email)
        assert "invalid sender email" in result.data

        result = self.app.post('/', data=message_with_empty_subject)
        assert "subject cannot be empty" in result.data

        result = self.app.post('/', data=message_with_empty_content)
        assert "content cannot be empty" in result.data


if __name__ == '__main__':
    unittest.main()