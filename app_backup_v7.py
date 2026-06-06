import streamlit as st
import pandas as pd
import subprocess
import os
from datetime import datetime

st.set_page_config(
    page_title="AI Events Radar",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
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
.badge-status {
    background-color: #FFF4D6; color: #7A4D00; padding: 4px 8px;
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
    today = datetime.now()
    days = (event_date.date() - today.date()).days
    return days


def get_event_status(date_text):
    days = get_days_remaining(date_text)

    if days == "Live":
        return "Live Source"

    if days < 0:
        return "Completed"
    elif days <= 7:
        return "Closing Soon"
    elif days <= 30:
        return "Upcoming Soon"
    else:
        return "Upcoming"


def get_technology(event_name, source):
    text = f"{event_name} {source}".lower()

    if "agentic" in text or "agents" in text:
        return "Agentic AI"
    elif "generative" in text or "genai" in text:
        return "Generative AI"
    elif "cloud" in text or "aws" in text or "azure" in text:
        return "Cloud AI"
    elif "nvidia" in text:
        return "AI Infrastructure"
    elif "openai" in text or "llm" in text:
        return "LLM"
    elif "hackathon" in text:
        return "AI Innovation"
    else:
        return "Artificial Intelligence"


def get_audience(event_type):
    event_type = str(event_type).lower()

    if event_type == "government":
        return "Professionals"
    elif event_type == "hackathon":
        return "Intermediate"
    elif event_type == "workshop":
        return "Beginner to Intermediate"
    else:
        return "All"


def get_certificate(event_type, source):
    source = str(source).lower()

    if source in ["microsoft", "aws", "google", "nvidia", "ibm"]:
        return "Possible"
    elif str(event_type).lower() == "government":
        return "Check Website"
    else:
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
        if days >= 0 and days <= 30:
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
avg_score = int(df["AI Score"].mean())
top_category = df["Type"].value_counts().idxmax()
top_source = df["Source"].value_counts().idxmax()
highest_scored_event = df.sort_values(by="AI Score", ascending=False).iloc[0]["Event"]
most_active_priority = df["Priority"].value_counts().idxmax()
closing_soon_count = len(df[df["Status"].isin(["Closing Soon", "Upcoming Soon"])])
certificate_count = len(df[df["Certificate"].str.lower() != "no"])

last_modified = os.path.getmtime("events.csv")
last_refreshed = datetime.fromtimestamp(last_modified).strftime("%d-%b-%Y %H:%M:%S")

st.markdown("""
<div class="hero-card">
    <h1>🚀 AI Events Radar</h1>
    <h3>Executive AI Event Intelligence Platform</h3>
    <p class="small-text">
        A centralized platform to discover, score, track, and prioritize AI events across Government, Enterprise, Community, and Social sources.
    </p>
</div>
""", unsafe_allow_html=True)

top_col1, top_col2 = st.columns([4, 1])

with top_col1:
    st.info(f"Last Refreshed: {last_refreshed}")

with top_col2:
    if st.button("🔄 Refresh", use_container_width=True):
        with st.spinner("Refreshing events..."):
            result = subprocess.run(
                ["python", "fetch_events.py"],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                st.success("Refreshed")
                st.rerun()
            else:
                st.error("Refresh failed")
                st.text(result.stderr)

page = st.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📅 Events",
        "📊 Analytics",
        "🌐 Sources",
        "🔎 Search",
        "🤖 AI Assistant",
        "📂 Archive",
        "🧾 Event Details"
    ],
    horizontal=True,
    label_visibility="collapsed"
)

if page == "🏠 Dashboard":

    st.markdown('<div class="section-title">Executive Overview</div>', unsafe_allow_html=True)

    k1, k2, k3, k4, k5, k6 = st.columns(6)

    with k1:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-number">{total_events}</div><div class="kpi-label">Total Events</div></div>""", unsafe_allow_html=True)

    with k2:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-number">{connected_sources}</div><div class="kpi-label">Sources</div></div>""", unsafe_allow_html=True)

    with k3:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-number">{high_priority_events}</div><div class="kpi-label">High Priority</div></div>""", unsafe_allow_html=True)

    with k4:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-number">{closing_soon_count}</div><div class="kpi-label">Upcoming Soon</div></div>""", unsafe_allow_html=True)

    with k5:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-number">{certificate_count}</div><div class="kpi-label">Certificate Possible</div></div>""", unsafe_allow_html=True)

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

    with e2:
        st.success(f"Top Category: {top_category}")
        st.success(f"Highest Scored Event: {highest_scored_event}")

elif page == "📅 Events":

    st.markdown('<div class="section-title">📅 All Events</div>', unsafe_allow_html=True)

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

    st.markdown('<div class="section-title">📊 Analytics</div>', unsafe_allow_html=True)

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

    st.markdown('<div class="section-title">🌐 Connected Sources</div>', unsafe_allow_html=True)

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

    st.markdown('<div class="section-title">🔎 AI Event Search</div>', unsafe_allow_html=True)

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

    if os.path.exists(archive_path):
        archive_df = pd.read_csv(archive_path)
        st.write(f"Total Archived Events: {len(archive_df)}")
        show_table(archive_df)
    else:
        st.warning("No archive found yet.")

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

st.caption("AI Events Radar v6.5 | Event Intelligence Engine | Multi-source AI Event Intelligence")