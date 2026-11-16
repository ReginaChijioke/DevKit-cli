
import os
import unittest
import requests
from unittest.mock import patch, Mock

from devkit.ai_client import get_api_key, generate_readme


class TestGetApiKey(unittest.TestCase):

    def test_returns_api_key_when_configured(self):
        with patch.dict(os.environ, {"GROQ_API_KEY": "test-key-123"}):
            result = get_api_key()

        self.assertEqual(result, "test-key-123")

    def test_prompts_user_when_environment_key_is_missing(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch(
                "devkit.ai_client.getpass.getpass",
                return_value="user-entered-key"
            ):
                result = get_api_key()

        self.assertEqual(result, "user-entered-key")

    def test_returns_none_when_user_enters_nothing(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch(
                "devkit.ai_client.getpass.getpass",
                return_value=""
            ):
                result = get_api_key()

        self.assertIsNone(result)

    def test_returns_none_when_user_enters_only_whitespace(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch(
                "devkit.ai_client.getpass.getpass",
                return_value="   "
            ):
                result = get_api_key()

        self.assertIsNone(result)


class TestGenerateReadme(unittest.TestCase):

    def test_returns_readme_content_when_request_succeeds(self):
        mock_response = Mock()

        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "# Test Project\n\nA sample project."
                    }
                }
            ]
        }

        project_info = {"project_name": "Test Project"}

        with patch(
            "devkit.ai_client.requests.post",
            return_value=mock_response
        ):
            result = generate_readme("test-api-key", project_info)

        self.assertEqual(
            result,
            "# Test Project\n\nA sample project."
        )

    def test_returns_none_when_request_fails(self):
        with patch(
            "devkit.ai_client.requests.post",
            side_effect=requests.exceptions.ConnectionError("Connection failed")
        ):
            with patch("builtins.print"):
                result = generate_readme(
                    "test-api-key",
                    {"project_name": "Test Project"}
                )

        self.assertIsNone(result)

    def test_returns_none_when_choices_is_missing(self):
        mock_response = Mock()
        mock_response.json.return_value = {
            "error": "Unexpected response"
        }

        with patch(
            "devkit.ai_client.requests.post",
            return_value=mock_response
        ):
            with patch("builtins.print"):
                result = generate_readme(
                    "test-api-key",
                    {"project_name": "Test Project"}
                )

        self.assertIsNone(result)

    def test_returns_none_when_choices_list_is_empty(self):
        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": []
        }

        with patch(
            "devkit.ai_client.requests.post",
            return_value=mock_response
        ):
            with patch("builtins.print"):
                result = generate_readme(
                    "test-api-key",
                    {"project_name": "Test Project"}
                )

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
