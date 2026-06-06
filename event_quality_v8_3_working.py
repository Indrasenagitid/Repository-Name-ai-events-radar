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
        "documentation"
    ]

    for word in blocked_words:
        if word in title:
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

        if name not in seen:

            seen.add(name)
            clean_events.append(event)

    return clean_events