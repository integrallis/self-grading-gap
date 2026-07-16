"""Unit tests for the message-content normalization shim."""

from vgap.pipeline.prompts import content_to_text


def test_string_identity():
    assert content_to_text("plain ```python\nx=1\n```") == "plain ```python\nx=1\n```"


def test_list_of_dict_blocks():
    blocks = [{"type": "reasoning", "text": "thinking..."}, {"type": "text", "text": "```python\nx=1\n```"}]
    assert content_to_text(blocks) == "thinking...```python\nx=1\n```"


def test_list_of_strings():
    assert content_to_text(["a", "b"]) == "ab"


def test_dict_block_without_text_key():
    assert content_to_text([{"type": "tool_use"}]) == ""


def test_non_string_fallback():
    assert content_to_text(42) == "42"
