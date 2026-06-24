"""Test utils module."""

from utils.storage import validate_inputs, clean_response


def test_validate_inputs_valid():
    assert validate_inputs("Hindi Film", "test", "Grief", "18-25", "Film", 5, "situation", "someone", "", 150)


def test_validate_inputs_empty_situation():
    assert not validate_inputs("Hindi Film", "test", "Grief", "18-25", "Film", 5, "", "someone", "", 150)


def test_validate_inputs_empty_spoken_to():
    assert not validate_inputs("Hindi Film", "test", "Grief", "18-25", "Film", 5, "situation", "", "", 150)


def test_validate_inputs_invalid_word_count():
    assert not validate_inputs("Hindi Film", "test", "Grief", "18-25", "Film", 5, "situation", "someone", "", -1)


def test_validate_inputs_unsupported_language():
    assert not validate_inputs("French", "test", "Grief", "18-25", "Film", 5, "situation", "someone", "", 150)


def test_clean_response_with_markdown():
    result = clean_response('```json\n{"key": "value"}\n```')
    assert "```" not in result
    assert '{"key": "value"}' in result


def test_clean_response_with_duplicate_headings():
    result = clean_response("# Heading\nSome text\n# Heading\nMore text")
    assert result.count("# Heading") == 1


def test_clean_response_with_extra_spacing():
    result = clean_response("Text   with   spaces\n\n\n\nMore text")
    assert "   " not in result
    assert "\n\n\n" not in result


def test_clean_response_empty():
    assert clean_response("") == ""
    assert clean_response(None) == ""
