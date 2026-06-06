import requests
from bs4 import BeautifulSoup

def get_nasscom_events():

    events = []

    url = "https://nasscom.in/events"

    try:
        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        if response.status_code == 200:

            soup = BeautifulSoup(response.text, "html.parser")

            events.append({
                "Event": "NASSCOM Events Portal",
                "Type": "Workshop",
                "Mode": "Online",
                "Date": "Live",
                "Fee": "Check Website",
                "Priority": "High",
                "Source": "NASSCOM",
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
                        or "generative" in text
                        or "technology" in text
                        or "summit" in text
                        or "webinar" in text
                    )
                ):

                    register_link = url

                    if href:
                        if href.startswith("http"):
                            register_link = href
                        elif href.startswith("/"):
                            register_link = "https://nasscom.in" + href

                    events.append({
                        "Event": f"NASSCOM Event: {title}",
                        "Type": "Workshop",
                        "Mode": "Online",
                        "Date": "Live",
                        "Fee": "Check Website",
                        "Priority": "Medium",
                        "Source": "NASSCOM",
                        "Register": register_link
                    })

                    added += 1

        else:
            events.append({
                "Event": "NASSCOM Website Unavailable",
                "Type": "Workshop",
                "Mode": "Online",
                "Date": "Unknown",
                "Fee": "Unknown",
                "Priority": "Medium",
                "Source": "NASSCOM",
                "Register": url
            })

    except Exception as e:

        print("NASSCOM Error:", e)

        events.append({
            "Event": "NASSCOM Source Error",
            "Type": "Workshop",
            "Mode": "Online",
            "Date": "Unknown",
            "Fee": "Unknown",
            "Priority": "Low",
            "Source": "NASSCOM",
            "Register": url
        })

    return events