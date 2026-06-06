import requests
from bs4 import BeautifulSoup

def get_nvidia_events():

    events = []

    url = "https://www.nvidia.com/en-us/events/"

    try:
        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        if response.status_code == 200:

            soup = BeautifulSoup(response.text, "html.parser")

            events.append({
                "Event": "NVIDIA Events Portal",
                "Type": "Workshop",
                "Mode": "Online",
                "Date": "Live",
                "Fee": "Check Website",
                "Priority": "High",
                "Source": "NVIDIA",
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
                        or "generative" in text
                        or "developer" in text
                        or "gtc" in text
                        or "webinar" in text
                        or "training" in text
                    )
                ):

                    register_link = url

                    if href:
                        if href.startswith("http"):
                            register_link = href
                        elif href.startswith("/"):
                            register_link = "https://www.nvidia.com" + href

                    events.append({
                        "Event": f"NVIDIA Event: {title}",
                        "Type": "Workshop",
                        "Mode": "Online",
                        "Date": "Live",
                        "Fee": "Check Website",
                        "Priority": "Medium",
                        "Source": "NVIDIA",
                        "Register": register_link
                    })

                    added += 1

        else:
            events.append({
                "Event": "NVIDIA Events Website Unavailable",
                "Type": "Workshop",
                "Mode": "Online",
                "Date": "Unknown",
                "Fee": "Unknown",
                "Priority": "Medium",
                "Source": "NVIDIA",
                "Register": url
            })

    except Exception as e:

        print("NVIDIA Error:", e)

        events.append({
            "Event": "NVIDIA Source Error",
            "Type": "Workshop",
            "Mode": "Online",
            "Date": "Unknown",
            "Fee": "Unknown",
            "Priority": "Low",
            "Source": "NVIDIA",
            "Register": url
        })

    return events