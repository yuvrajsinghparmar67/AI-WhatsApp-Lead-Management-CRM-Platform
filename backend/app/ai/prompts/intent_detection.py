"""
Prompt template for intent detection.

Kept as plain, reviewable strings separate from any API route or service -
so the prompt can be iterated on (and diffed in code review) without
touching business logic. Real intent-detection/lead-qualification/etc.
services land in a later milestone; this file exists now to establish the
pattern every future prompt will follow.
"""

DEFAULT_SYSTEM_PROMPT = """You are an AI assistant embedded in a business's customer \
messaging platform. Your job is to read an incoming customer message and \
classify its intent so the CRM can route and prioritize it correctly.

Respond with a single word from this list only: \
sales_inquiry, support_request, complaint, general_question, spam."""


def build_user_prompt(message_text: str) -> str:
    return f"Customer message:\n\"\"\"\n{message_text}\n\"\"\"\n\nIntent:"
