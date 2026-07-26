"""
Resolves "what system prompt actually runs right now" for each of the
pipeline's editable prompts, and lets admins override or reset them.

This is the ONLY place that decides between an admin's custom_text and the
code-defined default - ai_pipeline_service always calls
get_effective_prompt() rather than importing a prompt module's
DEFAULT_SYSTEM_PROMPT directly, so an admin edit takes effect immediately
without a redeploy.
"""
import uuid
from typing import Optional

from sqlalchemy.orm import Session

from app.ai.prompts import conversation_analysis, suggested_reply
from app.models.prompt_template import PromptTemplate

# (label, default text, admin-facing warning) for every editable prompt.
PROMPT_REGISTRY = {
    "conversation_analysis": {
        "label": "Conversation Analysis",
        "default_text": conversation_analysis.DEFAULT_SYSTEM_PROMPT,
        "warning": (
            "This prompt drives automatic lead scoring and MUST still instruct the model "
            "to respond with only a JSON object in the documented shape - editing away that "
            "instruction will silently stop lead status/priority/sentiment from updating "
            "(the pipeline fails soft, so it won't crash, it will just stop working)."
        ),
    },
    "suggested_reply": {
        "label": "Suggested Reply",
        "default_text": suggested_reply.DEFAULT_SYSTEM_PROMPT,
        "warning": None,
    },
}


def _get_template_row(db: Session, key: str) -> Optional[PromptTemplate]:
    return db.query(PromptTemplate).filter(PromptTemplate.key == key).first()


def get_effective_prompt(db: Session, key: str) -> str:
    """What actually gets sent to Gemini for this prompt right now."""
    row = _get_template_row(db, key)
    if row and row.custom_text and row.custom_text.strip():
        return row.custom_text
    return PROMPT_REGISTRY[key]["default_text"]


def list_prompts(db: Session) -> list[dict]:
    results = []
    for key, meta in PROMPT_REGISTRY.items():
        row = _get_template_row(db, key)
        is_custom = bool(row and row.custom_text and row.custom_text.strip())
        results.append(
            {
                "key": key,
                "label": meta["label"],
                "default_text": meta["default_text"],
                "custom_text": row.custom_text if row else None,
                "effective_text": row.custom_text if is_custom else meta["default_text"],
                "is_custom": is_custom,
                "updated_at": row.updated_at if row else None,
            }
        )
    return results


def update_prompt(db: Session, key: str, custom_text: Optional[str]) -> dict:
    if key not in PROMPT_REGISTRY:
        raise ValueError(f"Unknown prompt key: {key}")

    row = _get_template_row(db, key)
    if not row:
        row = PromptTemplate(id=uuid.uuid4(), key=key)
        db.add(row)

    # Empty/whitespace-only text resets to the code default rather than
    # storing an empty override.
    row.custom_text = custom_text.strip() if custom_text and custom_text.strip() else None

    db.commit()
    db.refresh(row)

    meta = PROMPT_REGISTRY[key]
    is_custom = bool(row.custom_text)
    return {
        "key": key,
        "label": meta["label"],
        "default_text": meta["default_text"],
        "custom_text": row.custom_text,
        "effective_text": row.custom_text if is_custom else meta["default_text"],
        "is_custom": is_custom,
        "updated_at": row.updated_at,
    }
