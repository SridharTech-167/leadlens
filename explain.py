"""
LeadLens explanation engine.

For each ranked lead, retrieves the structured + unstructured facts behind
its score ("retrieval") and asks an LLM to turn them into a one- or two-
sentence, plain-English explanation ("generation") -- a lightweight RAG
pattern over CRM data.

Works in two modes:
  - LLM mode: set OPENAI_API_KEY (or GROQ_API_KEY, see call_llm()) to get
    real generated explanations.
  - Offline/demo mode: if no API key is set, falls back to a deterministic
    template so the app still runs end-to-end without any external calls.
"""

import os
from ranking import top_factors

FACTOR_PHRASES = {
    "deal size": "a large deal value (₹{deal_value:,})",
    "recent activity": "recent contact activity ({days} day(s) ago)",
    "engagement": "strong engagement (score {engagement}/100)",
}


def build_context(row) -> str:
    """Assemble the 'retrieved' facts for one lead into a short context
    block that gets passed to the LLM."""
    return (
        f"Lead: {row['name']} at {row['company']}\n"
        f"Source: {row['source']}\n"
        f"Status: {row['status']}\n"
        f"Deal value: Rs.{row['deal_value']:,}\n"
        f"Last contacted: {row['last_contact_days_ago']} day(s) ago\n"
        f"Engagement score: {row['engagement_score']}/100\n"
        f"Notes: {row['notes']}\n"
    )


def template_explanation(row) -> str:
    """Deterministic fallback explanation -- no API key required."""
    factors = top_factors(row)
    phrases = []
    for f in factors:
        template = FACTOR_PHRASES[f]
        phrases.append(template.format(
            deal_value=row["deal_value"],
            days=row["last_contact_days_ago"],
            engagement=row["engagement_score"],
        ))
    joined = " and ".join(phrases)
    return f"Ranked high mainly due to {joined}. Note: \"{row['notes']}\""


def call_llm(context: str) -> str | None:
    """Attempts a real LLM call. Returns None if no API key is configured
    or the call fails, so the caller can fall back to the template."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a sales assistant. In one short sentence, "
                        "explain why this lead is a priority, using only "
                        "the facts given. Be concrete and specific."
                    ),
                },
                {"role": "user", "content": context},
            ],
            max_tokens=80,
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return None


def explain_lead(row) -> str:
    """Public entry point: try the LLM, fall back to the template."""
    context = build_context(row)
    llm_result = call_llm(context)
    return llm_result if llm_result else template_explanation(row)