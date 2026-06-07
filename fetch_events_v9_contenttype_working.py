import pandas as pd
from datetime import datetime
import os

from sources.indiaai_source import get_indiaai_events
from sources.meity_source import get_meity_events
from sources.google_source import get_google_events
from sources.nasscom_source import get_nasscom_events
from sources.devpost_source import get_devpost_events
from sources.microsoft_source import get_microsoft_events
from sources.nvidia_source import get_nvidia_events
from sources.openai_source import get_openai_events
from sources.aws_source import get_aws_events
from sources.internet_radar_source import get_internet_radar_events
from sources.jobs_radar_source import get_jobs_radar_events
from sources.ai_sources_hub import get_ai_sources_hub_events
from release_notes_source import get_release_notes_events
from ai_news_radar_source import get_ai_news_radar_events

from event_quality import (
    is_valid_event,
    remove_duplicate_events
)

os.makedirs("archive", exist_ok=True)

def classify_content_type(event):

    event_name = str(event.get("Event", "")).lower()
    event_type = str(event.get("Type", "")).lower()
    source = str(event.get("Source", "")).lower()
    register = str(event.get("Register", "")).lower()

    text = f"{event_name} {event_type} {source} {register}"

    if any(word in text for word in ["job", "jobs", "career", "careers", "naukri", "linkedin", "indeed", "foundit", "wellfound"]):
        return "Job"

    if any(word in text for word in ["release notes", "changelog", "releases", "release note"]):
        return "ReleaseNote"

    if any(word in text for word in ["news", "blog", "announcement", "announcements", "updates"]):
        return "News"

    if any(word in text for word in ["course", "training", "learning", "bootcamp", "certification", "certificate", "youtube", "krish naik", "campusx", "codebasics", "deeplearning"]):
        return "Learning"

    if any(word in text for word in ["tool", "tools", "github", "product hunt", "hugging face", "langchain", "crewai", "autogen", "llamaindex"]):
        return "Tool"

    if any(word in text for word in ["research", "paper", "papers", "papers with code", "arxiv"]):
        return "Research"

    if any(word in text for word in ["community", "forum", "social", "linkedin", "instagram"]):
        return "Community"

    if any(word in text for word in ["event", "events", "workshop", "webinar", "conference", "summit", "hackathon", "challenge"]):
        return "Event"

    return "Other"

SOURCE_FUNCTIONS = [
    ("IndiaAI", get_indiaai_events),
    ("MeitY", get_meity_events),
    ("Google", get_google_events),
    ("NASSCOM", get_nasscom_events),
    ("Devpost", get_devpost_events),
    ("Microsoft", get_microsoft_events),
    ("NVIDIA", get_nvidia_events),
    ("OpenAI", get_openai_events),
    ("AWS", get_aws_events),
    ("Internet Radar", get_internet_radar_events),
    ("AI Jobs Radar", get_jobs_radar_events),
    ("AI Sources Hub", get_ai_sources_hub_events),
    ("AI Release Notes Radar", get_release_notes_events),
    ("AI News Radar", get_ai_news_radar_events),
]

previous_events = pd.DataFrame()

if os.path.exists("events.csv"):
    previous_events = pd.read_csv("events.csv")

if os.path.exists("events.csv"):

    current_df = pd.read_csv("events.csv")

    if os.path.exists("archive/old_events.csv"):
        old_df = pd.read_csv("archive/old_events.csv")
        combined = pd.concat([old_df, current_df], ignore_index=True)

        combined.drop_duplicates(
            subset=["Event"],
            inplace=True
        )

        combined.to_csv("archive/old_events.csv", index=False)

    else:
        current_df.to_csv("archive/old_events.csv", index=False)

events = []
source_status_rows = []

current_time = datetime.now().strftime("%d-%b-%Y %H:%M:%S")

for source_name, source_function in SOURCE_FUNCTIONS:

    try:
        source_events = source_function()

        if source_events is None:
            source_events = []

        for event in source_events:
            event["LastUpdated"] = current_time
            event["ContentType"] = classify_content_type(event)

        events.extend(source_events)

        status = "Healthy" if len(source_events) > 0 else "Warning"

        source_status_rows.append(
            {
                "Source": source_name,
                "Events Count": len(source_events),
                "Status": status,
                "Last Checked": current_time,
                "Message": "Source returned events successfully"
            }
        )

    except Exception as e:

        source_status_rows.append(
            {
                "Source": source_name,
                "Events Count": 0,
                "Status": "Failed",
                "Last Checked": current_time,
                "Message": str(e)
            }
        )

source_status_df = pd.DataFrame(source_status_rows)
source_status_df.to_csv("source_status.csv", index=False)

filtered_events = []

for event in events:

    if is_valid_event(
        event.get("Event", "")
    ):
        filtered_events.append(event)

filtered_events = remove_duplicate_events(
    filtered_events
)

df = pd.DataFrame(filtered_events)

if df.empty:
    df = pd.DataFrame(
        columns=[
            "Event", "Type", "Mode", "Date", "Fee",
            "Priority", "Source", "Register", "LastUpdated"
        ]
    )

required_columns = [
    "Event", "Type", "Mode", "Date", "Fee",
    "Priority", "Source", "Register", "LastUpdated"
]

for column in required_columns:
    if column not in df.columns:
        df[column] = ""

df.drop_duplicates(
    subset=["Event"],
    inplace=True
)

active_events = []
completed_events = []

today = datetime.now()

for _, row in df.iterrows():

    try:
        event_date = datetime.strptime(
            str(row["Date"]),
            "%d-%b-%Y"
        )

        if event_date.date() >= today.date():
            active_events.append(row)
        else:
            completed_events.append(row)

    except Exception:
        active_events.append(row)

df = pd.DataFrame(active_events)

if len(completed_events) > 0:

    completed_df = pd.DataFrame(completed_events)
    archive_file = "archive/completed_events.csv"

    if os.path.exists(archive_file):

        old_completed = pd.read_csv(archive_file)

        completed_df = pd.concat(
            [old_completed, completed_df],
            ignore_index=True
        )

        completed_df.drop_duplicates(
            subset=["Event"],
            inplace=True
        )

    completed_df.to_csv(archive_file, index=False)

new_events = pd.DataFrame()

if not previous_events.empty and "Event" in previous_events.columns:

    previous_event_names = set(
        previous_events["Event"].astype(str).tolist()
    )

    new_events = df[
        ~df["Event"].astype(str).isin(previous_event_names)
    ]

else:
    new_events = df.copy()

new_events.to_csv("new_events.csv", index=False)

df.to_csv("events.csv", index=False)

print("\nAI Events Radar Refresh Completed")
print(f"Current Active Events : {len(df)}")

if os.path.exists("archive/old_events.csv"):
    archive_df = pd.read_csv("archive/old_events.csv")
    print(f"Old Archived Events : {len(archive_df)}")
else:
    print("Old Archived Events : 0")

if os.path.exists("archive/completed_events.csv"):
    completed_archive_df = pd.read_csv("archive/completed_events.csv")
    print(f"Completed Events Archived : {len(completed_archive_df)}")
else:
    print("Completed Events Archived : 0")

if os.path.exists("new_events.csv"):
    new_events_df = pd.read_csv("new_events.csv")
    print(f"New Events Detected : {len(new_events_df)}")
else:
    print("New Events Detected : 0")

print(f"Source Status Logged : {len(source_status_df)} sources")
print(f"Quality Filter Applied : {len(events)} raw events -> {len(df)} clean active events")
print(f"Refresh Time : {datetime.now()}")