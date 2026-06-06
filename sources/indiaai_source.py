import requests
from bs4 import BeautifulSoup

def get_indiaai_events():

    events = []

    url = "https://indiaai.gov.in/events"

    try:
        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        if response.status_code == 200:

            soup = BeautifulSoup(response.text, "html.parser")

            events.append({
                "Event": "IndiaAI Events Portal",
                "Type": "Government",
                "Mode": "Online",
                "Date": "Live",
                "Fee": "Check Website",
                "Priority": "High",
                "Source": "IndiaAI",
                "Register": url
            })

            added = 0

            for link in soup.find_all("a"):

                title = link.get_text(strip=True)
                href = link.get("href")

                if not title:
                    continue

                text = title.lower()

                if (
                    len(title) > 10
                    and len(title) < 120
                    and added < 10
                    and (
                        "ai" in text
                        or "artificial intelligence" in text
                        or "genai" in text
                        or "event" in text
                        or "workshop" in text
                        or "webinar" in text
                        or "program" in text
                        or "challenge" in text
                    )
                ):

                    register_link = url

                    if href:
                        if href.startswith("http"):
                            register_link = href
                        elif href.startswith("/"):
                            register_link = "https://indiaai.gov.in" + href

                    events.append({
                        "Event": f"IndiaAI Event: {title}",
                        "Type": "Government",
                        "Mode": "Online",
                        "Date": "Live",
                        "Fee": "Check Website",
                        "Priority": "High",
                        "Source": "IndiaAI",
                        "Register": register_link
                    })

                    added += 1

        else:
            events.append({
                "Event": "IndiaAI Website Unavailable",
                "Type": "Government",
                "Mode": "Online",
                "Date": "Unknown",
                "Fee": "Unknown",
                "Priority": "Medium",
                "Source": "IndiaAI",
                "Register": url
            })

    except Exception as e:

        print("IndiaAI Error:", e)

        events.append({
            "Event": "IndiaAI Source Error",
            "Type": "Government",
            "Mode": "Online",
            "Date": "Unknown",
            "Fee": "Unknown",
            "Priority": "Low",
            "Source": "IndiaAI",
            "Register": url
        })

    return events