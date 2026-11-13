
import os
import unittest
from unittest.mock import patch

from devkit.ai_client import get_api_key


class TestGetApiKey(unittest.TestCase):

    def test_returns_api_key_when_configured(self):
        with patch.dict(os.environ, {"GROQ_API_KEY": "test-key-123"}):
            result = get_api_key()

        self.assertEqual(result, "test-key-123")

    def test_returns_none_when_api_key_is_missing(self):
        with patch.dict(os.environ, {}, clear=True):
            result = get_api_key()

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
