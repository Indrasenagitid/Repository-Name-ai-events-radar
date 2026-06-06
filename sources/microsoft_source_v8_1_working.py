import requests
from bs4 import BeautifulSoup

def get_microsoft_events():

    events = []

    url = "https://learn.microsoft.com/events/"

    try:
        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        if response.status_code == 200:

            soup = BeautifulSoup(response.text, "html.parser")

            events.append({
                "Event": "Microsoft Events Portal",
                "Type": "Workshop",
                "Mode": "Online",
                "Date": "Live",
                "Fee": "Check Website",
                "Priority": "High",
                "Source": "Microsoft",
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
                        or "azure" in text
                        or "copilot" in text
                        or "developer" in text
                        or "webinar" in text
                        or "training" in text
                    )
                ):

                    register_link = url

                    if href:
                        if href.startswith("http"):
                            register_link = href
                        elif href.startswith("/"):
                            register_link = "https://learn.microsoft.com" + href

                    events.append({
                        "Event": f"Microsoft Event: {title}",
                        "Type": "Workshop",
                        "Mode": "Online",
                        "Date": "Live",
                        "Fee": "Check Website",
                        "Priority": "Medium",
                        "Source": "Microsoft",
                        "Register": register_link
                    })

                    added += 1

        else:
            events.append({
                "Event": "Microsoft Events Website Unavailable",
                "Type": "Workshop",
                "Mode": "Online",
                "Date": "Unknown",
                "Fee": "Unknown",
                "Priority": "Medium",
                "Source": "Microsoft",
                "Register": url
            })

    except Exception as e:

        print("Microsoft Error:", e)

        events.append({
            "Event": "Microsoft Source Error",
            "Type": "Workshop",
            "Mode": "Online",
            "Date": "Unknown",
            "Fee": "Unknown",
            "Priority": "Low",
            "Source": "Microsoft",
            "Register": url
        })

    return events