import pandas as pd
import re
import os

def normalize_text(text):
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

if not os.path.exists("events.csv"):
    print("events.csv not found")
    exit()

df = pd.read_csv("events.csv")

df["NormalizedEvent"] = df["Event"].apply(normalize_text)

duplicates = df[df.duplicated(subset=["NormalizedEvent"], keep=False)]

if duplicates.empty:
    print("No duplicate or repeated events found.")
else:
    print("Duplicate / repeated events found:")
    print(duplicates[["Event", "Source", "Register"]])

    duplicates.to_csv("duplicate_events_report.csv", index=False)
    print("\nReport created: duplicate_events_report.csv")