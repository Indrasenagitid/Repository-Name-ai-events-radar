import pandas as pd
import os

if not os.path.exists("events.csv"):
    print("events.csv not found")
    exit()

df = pd.read_csv("events.csv")

generic_words = [
    "home",
    "portal",
    "official portal",
    "updates",
    "blog",
    "news",
    "events portal"
]

generic_domains = [
    "https://openai.com",
    "https://www.anthropic.com",
    "https://www.linkedin.com/",
    "https://www.instagram.com/",
    "https://www.youtube.com/",
    "https://nasscom.in",
    "https://indiaai.gov.in",
    "https://www.meity.gov.in",
    "https://www.digitalindia.gov.in",
]

issues = []

for _, row in df.iterrows():

    event = str(row.get("Event", ""))
    source = str(row.get("Source", ""))
    register = str(row.get("Register", ""))

    issue = ""

    if register.strip() in generic_domains:
        issue = "Generic home page URL"

    elif register.count("/") <= 3:
        issue = "Likely generic domain"

    elif "search" not in register.lower() and any(word in event.lower() for word in ["jobs", "course", "certification"]):
        issue = "May need search-specific URL"

    if issue:
        issues.append({
            "Event": event,
            "Source": source,
            "Register": register,
            "Issue": issue
        })

if len(issues) == 0:
    print("No major URL quality issues found.")
else:
    report = pd.DataFrame(issues)
    report.to_csv("url_quality_report.csv", index=False)

    print("URL quality issues found:")
    print(report)
    print("\nReport created: url_quality_report.csv")