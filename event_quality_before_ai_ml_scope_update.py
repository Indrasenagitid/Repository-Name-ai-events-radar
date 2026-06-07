import re


def normalize_event_name(text):

    text = str(text).lower().strip()

    prefixes = [
        "ai sources hub:",
        "internet radar:",
        "ai news radar:",
        "social radar:",
        "ai jobs radar:",
        "aws event:",
        "google event:",
        "microsoft event:",
        "nvidia event:",
        "openai update/event:",
        "indiaai event:",
        "meity update/event:",
        "nasscom event:",
        "devpost hackathon:"
    ]

    for prefix in prefixes:
        text = text.replace(prefix, "")

    text = re.sub(r"[^a-z0-9 ]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def is_valid_event(title):

    if not title:
        return False

    title = str(title).strip().lower()

    blocked_words = [
        "skip to main content",
        "home",
        "about",
        "about us",
        "contact",
        "contact us",
        "privacy",
        "privacy policy",
        "terms",
        "terms of use",
        "cookie",
        "login",
        "sign in",
        "sign up",
        "portal",
        "menu",
        "navigation",
        "search",
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
        "certification",
        "job",
        "jobs",
        "career",
        "careers",
        "engineer",
        "product manager",
        "prompt engineer",
        "automation engineer",
        "langchain",
        "langgraph",
        "crewai",
        "autogen",
        "hugging face",
        "anthropic",
        "claude",
        "release",
        "release notes",
        "model",
        "tool",
        "research"
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

        name = normalize_event_name(
            event.get("Event", "")
        )

        if name and name not in seen:

            seen.add(name)
            clean_events.append(event)

    return clean_events