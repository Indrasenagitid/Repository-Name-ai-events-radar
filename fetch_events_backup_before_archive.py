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

# Backup existing events file into archive
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

# Save current events
df = pd.DataFrame(events)

df.drop_duplicates(
    subset=["Event"],
    inplace=True
)

df.to_csv(
    "events.csv",
    index=False
)

print("\nAI Events Radar Refresh Completed")
print(f"Current Events : {len(df)}")

if os.path.exists("archive/old_events.csv"):
    archive_df = pd.read_csv("archive/old_events.csv")
    print(f"Archived Events : {len(archive_df)}")
else:
    print("Archived Events : 0")

print(f"Refresh Time : {datetime.now()}")