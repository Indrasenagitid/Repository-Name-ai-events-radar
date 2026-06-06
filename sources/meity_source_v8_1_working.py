import requests
from bs4 import BeautifulSoup

def get_meity_events():

    events = []

    url = "https://www.meity.gov.in/"

    try:
        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        if response.status_code == 200:

            soup = BeautifulSoup(response.text, "html.parser")

            events.append({
                "Event": "MeitY Official Portal",
                "Type": "Government",
                "Mode": "Online",
                "Date": "Live",
                "Fee": "Check Website",
                "Priority": "High",
                "Source": "MeitY",
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
                    and len(title) < 140
                    and added < 10
                    and (
                        "ai" in text
                        or "artificial intelligence" in text
                        or "digital india" in text
                        or "technology" in text
                        or "startup" in text
                        or "innovation" in text
                        or "scheme" in text
                        or "program" in text
                    )
                ):

                    register_link = url

                    if href:
                        if href.startswith("http"):
                            register_link = href
                        elif href.startswith("/"):
                            register_link = "https://www.meity.gov.in" + href

                    events.append({
                        "Event": f"MeitY Update/Event: {title}",
                        "Type": "Government",
                        "Mode": "Online",
                        "Date": "Live",
                        "Fee": "Check Website",
                        "Priority": "High",
                        "Source": "MeitY",
                        "Register": register_link
                    })

                    added += 1

        else:
            events.append({
                "Event": "MeitY Website Unavailable",
                "Type": "Government",
                "Mode": "Online",
                "Date": "Unknown",
                "Fee": "Unknown",
                "Priority": "Medium",
                "Source": "MeitY",
                "Register": url
            })

    except Exception as e:

        print("MeitY Error:", e)

        events.append({
            "Event": "MeitY Source Error",
            "Type": "Government",
            "Mode": "Online",
            "Date": "Unknown",
            "Fee": "Unknown",
            "Priority": "Low",
            "Source": "MeitY",
            "Register": url
        })

    return events