import pandas as pd
from datetime import datetime

# Sample event data
# Later, we will replace this with real website data collection
events = [
    {
        "Event": "IndiaAI Government AI Program",
        "Type": "Government",
        "Mode": "Online",
        "Date": "10-Jul-2026",
        "Fee": "Free",
        "Register": "https://indiaai.gov.in"
    },
    {
        "Event": "MeitY Digital India AI Workshop",
        "Type": "Government",
        "Mode": "Online",
        "Date": "15-Jul-2026",
        "Fee": "Free",
        "Register": "https://www.meity.gov.in"
    },
    {
        "Event": "Google Developer AI Webinar",
        "Type": "Workshop",
        "Mode": "Online",
        "Date": "20-Jul-2026",
        "Fee": "Free",
        "Register": "https://developers.google.com/events"
    },
    {
        "Event": "NASSCOM FutureSkills AI Session",
        "Type": "Workshop",
        "Mode": "Online",
        "Date": "25-Jul-2026",
        "Fee": "Free",
        "Register": "https://futureskillsprime.in"
    },
    {
        "Event": "Global Agentic AI Hackathon",
        "Type": "Hackathon",
        "Mode": "Online",
        "Date": "30-Jul-2026",
        "Fee": "Free",
        "Register": "https://devpost.com"
    }
]

# Convert to DataFrame
df = pd.DataFrame(events)

# Save events to CSV
df.to_csv("events.csv", index=False)

print("AI Events Radar - Event collection completed successfully.")
print(f"Total events saved: {len(df)}")
print(f"Last updated: {datetime.now()}")