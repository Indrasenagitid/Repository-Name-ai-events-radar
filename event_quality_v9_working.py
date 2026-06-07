import re


def normalize_event_name(text):

    text = str(text).lower().strip()

    prefixes = [
        "ai sources hub:",
        "internet radar:",
        "ai news radar:",
        "social radar:",
        "ai jobs radar:",
        "ai release notes radar:",
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

    scope_keywords = [
        "ai",
        "artificial intelligence",
        "generative ai",
        "genai",
        "agentic",
        "agents",
        "llm",
        "large language model",
        "gpt",
        "chatgpt",
        "openai",
        "claude",
        "anthropic",
        "gemini",
        "copilot",
        "machine learning",
        "ml",
        "deep learning",
        "data science",
        "data scientist",
        "mlops",
        "modelops",
        "data engineering",
        "analytics",
        "business intelligence",
        "computer vision",
        "nlp",
        "natural language processing",
        "neural",
        "automation",
        "ai automation",
        "prompt",
        "prompt engineering",
        "rag",
        "retrieval augmented generation",
        "vector",
        "vector database",
        "embedding",
        "embeddings",
        "nvidia",
        "aws ai",
        "azure ai",
        "google ai",
        "langchain",
        "langgraph",
        "crewai",
        "autogen",
        "llamaindex",
        "hugging face",
        "transformers",
        "model",
        "release",
        "release notes",
        "changelog",
        "tool",
        "tools",
        "research",
        "paper",
        "papers",
        "hackathon",
        "challenge",
        "workshop",
        "webinar",
        "summit",
        "conference",
        "certification",
        "certificate",
        "course",
        "bootcamp",
        "job",
        "jobs",
        "career",
        "careers",
        "engineer",
        "product manager",
        "prompt engineer",
        "automation engineer"
    ]

    if not any(keyword in title for keyword in scope_keywords):
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