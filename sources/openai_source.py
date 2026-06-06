import requests
from bs4 import BeautifulSoup

def get_openai_events():

    events = []

    url = "https://openai.com/news/"

    try:
        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        if response.status_code == 200:

            soup = BeautifulSoup(response.text, "html.parser")

            events.append({
                "Event": "OpenAI News and Events Portal",
                "Type": "Workshop",
                "Mode": "Online",
                "Date": "Live",
                "Fee": "Check Website",
                "Priority": "High",
                "Source": "OpenAI",
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
                        "openai" in text
                        or "developer" in text
                        or "api" in text
                        or "agents" in text
                        or "chatgpt" in text
                        or "gpt" in text
                        or "event" in text
                    )
                ):

                    register_link = url

                    if href:
                        if href.startswith("http"):
                            register_link = href
                        elif href.startswith("/"):
                            register_link = "https://openai.com" + href

                    events.append({
                        "Event": f"OpenAI Update/Event: {title}",
                        "Type": "Workshop",
                        "Mode": "Online",
                        "Date": "Live",
                        "Fee": "Check Website",
                        "Priority": "Medium",
                        "Source": "OpenAI",
                        "Register": register_link
                    })

                    added += 1

        else:
            events.append({
                "Event": "OpenAI Website Unavailable",
                "Type": "Workshop",
                "Mode": "Online",
                "Date": "Unknown",
                "Fee": "Unknown",
                "Priority": "Medium",
                "Source": "OpenAI",
                "Register": url
            })

    except Exception as e:

        print("OpenAI Error:", e)

        events.append({
            "Event": "OpenAI Source Error",
            "Type": "Workshop",
            "Mode": "Online",
            "Date": "Unknown",
            "Fee": "Unknown",
            "Priority": "Low",
            "Source": "OpenAI",
            "Register": url
        })

    return events