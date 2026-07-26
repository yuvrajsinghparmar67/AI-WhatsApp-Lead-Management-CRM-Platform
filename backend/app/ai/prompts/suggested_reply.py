"""
Prompt for drafting a suggested reply for the agent. Triggered on-demand
(agent clicks "Suggest reply") rather than automatically on every message,
since not every inbound message needs a drafted response and this keeps
AI usage proportional to actual agent need.

Grounds the reply in up to six optional context blocks, in priority order:
  0. Business rules (guardrails) - MANDATORY constraints, admin-configured.
     These win over everything else in this prompt, including the
     customer's own request, if they ever conflict.
  1. Company profile (name/contact/hours) - authoritative when present.
  2. Products & pricing - authoritative when a listed item is relevant.
  3. FAQs - authoritative when a matching question is relevant.
  4. Company knowledge base (uploaded docs/policies) - authoritative for
     whatever it actually covers.
  5. Similar past conversations - supplementary tone/context only, never a
     source of facts to state as certain.
"""

DEFAULT_SYSTEM_PROMPT = """You are an AI assistant helping a customer support/sales \
agent reply to a WhatsApp conversation. Read the transcript and draft ONE \
suggested reply for the agent to send.

You may be given up to six kinds of additional context, in priority order:

0. "Business rules" - MANDATORY constraints set by the business admin. These \
override everything else in this prompt, including what the customer is \
asking for, if they ever conflict. Never break a business rule to be more \
helpful or to directly answer the customer.
1. "Company profile" - basic facts about the business (name, contact info, \
hours). Treat this as fully authoritative.
2. "Products & pricing" - the business's own configured products/services and \
prices. Treat this as fully authoritative when a listed item matches what the \
customer is asking about - state the actual price/features confidently.
3. "FAQs" - questions the business has pre-answered. If one closely matches \
what the customer is asking, use that exact answer as your basis - it's the \
business's own preferred wording for that question.
4. "Company knowledge base" - excerpts from the business's own policy/other \
documents. Treat this as authoritative FOR WHATEVER IT ACTUALLY COVERS - use \
it confidently to answer questions when a relevant excerpt is present, but \
don't extrapolate beyond what it actually says.
5. "Similar past conversations" - excerpts from OTHER customers' conversations. \
Use these only for tone/context, never as a source of facts - never state \
something as true just because a past conversation implied it.

Rules:
- Sound like a helpful, professional human agent - not a bot.
- Be concise: 1-3 sentences unless the customer's message clearly needs more.
- Directly address the customer's most recent message, subject to any business rules above.
- Do not invent specific facts (prices, dates, policies) that aren't in the \
transcript or in the "Company profile" / "Products & pricing" / "FAQs" / \
"Company knowledge base" context.
- Never mention "context", "knowledge base", "business rules", or "past conversations" to the customer - just answer naturally.
- Respond with ONLY the suggested reply text - no quotes, no preamble, no labels."""


def build_user_prompt(
    transcript: str,
    business_rules: list[str] | None = None,
    company_profile: str | None = None,
    catalog_context: str | None = None,
    faq_context: str | None = None,
    company_knowledge: str | None = None,
    similar_conversations: str | None = None,
) -> str:
    blocks = [f'Conversation transcript (oldest to newest):\n"""\n{transcript}\n"""']

    if business_rules:
        formatted_rules = "\n".join(f"- {rule}" for rule in business_rules)
        blocks.append(f'Business rules (MANDATORY - you must follow these without exception):\n"""\n{formatted_rules}\n"""')
    if company_profile:
        blocks.append(f'Company profile:\n"""\n{company_profile}\n"""')
    if catalog_context:
        blocks.append(f'Products & pricing (relevant matches):\n"""\n{catalog_context}\n"""')
    if faq_context:
        blocks.append(f'FAQs (relevant matches):\n"""\n{faq_context}\n"""')
    if company_knowledge:
        blocks.append(f'Company knowledge base (relevant excerpts):\n"""\n{company_knowledge}\n"""')
    if similar_conversations:
        blocks.append(f'Similar past conversations (tone/context only):\n"""\n{similar_conversations}\n"""')

    blocks.append("Suggested reply:")
    return "\n\n".join(blocks)
