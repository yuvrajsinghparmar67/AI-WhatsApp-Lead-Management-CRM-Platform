"""Unit tests for the tolerant JSON parsing used on AI provider responses."""
import pytest

from app.ai.utils import parse_json_response


def test_parses_plain_json():
    assert parse_json_response('{"a": 1}') == {"a": 1}


def test_parses_json_wrapped_in_labeled_code_fence():
    raw = '```json\n{"a": 1}\n```'
    assert parse_json_response(raw) == {"a": 1}


def test_parses_json_wrapped_in_bare_code_fence():
    raw = '```\n{"a": 1}\n```'
    assert parse_json_response(raw) == {"a": 1}


def test_invalid_json_raises():
    with pytest.raises(Exception):
        parse_json_response("not json at all")
