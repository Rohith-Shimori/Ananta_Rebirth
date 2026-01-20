
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Mock torch before importing core.ollama_client
sys.modules['torch'] = MagicMock()
sys.modules['torch'].cuda.is_available.return_value = False

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.ollama_client import OllamaClient
import core.ollama_client

class TestOllamaOptimization(unittest.TestCase):
    def setUp(self):
        # Mock requests.post and requests.Session
        self.post_patcher = patch('requests.post')
        self.session_patcher = patch('requests.Session')

        self.mock_post = self.post_patcher.start()
        self.mock_session_cls = self.session_patcher.start()

        # Setup mock session instance
        self.mock_session_instance = MagicMock()
        self.mock_session_cls.return_value = self.mock_session_instance

        # Setup responses
        mock_response = MagicMock()
        mock_response.json.return_value = {"response": "test response", "done": True, "message": {"content": "test chat"}}
        mock_response.iter_lines.return_value = [b'{"response": "chunk", "done": false}', b'{"response": "", "done": true}']

        self.mock_post.return_value = mock_response
        self.mock_session_instance.post.return_value = mock_response

    def tearDown(self):
        self.post_patcher.stop()
        self.session_patcher.stop()

    def test_connection_reuse(self):
        print("\nTesting Connection Reuse...")

        # Initialize client
        client = OllamaClient()

        # 1. Test generate (currently uses requests.post)
        print("Calling generate()...")
        client.generate("test prompt")

        # 2. Test chat (currently uses requests.post)
        print("Calling chat()...")
        client.chat([{"role": "user", "content": "hi"}])

        # 3. Test stream (currently creates NEW Session)
        print("Calling stream()...")
        list(client.stream("stream prompt"))

        # Check calls
        print(f"requests.post calls: {self.mock_post.call_count}")
        print(f"requests.Session() instantiations: {self.mock_session_cls.call_count}")
        print(f"session.post calls: {self.mock_session_instance.post.call_count}")

        # In unoptimized code:
        # requests.post should be called for generate and chat (at least 2 times)
        # requests.Session() should be called once for stream
        # session.post should be called once (inside stream)

        # In optimized code:
        # requests.post should be 0 (except if init does something)
        # requests.Session() should be 1 (in init)
        # session.post should be 3 (generate, chat, stream)

if __name__ == '__main__':
    unittest.main()
