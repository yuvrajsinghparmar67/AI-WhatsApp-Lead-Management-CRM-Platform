"""
Small helpers shared across the AI layer - currently just tolerant JSON
parsing, since models occasionally wrap JSON in markdown code fences
despite being told not to.
"""
import json
from typing import Any


def parse_json_response(raw_text: str) -> Any:
    text = raw_text.strip()

    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:]
        text = text.strip()

    return json.loads(text)
