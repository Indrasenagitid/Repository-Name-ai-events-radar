import streamlit as st
import pandas as pd
import subprocess
import os
from datetime import datetime

st.set_page_config(
    page_title="AI Events Radar",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stApp { background-color: #F5F5F7; }
.block-container { padding-top: 1.2rem; padding-bottom: 1rem; }
h1 { font-size: 38px; font-weight: 800; color: #111111; }
.hero-card {
    background: white; padding: 22px 28px; border-radius: 24px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.05); margin-bottom: 14px;
}
.kpi-card {
    background: white; padding: 20px; border-radius: 22px;
    box-shadow: 0px 5px 16px rgba(0,0,0,0.04);
    text-align: center; min-height: 105px;
}
.kpi-number { font-size: 34px; font-weight: 800; color: #111111; }
.kpi-label { font-size: 13px; color: #6E6E73; }
.event-card {
    background: white; padding: 18px; border-radius: 22px;
    box-shadow: 0px 5px 16px rgba(0,0,0,0.04);
    min-height: 215px; margin-bottom: 6px;
}
.details-card {
    background: white; padding: 26px; border-radius: 24px;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.05); margin-top: 12px;
}
.event-title { font-size: 17px; font-weight: 750; color: #111111; margin-bottom: 8px; }
.section-title { font-size: 24px; font-weight: 750; color: #111111; margin-top: 16px; margin-bottom: 8px; }
.small-text { color: #6E6E73; font-size: 13px; }
.badge-high {
    background-color: #FFE8E8; color: #B00020; padding: 4px 8px;
    border-radius: 16px; font-size: 11px; font-weight: 700;
}
.badge-type {
    background-color: #EAF3FF; color: #0057B8; padding: 4px 8px;
    border-radius: 16px; font-size: 11px; font-weight: 700;
}
.badge-score {
    background-color: #E8F7EF; color: #087A3D; padding: 4px 8px;
    border-radius: 16px; font-size: 11px; font-weight: 700;
}
</style>
""", unsafe_allow_html=True)


def parse_event_date(date_text):
    try:
        if str(date_text).lower() in ["live", "unknown", "nan", ""]:
            return None
        return datetime.strptime(str(date_text), "%d-%b-%Y")
    except Exception:
        return None


def get_days_remaining(date_text):
    event_date = parse_event_date(date_text)
    if event_date is None:
        return "Live"
    return (event_date.date() - datetime.now().date()).days


def get_event_status(date_text):
    days = get_days_remaining(date_text)

    if days == "Live":
        return "Live Source"
    if days < 0:
        return "Completed"
    if days <= 7:
        return "Closing Soon"
    if days <= 30:
        return "Upcoming Soon"
    return "Upcoming"


def get_technology(event_name, source):
    text = f"{event_name} {source}".lower()

    if "agentic" in text or "agents" in text:
        return "Agentic AI"
    if "generative" in text or "genai" in text or "gemini" in text:
        return "Generative AI"
    if "cloud" in text or "aws" in text or "azure" in text:
        return "Cloud AI"
    if "nvidia" in text:
        return "AI Infrastructure"
    if "openai" in text or "llm" in text:
        return "LLM"
    if "hackathon" in text or "challenge" in text:
        return "AI Innovation"
    return "Artificial Intelligence"


def get_audience(event_type):
    event_type = str(event_type).lower()

    if event_type == "government":
        return "Professionals"
    if event_type == "hackathon":
        return "Intermediate"
    if event_type == "workshop":
        return "Beginner to Intermediate"
    return "All"


def get_certificate(event_type, source):
    source = str(source).lower()

    if source in ["microsoft", "aws", "google", "nvidia", "ibm", "openai"]:
        return "Possible"
    if str(event_type).lower() == "government":
        return "Check Website"
    return "No"


def calculate_ai_score(row):
    score = 45

    if str(row["Priority"]).lower() == "high":
        score += 20
    if str(row["Fee"]).lower() == "free":
        score += 10
    if str(row["Mode"]).lower() == "online":
        score += 5
    if str(row["Type"]).lower() == "government":
        score += 10
    if str(row["Type"]).lower() == "hackathon":
        score += 8

    days = get_days_remaining(row["Date"])

    if isinstance(days, int):
        if 0 <= days <= 30:
            score += 7
        elif days > 30:
            score += 3

    return min(score, 100)


def recommendation_reason(row):
    reasons = []

    if str(row["Priority"]).lower() == "high":
        reasons.append("high-priority")
    if str(row["Fee"]).lower() == "free":
        reasons.append("free participation")
    if str(row["Mode"]).lower() == "online":
        reasons.append("online access")
    if str(row["Type"]).lower() == "government":
        reasons.append("government-backed")
    if str(row["Technology"]):
        reasons.append(row["Technology"])

    if not reasons:
        return "Recommended based on relevance and source quality."

    return "Recommended because it is " + ", ".join(reasons) + "."


def show_table(dataframe):
    st.dataframe(
        dataframe.reset_index(drop=True),
        use_container_width=True,
        column_config={
            "Register": st.column_config.LinkColumn("Register")
        }
    )


def search_events(dataframe, query):
    query = query.lower().strip()

    if not query:
        return dataframe

    return dataframe[
        dataframe.apply(
            lambda row: query in " ".join(row.astype(str)).lower(),
            axis=1
        )
    ]


def assistant_answer(dataframe, question):
    q = question.lower().strip()
    result = dataframe.copy()

    if "government" in q or "govt" in q:
        result = result[result["Type"].str.lower() == "government"]
    elif "workshop" in q:
        result = result[result["Type"].str.lower() == "workshop"]
    elif "hackathon" in q:
        result = result[result["Type"].str.lower() == "hackathon"]
    elif "high" in q or "priority" in q:
        result = result[result["Priority"].str.lower() == "high"]
    elif "free" in q:
        result = result[result["Fee"].str.lower() == "free"]
    elif "online" in q:
        result = result[result["Mode"].str.lower() == "online"]
    elif "certificate" in q:
        result = result[result["Certificate"].str.lower() != "no"]
    elif "closing" in q or "soon" in q:
        result = result[result["Status"].str.lower().isin(["closing soon", "upcoming soon"])]
    elif "genai" in q or "generative" in q:
        result = result[result["Technology"].str.lower() == "generative ai"]
    elif "agentic" in q:
        result = result[result["Technology"].str.lower() == "agentic ai"]
    elif "best" in q or "top" in q or "recommend" in q:
        result = result.sort_values(by="AI Score", ascending=False).head(5)
    else:
        result = search_events(result, q)

    return result


def show_event_cards(dataframe, max_cards=3):
    cards_df = dataframe.head(max_cards).reset_index(drop=True)

    if cards_df.empty:
        st.warning("No events found")
        return

    cols = st.columns(3)

    for index, row in cards_df.iterrows():
        with cols[index]:
            days = row["Days Remaining"]
            days_text = f"{days} days left" if isinstance(days, int) else str(days)

            st.markdown(f"""
            <div class="event-card">
                <div class="event-title">{row["Event"]}</div>
                <span class="badge-type">{row["Type"]}</span>
                <span class="badge-high">🔥 {row["Priority"]}</span>
                <span class="badge-score">AI Score {row["AI Score"]}</span>
                <br><br>
                <p><b>Date:</b> {row["Date"]}</p>
                <p><b>Status:</b> {row["Status"]}</p>
                <p><b>Time Left:</b> {days_text}</p>
                <p><b>Technology:</b> {row["Technology"]}</p>
                <p><b>Source:</b> {row["Source"]}</p>
            </div>
            """, unsafe_allow_html=True)

            st.link_button("Register", row["Register"], use_container_width=True)


if not os.path.exists("events.csv"):
    st.error("events.csv file not found. Please run fetch_events.py first.")
    st.stop()

df = pd.read_csv("events.csv")

required_columns = [
    "Event", "Type", "Mode", "Date", "Fee",
    "Priority", "Source", "Register", "LastUpdated"
]

for column in required_columns:
    if column not in df.columns:
        df[column] = ""

for column in required_columns:
    df[column] = df[column].astype(str).str.strip()

df["Days Remaining"] = df["Date"].apply(get_days_remaining)
df["Status"] = df["Date"].apply(get_event_status)
df["Technology"] = df.apply(lambda row: get_technology(row["Event"], row["Source"]), axis=1)
df["Audience"] = df["Type"].apply(get_audience)
df["Certificate"] = df.apply(lambda row: get_certificate(row["Type"], row["Source"]), axis=1)
df["AI Score"] = df.apply(calculate_ai_score, axis=1)
df["Recommendation Reason"] = df.apply(recommendation_reason, axis=1)

df = df.sort_values(by=["AI Score"], ascending=False)

total_events = len(df)
government_events = len(df[df["Type"].str.lower() == "government"])
workshops = len(df[df["Type"].str.lower() == "workshop"])
high_priority_events = len(df[df["Priority"].str.lower() == "high"])
connected_sources = df["Source"].nunique()
avg_score = int(df["AI Score"].mean()) if total_events > 0 else 0
top_category = df["Type"].value_counts().idxmax() if total_events > 0 else "N/A"
top_source = df["Source"].value_counts().idxmax() if total_events > 0 else "N/A"
highest_scored_event = df.iloc[0]["Event"] if total_events > 0 else "N/A"
most_active_priority = df["Priority"].value_counts().idxmax() if total_events > 0 else "N/A"
closing_soon_count = len(df[df["Status"].isin(["Closing Soon", "Upcoming Soon"])])
certificate_count = len(df[df["Certificate"].str.lower() != "no"])
free_events_count = len(df[df["Fee"].str.lower() == "free"])

last_modified = os.path.getmtime("events.csv")
last_refreshed = datetime.fromtimestamp(last_modified).strftime("%d-%b-%Y %H:%M:%S")

new_events_count = 0
if os.path.exists("new_events.csv"):
    try:
        new_events_count = len(pd.read_csv("new_events.csv"))
    except Exception:
        new_events_count = 0

old_archive_count = 0
if os.path.exists("archive/old_events.csv"):
    try:
        old_archive_count = len(pd.read_csv("archive/old_events.csv"))
    except Exception:
        old_archive_count = 0

completed_archive_count = 0
if os.path.exists("archive/completed_events.csv"):
    try:
        completed_archive_count = len(pd.read_csv("archive/completed_events.csv"))
    except Exception:
        completed_archive_count = 0

expected_sources = [
    "IndiaAI",
    "MeitY",
    "Google",
    "NASSCOM",
    "Devpost",
    "Microsoft",
    "NVIDIA",
    "OpenAI",
    "AWS"
]

source_counts = df["Source"].value_counts().to_dict()
healthy_sources = len([s for s in expected_sources if source_counts.get(s, 0) > 0])
warning_sources = len(expected_sources) - healthy_sources

st.sidebar.title("🚀 AI Events Radar")
st.sidebar.caption("v7.1 Platform Control Center")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📅 Events",
        "📊 Analytics",
        "🌐 Sources",
        "🔎 Search",
        "🤖 AI Assistant",
        "📂 Archive",
        "🧾 Event Details",
        "🆕 New Events",
        "📡 Source Health",
        "📰 Daily Digest",
        "⚙️ Platform Status"
    ]
)

st.sidebar.markdown("---")
st.sidebar.metric("Active Events", total_events)
st.sidebar.metric("New Events", new_events_count)
st.sidebar.metric("Healthy Sources", healthy_sources)

st.markdown("""
<div class="hero-card">
    <h1>🚀 AI Events Radar</h1>
    <h3>Global Real-Time AI Event Intelligence Platform</h3>
    <p class="small-text">
        A centralized lifetime platform to discover, score, track, archive, and prioritize AI events across Government, Enterprise, Community, Cloud, and Innovation sources.
    </p>
</div>
""", unsafe_allow_html=True)

top_col1, top_col2 = st.columns([4, 1])

with top_col1:
    st.info(f"Last Refreshed: {last_refreshed}")

with top_col2:
    if st.button("🔄 Refresh", use_container_width=True):
        with st.spinner("Refreshing events from all connected sources..."):
            result = subprocess.run(
                ["python", "fetch_events.py"],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                st.success("Refresh completed")
                st.text(result.stdout)
                st.rerun()
            else:
                st.error("Refresh failed")
                st.text(result.stderr)


if page == "🏠 Dashboard":

    st.markdown('<div class="section-title">Executive Overview</div>', unsafe_allow_html=True)

    k1, k2, k3, k4, k5, k6 = st.columns(6)

    with k1:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-number">{total_events}</div><div class="kpi-label">Total Events</div></div>""", unsafe_allow_html=True)

    with k2:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-number">{connected_sources}</div><div class="kpi-label">Sources</div></div>""", unsafe_allow_html=True)

    with k3:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-number">{new_events_count}</div><div class="kpi-label">New Events</div></div>""", unsafe_allow_html=True)

    with k4:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-number">{high_priority_events}</div><div class="kpi-label">High Priority</div></div>""", unsafe_allow_html=True)

    with k5:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-number">{healthy_sources}</div><div class="kpi-label">Healthy Sources</div></div>""", unsafe_allow_html=True)

    with k6:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-number">{avg_score}</div><div class="kpi-label">Avg AI Score</div></div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-title">🔥 Top AI Recommended Events</div>', unsafe_allow_html=True)

    show_event_cards(df, max_cards=3)

    st.info(
        f"📌 AI Recommendation: Prioritize events with AI Score above 85. Most active category: {top_category}."
    )

    st.markdown('<div class="section-title">🧠 Executive Insights</div>', unsafe_allow_html=True)

    e1, e2 = st.columns(2)

    with e1:
        st.success(f"Top Source: {top_source}")
        st.success(f"Most Active Priority: {most_active_priority}")
        st.success(f"New Events Detected: {new_events_count}")

    with e2:
        st.success(f"Top Category: {top_category}")
        st.success(f"Highest Scored Event: {highest_scored_event}")
        st.success(f"Completed Events Archived: {completed_archive_count}")


elif page == "📅 Events":

    st.markdown('<div class="section-title">📅 All Active Events</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        type_filter = st.selectbox("Type", ["All"] + sorted(df["Type"].unique().tolist()))

    with c2:
        priority_filter = st.selectbox("Priority", ["All"] + sorted(df["Priority"].unique().tolist()))

    with c3:
        source_filter = st.selectbox("Source", ["All"] + sorted(df["Source"].unique().tolist()))

    with c4:
        status_filter = st.selectbox("Status", ["All"] + sorted(df["Status"].unique().tolist()))

    filtered_df = df.copy()

    if type_filter != "All":
        filtered_df = filtered_df[filtered_df["Type"] == type_filter]

    if priority_filter != "All":
        filtered_df = filtered_df[filtered_df["Priority"] == priority_filter]

    if source_filter != "All":
        filtered_df = filtered_df[filtered_df["Source"] == source_filter]

    if status_filter != "All":
        filtered_df = filtered_df[filtered_df["Status"] == status_filter]

    show_table(filtered_df)


elif page == "📊 Analytics":

    st.markdown('<div class="section-title">📊 Real-Time Event Analytics</div>', unsafe_allow_html=True)

    source_df = df["Source"].value_counts().reset_index()
    source_df.columns = ["Source", "Events Count"]

    type_df = df["Type"].value_counts().reset_index()
    type_df.columns = ["Type", "Events Count"]

    tech_df = df["Technology"].value_counts().reset_index()
    tech_df.columns = ["Technology", "Events Count"]

    status_df = df["Status"].value_counts().reset_index()
    status_df.columns = ["Status", "Events Count"]

    a1, a2 = st.columns(2)

    with a1:
        st.write("Events by Source")
        st.bar_chart(source_df.set_index("Source"))

    with a2:
        st.write("Events by Technology")
        st.bar_chart(tech_df.set_index("Technology"))

    a3, a4 = st.columns(2)

    with a3:
        st.write("Events by Type")
        st.bar_chart(type_df.set_index("Type"))

    with a4:
        st.write("Events by Status")
        st.bar_chart(status_df.set_index("Status"))


elif page == "🌐 Sources":

    st.markdown('<div class="section-title">🌐 Connected Global Sources</div>', unsafe_allow_html=True)

    source_df = df["Source"].value_counts().reset_index()
    source_df.columns = ["Source", "Events Count"]

    s1, s2, s3 = st.columns(3)

    for index, row in source_df.iterrows():
        target_col = [s1, s2, s3][index % 3]

        with target_col:
            st.markdown(f"""
            <div class="event-card">
                <div class="event-title">{row["Source"]}</div>
                <p><b>Events:</b> {row["Events Count"]}</p>
                <p class="small-text">Source connected and active</p>
            </div>
            """, unsafe_allow_html=True)


elif page == "🔎 Search":

    st.markdown('<div class="section-title">🔎 Global AI Event Search</div>', unsafe_allow_html=True)

    search_query = st.text_input(
        "Search by keyword: government, workshop, hackathon, free, high, GenAI, Agentic AI, certificate"
    )

    if search_query:
        search_result = search_events(df, search_query)

        if not search_result.empty:
            st.success(f"Found {len(search_result)} matching event(s)")
            show_table(search_result)
        else:
            st.warning("No matching events found")
    else:
        st.info("Enter a keyword to search across all events.")


elif page == "🤖 AI Assistant":

    st.markdown('<div class="section-title">🤖 AI Event Assistant</div>', unsafe_allow_html=True)

    st.write("Ask questions like:")
    st.info("Best events | Free workshops | Closing soon | Certificate events | GenAI events | Agentic AI events")

    question = st.text_input("Ask AI")

    if question:
        result = assistant_answer(df, question)

        if not result.empty:
            st.success(f"AI found {len(result)} matching event(s).")
            show_table(result)
        else:
            st.warning("No matching events found.")


elif page == "📂 Archive":

    st.markdown('<div class="section-title">📂 Archived Events</div>', unsafe_allow_html=True)

    archive_path = "archive/old_events.csv"
    completed_path = "archive/completed_events.csv"

    if os.path.exists(archive_path):
        archive_df = pd.read_csv(archive_path)
        st.write(f"Total Old Archived Events: {len(archive_df)}")
        show_table(archive_df)
    else:
        st.warning("No old archive found yet.")

    st.markdown("### Completed Events Archive")

    if os.path.exists(completed_path):
        completed_df = pd.read_csv(completed_path)
        st.write(f"Total Completed Events Archived: {len(completed_df)}")
        show_table(completed_df)
    else:
        st.info("No completed events archive found yet.")


elif page == "🧾 Event Details":

    st.markdown('<div class="section-title">🧾 Event Details</div>', unsafe_allow_html=True)

    selected_event = st.selectbox(
        "Select an event to view details",
        df["Event"].tolist()
    )

    selected_row = df[df["Event"] == selected_event].iloc[0]

    st.markdown(f"""
    <div class="details-card">
        <h2>{selected_row["Event"]}</h2>
        <p><b>AI Score:</b> {selected_row["AI Score"]}/100</p>
        <p><b>Technology:</b> {selected_row["Technology"]}</p>
        <p><b>Status:</b> {selected_row["Status"]}</p>
        <p><b>Days Remaining:</b> {selected_row["Days Remaining"]}</p>
        <p><b>Audience:</b> {selected_row["Audience"]}</p>
        <p><b>Certificate:</b> {selected_row["Certificate"]}</p>
        <p><b>Type:</b> {selected_row["Type"]}</p>
        <p><b>Source:</b> {selected_row["Source"]}</p>
        <p><b>Date:</b> {selected_row["Date"]}</p>
        <p><b>Mode:</b> {selected_row["Mode"]}</p>
        <p><b>Fee:</b> {selected_row["Fee"]}</p>
        <p><b>Priority:</b> {selected_row["Priority"]}</p>
        <p><b>Last Updated:</b> {selected_row["LastUpdated"]}</p>
        <h3>Why this event is recommended</h3>
        <p>{selected_row["Recommendation Reason"]}</p>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "Register for this event",
        selected_row["Register"],
        use_container_width=True
    )


elif page == "🆕 New Events":

    st.markdown('<div class="section-title">🆕 Newly Detected Events</div>', unsafe_allow_html=True)

    new_events_path = "new_events.csv"

    if os.path.exists(new_events_path):
        new_df = pd.read_csv(new_events_path)

        if not new_df.empty:
            st.success(f"{len(new_df)} new event(s) detected in the latest refresh.")
            show_table(new_df)
        else:
            st.info("No new events detected in the latest refresh.")
    else:
        st.warning("new_events.csv not found. Please click Refresh once.")


elif page == "📡 Source Health":

    st.markdown('<div class="section-title">📡 Source Health Monitor</div>', unsafe_allow_html=True)

    health_rows = []

    for source in expected_sources:
        count = source_counts.get(source, 0)
        status = "Healthy" if count > 0 else "Warning"

        health_rows.append(
            {
                "Source": source,
                "Events Count": count,
                "Status": status,
                "Last Checked": last_refreshed
            }
        )

    health_df = pd.DataFrame(health_rows)

    h1, h2, h3 = st.columns(3)

    with h1:
        st.metric("Expected Sources", len(expected_sources))

    with h2:
        st.metric("Healthy Sources", healthy_sources)

    with h3:
        st.metric("Warning Sources", warning_sources)

    st.dataframe(health_df, use_container_width=True)

    st.markdown("### Source Summary")

    for _, row in health_df.iterrows():
        if row["Status"] == "Healthy":
            st.success(f"{row['Source']} is active with {row['Events Count']} event(s).")
        else:
            st.warning(f"{row['Source']} returned 0 events. Please review the source connector.")


elif page == "📰 Daily Digest":

    st.markdown('<div class="section-title">📰 Daily AI Events Digest</div>', unsafe_allow_html=True)

    today_text = datetime.now().strftime("%d-%b-%Y")

    st.success(f"AI Events Daily Digest generated on {today_text}")

    d1, d2, d3, d4 = st.columns(4)

    with d1:
        st.metric("Total Events", total_events)

    with d2:
        st.metric("High Priority", high_priority_events)

    with d3:
        st.metric("Free Events", free_events_count)

    with d4:
        st.metric("New Events", new_events_count)

    st.markdown("### 🔥 Top Recommended Events")

    top_digest_events = df.sort_values(
        by="AI Score",
        ascending=False
    ).head(5)

    show_table(top_digest_events)

    st.markdown("### 🆕 Newly Detected Events")

    if os.path.exists("new_events.csv"):
        new_df = pd.read_csv("new_events.csv")

        if not new_df.empty:
            show_table(new_df.head(5))
        else:
            st.info("No new events detected in latest refresh.")
    else:
        st.warning("new_events.csv not available yet.")

    st.markdown("### 🏛 Government / Public AI Programs")

    govt_df = df[df["Type"].str.lower() == "government"]

    if not govt_df.empty:
        show_table(govt_df)
    else:
        st.info("No government AI programs found.")

    st.markdown("### 🎓 Certificate Opportunities")

    cert_df = df[df["Certificate"].str.lower() != "no"]

    if not cert_df.empty:
        show_table(cert_df.head(10))
    else:
        st.info("No certificate opportunities found.")

    st.markdown("### 🤖 AI Recommendation")

    best_event = df.sort_values(
        by="AI Score",
        ascending=False
    ).iloc[0]

    st.info(
        f"Recommended Event: {best_event['Event']} "
        f"| Source: {best_event['Source']} "
        f"| AI Score: {best_event['AI Score']}/100"
    )


elif page == "⚙️ Platform Status":

    st.markdown('<div class="section-title">⚙️ Platform Status</div>', unsafe_allow_html=True)

    p1, p2, p3, p4 = st.columns(4)

    with p1:
        st.metric("Active Events", total_events)

    with p2:
        st.metric("New Events", new_events_count)

    with p3:
        st.metric("Old Archive", old_archive_count)

    with p4:
        st.metric("Completed Archive", completed_archive_count)

    st.markdown("### Refresh Engine Status")

    st.success("fetch_events.py is connected as the platform refresh engine.")
    st.info(f"Last Refresh Time: {last_refreshed}")

    st.markdown("### Platform Readiness")

    readiness_rows = [
        {"Feature": "Dashboard", "Status": "Ready"},
        {"Feature": "Multi-source Fetch Engine", "Status": "Ready"},
        {"Feature": "New Event Detection", "Status": "Ready"},
        {"Feature": "Archive Engine", "Status": "Ready"},
        {"Feature": "Completed Event Archive", "Status": "Ready"},
        {"Feature": "Source Health Monitor", "Status": "Ready"},
        {"Feature": "Daily Digest", "Status": "Ready"},
        {"Feature": "Real Web Scraping", "Status": "Pending"},
        {"Feature": "Database Backend", "Status": "Pending"},
        {"Feature": "Public Deployment", "Status": "Pending"}
    ]

    readiness_df = pd.DataFrame(readiness_rows)

    st.dataframe(readiness_df, use_container_width=True)

st.caption("AI Events Radar v7.1 | Global Real-Time AI Event Intelligence Platform | Platform Status Enabled")