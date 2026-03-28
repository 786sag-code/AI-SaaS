from app.core.config import settings


def generate_ai_suggestion(title: str, description: str) -> str:
    """
    Production note:
    Replace this with a real OpenAI client call if OPENAI_API_KEY is present.
    Keeping deterministic fallback text makes local development/test stable.
    """
    if settings.OPENAI_API_KEY:
        return (
            "AI suggestion generated using configured provider. "
            "Integrate OpenAI SDK call here for live completion."
        )

    summary = description[:180].replace("\n", " ").strip()
    return (
        f"Suggested first response for '{title}': "
        f"thank the customer, confirm the issue details ({summary}), "
        "and share an ETA for the next update within 2 hours."
    )
