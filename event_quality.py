def is_valid_event(title):

    if not title:
        return False

    title = str(title).strip().lower()

    blocked_words = [
        "home",
        "about",
        "contact",
        "privacy",
        "terms",
        "cookie",
        "login",
        "sign in",
        "sign up",
        "portal",
        "menu",
        "search",
        "careers",
        "jobs",
        "accessibility",
        "documentation",
        "subscribe",
        "newsletter",
        "press",
        "media",
        "help",
        "support"
    ]

    for word in blocked_words:
        if word in title:
            return False

    ai_keywords = [
        "ai",
        "artificial intelligence",
        "genai",
        "generative ai",
        "agentic",
        "agents",
        "llm",
        "gpt",
        "chatgpt",
        "openai",
        "gemini",
        "copilot",
        "machine learning",
        "deep learning",
        "data science",
        "neural",
        "automation",
        "prompt",
        "rag",
        "vector",
        "nvidia",
        "aws ai",
        "azure ai",
        "google ai",
        "hackathon",
        "challenge",
        "workshop",
        "webinar",
        "summit",
        "conference",
        "certification"
    ]

    if not any(keyword in title for keyword in ai_keywords):
        return False

    if len(title) < 10:
        return False

    return True


def remove_duplicate_events(events):

    seen = set()
    clean_events = []

    for event in events:

        name = str(
            event.get("Event", "")
        ).strip().lower()

        if name and name not in seen:

            seen.add(name)
            clean_events.append(event)

    return clean_events