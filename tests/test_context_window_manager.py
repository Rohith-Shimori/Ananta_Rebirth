
import unittest
import sys
import os

# Add repo root to path so we can import core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.context_window_manager import ContextWindowManager

class TestContextWindowManager(unittest.TestCase):
    def setUp(self):
        self.manager = ContextWindowManager()

    def test_compress_context_empty(self):
        compressed, ratio = self.manager.compress_context("", "model")
        self.assertEqual(compressed, "")
        self.assertEqual(ratio, 1.0)

    def test_compress_context_identity(self):
        context = "This is a simple context."
        # If we ask for 1.0 ratio, it should be approximately same (ignoring whitespace normalization if any)
        # The implementation joins with \n, so if original didn't have \n but was single line, it's fine.
        compressed, ratio = self.manager.compress_context(context, "model", target_ratio=1.0)
        self.assertEqual(compressed.strip(), context.strip())
        self.assertAlmostEqual(ratio, 1.0, delta=0.1)

    def test_compress_context_preserves_important(self):
        context = (
            "This is filler.\n"
            "Important: This must be kept.\n"
            "More filler.\n"
            "Note: This is also critical.\n"
            "Just noise.\n"
        )

        # Target ratio that allows preserving important lines but drops some filler
        # Total lines: 5. Important: 2. Filler: 3.
        # Target ratio 0.5 -> 50% tokens.

        compressed, ratio = self.manager.compress_context(context, "model", target_ratio=0.5)

        self.assertIn("Important: This must be kept.", compressed)
        self.assertIn("Note: This is also critical.", compressed)

        # Check that ratio calculation is reasonable
        self.assertTrue(0.0 < ratio <= 1.0)

    def test_compress_context_sampling(self):
        # Create a context with many non-important lines
        lines = [f"Line {i} content" for i in range(100)]
        context = "\n".join(lines)

        # Compress to 50%
        compressed, ratio = self.manager.compress_context(context, "model", target_ratio=0.5)

        compressed_lines = compressed.split('\n')

        # Should have kept approximately half
        self.assertTrue(40 <= len(compressed_lines) <= 60, f"Expected ~50 lines, got {len(compressed_lines)}")

        # Should be the first ones (as per current logic which takes head of list)
        self.assertIn("Line 0 content", compressed)
        self.assertIn("Line 40 content", compressed)

        # Verify result is a string
        self.assertIsInstance(compressed, str)
        self.assertIsInstance(ratio, float)

if __name__ == '__main__':
    unittest.main()
