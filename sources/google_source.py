import requests
from bs4 import BeautifulSoup

def get_google_events():

    events = []

    url = "https://developers.google.com/events"

    try:

        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        if response.status_code == 200:

            soup = BeautifulSoup(response.text, "html.parser")

            events.append(
                {
                    "Event": "Google Developers Events Portal",
                    "Type": "Workshop",
                    "Mode": "Online",
                    "Date": "Live",
                    "Fee": "Check Website",
                    "Priority": "High",
                    "Source": "Google",
                    "Register": url
                }
            )

            links = soup.find_all("a")

            added = 0

            for link in links:

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
                        or "gemini" in text
                        or "cloud" in text
                        or "developer" in text
                        or "workshop" in text
                        or "webinar" in text
                    )
                ):

                    register_link = url

                    if href:
                        if href.startswith("http"):
                            register_link = href
                        elif href.startswith("/"):
                            register_link = "https://developers.google.com" + href

                    events.append(
                        {
                            "Event": f"Google Event: {title}",
                            "Type": "Workshop",
                            "Mode": "Online",
                            "Date": "Live",
                            "Fee": "Check Website",
                            "Priority": "Medium",
                            "Source": "Google",
                            "Register": register_link
                        }
                    )

                    added += 1

        else:

            events.append(
                {
                    "Event": "Google Developers Events Website Unavailable",
                    "Type": "Workshop",
                    "Mode": "Online",
                    "Date": "Unknown",
                    "Fee": "Unknown",
                    "Priority": "Medium",
                    "Source": "Google",
                    "Register": url
                }
            )

    except Exception as e:

        print("Google Error:", e)

        events.append(
            {
                "Event": "Google Source Error",
                "Type": "Workshop",
                "Mode": "Online",
                "Date": "Unknown",
                "Fee": "Unknown",
                "Priority": "Low",
                "Source": "Google",
                "Register": url
            }
        )

    return events