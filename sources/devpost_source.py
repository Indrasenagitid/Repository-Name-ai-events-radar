import requests
from bs4 import BeautifulSoup

def get_devpost_events():

    events = []

    url = "https://devpost.com/hackathons"

    try:
        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        if response.status_code == 200:

            soup = BeautifulSoup(response.text, "html.parser")

            events.append({
                "Event": "Devpost Hackathons Portal",
                "Type": "Hackathon",
                "Mode": "Online",
                "Date": "Live",
                "Fee": "Check Website",
                "Priority": "High",
                "Source": "Devpost",
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
                        or "hackathon" in text
                        or "challenge" in text
                        or "innovation" in text
                        or "developer" in text
                        or "machine learning" in text
                    )
                ):

                    register_link = url

                    if href:
                        if href.startswith("http"):
                            register_link = href
                        elif href.startswith("/"):
                            register_link = "https://devpost.com" + href

                    events.append({
                        "Event": f"Devpost Hackathon: {title}",
                        "Type": "Hackathon",
                        "Mode": "Online",
                        "Date": "Live",
                        "Fee": "Check Website",
                        "Priority": "High",
                        "Source": "Devpost",
                        "Register": register_link
                    })

                    added += 1

        else:
            events.append({
                "Event": "Devpost Website Unavailable",
                "Type": "Hackathon",
                "Mode": "Online",
                "Date": "Unknown",
                "Fee": "Unknown",
                "Priority": "Medium",
                "Source": "Devpost",
                "Register": url
            })

    except Exception as e:

        print("Devpost Error:", e)

        events.append({
            "Event": "Devpost Source Error",
            "Type": "Hackathon",
            "Mode": "Online",
            "Date": "Unknown",
            "Fee": "Unknown",
            "Priority": "Low",
            "Source": "Devpost",
            "Register": url
        })

    return events