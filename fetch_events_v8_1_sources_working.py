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

# Make sure archive folder exists
os.makedirs("archive", exist_ok=True)

# Load previous events for new-event comparison
previous_events = pd.DataFrame()

if os.path.exists("events.csv"):
    previous_events = pd.read_csv("events.csv")

# Backup existing events file into old archive
if os.path.exists("events.csv"):

    current_df = pd.read_csv("events.csv")

    if os.path.exists("archive/old_events.csv"):
        old_df = pd.read_csv("archive/old_events.csv")

        combined = pd.concat(
            [old_df, current_df],
            ignore_index=True
        )

        combined.drop_duplicates(
            subset=["Event"],
            inplace=True
        )

        combined.to_csv(
            "archive/old_events.csv",
            index=False
        )

    else:
        current_df.to_csv(
            "archive/old_events.csv",
            index=False
        )

# Collect events from multiple sources
events = []

events.extend(get_indiaai_events())
events.extend(get_meity_events())
events.extend(get_google_events())
events.extend(get_nasscom_events())
events.extend(get_devpost_events())
events.extend(get_microsoft_events())
events.extend(get_nvidia_events())
events.extend(get_openai_events())
events.extend(get_aws_events())

# Add LastUpdated column
current_time = datetime.now().strftime("%d-%b-%Y %H:%M:%S")

for event in events:
    event["LastUpdated"] = current_time

# Convert events to DataFrame
df = pd.DataFrame(events)

df.drop_duplicates(
    subset=["Event"],
    inplace=True
)

# Auto archive completed events
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

    completed_df.to_csv(
        archive_file,
        index=False
    )

# Detect newly added active events
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

new_events.to_csv(
    "new_events.csv",
    index=False
)

# Save active current events
df.to_csv(
    "events.csv",
    index=False
)

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

print(f"Refresh Time : {datetime.now()}")