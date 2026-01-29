import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Mock torch before importing core.ollama_client
sys.modules['torch'] = MagicMock()

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.ollama_client import OllamaClient

class TestOllamaSession(unittest.TestCase):
    def setUp(self):
        # Patch requests
        self.requests_patcher = patch('core.ollama_client.requests')
        self.mock_requests = self.requests_patcher.start()

        # Setup mock session
        self.mock_session = MagicMock()
        self.mock_requests.Session.return_value = self.mock_session

        # Setup mock response
        self.mock_response = MagicMock()
        self.mock_response.json.return_value = {"message": {"content": "Test response"}, "response": "Test response", "done": True}
        self.mock_response.iter_lines.return_value = [b'{"response": "Test chunk", "done": false}', b'{"done": true}']
        self.mock_session.post.return_value = self.mock_response
        self.mock_requests.post.return_value = self.mock_response

    def tearDown(self):
        self.requests_patcher.stop()

    def test_session_initialized(self):
        """Test that self.session is initialized"""
        client = OllamaClient()
        self.assertTrue(hasattr(client, 'session'), "OllamaClient should have a 'session' attribute")
        self.assertEqual(client.session, self.mock_session, "client.session should be the mock session")

    def test_chat_uses_session(self):
        """Test that chat uses the session.post"""
        client = OllamaClient()
        client.chat([{"role": "user", "content": "Hello"}])

        # Should call session.post, NOT requests.post
        self.mock_session.post.assert_called()
        self.mock_requests.post.assert_not_called()

    def test_generate_uses_session(self):
        """Test that generate uses the session.post"""
        client = OllamaClient()
        client.generate("Hello")

        self.mock_session.post.assert_called()
        self.mock_requests.post.assert_not_called()

if __name__ == '__main__':
    unittest.main()
