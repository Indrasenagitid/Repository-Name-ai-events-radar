import requests
from bs4 import BeautifulSoup

def get_aws_events():

    events = []

    try:

        url = "https://aws.amazon.com/events/"

        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        if response.status_code == 200:

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            # Always keep portal entry
            events.append(
                {
                    "Event": "AWS Events Portal",
                    "Type": "Workshop",
                    "Mode": "Online",
                    "Date": "Live",
                    "Fee": "Check Website",
                    "Priority": "High",
                    "Source": "AWS",
                    "Register": url
                }
            )

            links = soup.find_all("a")

            added = 0

            for link in links:

                title = link.get_text(strip=True)

                if (
                    len(title) > 10
                    and len(title) < 120
                    and added < 10
                ):

                    events.append(
                        {
                            "Event": f"AWS Event: {title}",
                            "Type": "Workshop",
                            "Mode": "Online",
                            "Date": "Live",
                            "Fee": "Check Website",
                            "Priority": "Medium",
                            "Source": "AWS",
                            "Register": url
                        }
                    )

                    added += 1

        else:

            events.append(
                {
                    "Event": "AWS Website Unavailable",
                    "Type": "Workshop",
                    "Mode": "Online",
                    "Date": "Unknown",
                    "Fee": "Unknown",
                    "Priority": "Medium",
                    "Source": "AWS",
                    "Register": url
                }
            )

    except Exception as e:

        print("AWS Error:", e)

        events.append(
            {
                "Event": "AWS Source Error",
                "Type": "Workshop",
                "Mode": "Online",
                "Date": "Unknown",
                "Fee": "Unknown",
                "Priority": "Low",
                "Source": "AWS",
                "Register": "https://aws.amazon.com/events/"
            }
        )

    return events