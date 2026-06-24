import pytest
from unittest.mock import patch, MagicMock
import gemini_client


def test_generate_json_returns_parsed_dict():
    mock_response = MagicMock()
    mock_response.text = '{"key": "value"}'
    with patch("gemini_client.genai.Client") as MockClient:
        MockClient.return_value.models.generate_content.return_value = mock_response
        result = gemini_client.generate_json(
            api_key="fake-key",
            model="gemini-2.5-flash",
            temperature=1.0,
            system_instruction="You are a writer.",
            prompt="Write something"
        )
    assert result == {"key": "value"}


def test_generate_json_strips_markdown_fences():
    mock_response = MagicMock()
    mock_response.text = '```json\n{"key": "value"}\n```'
    with patch("gemini_client.genai.Client") as MockClient:
        MockClient.return_value.models.generate_content.return_value = mock_response
        result = gemini_client.generate_json(
            api_key="fake-key",
            model="gemini-2.5-flash",
            temperature=1.0,
            system_instruction="You are a writer.",
            prompt="Write something"
        )
    assert result == {"key": "value"}


def test_generate_json_returns_none_on_parse_error():
    mock_response = MagicMock()
    mock_response.text = "not valid json"
    with patch("gemini_client.genai.Client") as MockClient:
        MockClient.return_value.models.generate_content.return_value = mock_response
        result = gemini_client.generate_json(
            api_key="fake-key",
            model="gemini-2.5-flash",
            temperature=1.0,
            system_instruction="You are a writer.",
            prompt="Write something"
        )
    assert result is None


def test_generate_json_returns_none_on_non_429_error():
    with patch("gemini_client.genai.Client") as MockClient:
        MockClient.return_value.models.generate_content.side_effect = Exception("auth error")
        result = gemini_client.generate_json(
            api_key="fake-key",
            model="gemini-2.5-flash",
            temperature=1.0,
            system_instruction="You are a writer.",
            prompt="Write something"
        )
    assert result is None


def test_generate_json_retries_on_429():
    with patch("gemini_client.genai.Client") as MockClient:
        mock_client = MockClient.return_value
        mock_client.models.generate_content.side_effect = [
            Exception("429 quota exceeded"),
            MagicMock(text='{"ok": true}')
        ]
        with patch("gemini_client.time.sleep"):
            result = gemini_client.generate_json(
                api_key="fake-key",
                model="gemini-2.5-flash",
                temperature=1.0,
                system_instruction="You are a writer.",
                prompt="Write something",
                max_retries=3
            )
    assert result == {"ok": True}
    assert mock_client.models.generate_content.call_count == 2
