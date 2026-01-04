
import unittest
from unittest.mock import patch, MagicMock
from core.ollama_client import OllamaClient
import requests

class TestOllamaConnectionPooling(unittest.TestCase):
    def test_generate_uses_session_and_reuses_connection(self):
        client = OllamaClient()

        # We want to verify that client.session.post is called, not requests.post
        # And we want to see if the session object is reused (which it is by design if we use self.session)

        # Mock requests.post to ensure it's NOT called
        with patch('requests.post') as mock_requests_post:
             # Mock the session.post method on the instance
             client.session.post = MagicMock()

             mock_response = MagicMock()
             mock_response.iter_lines.return_value = [b'{"response": "test", "done": true}']
             mock_response.json.return_value = {"response": "test", "done": True}

             client.session.post.return_value = mock_response

             client.generate("test prompt")
             client.generate("test prompt 2")

             # requests.post should NOT be called
             self.assertEqual(mock_requests_post.call_count, 0)

             # client.session.post should be called 2 times
             self.assertEqual(client.session.post.call_count, 2)

             print("\nVerified: requests.Session.post called 2 times (session reuse confirmed)")
             print("Verified: requests.post NOT called")

if __name__ == '__main__':
    unittest.main()
