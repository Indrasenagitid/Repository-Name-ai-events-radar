import requests

def get_aws_events():

    events = []

    try:

        response = requests.get(
            "https://aws.amazon.com/events/",
            timeout=10
        )

        if response.status_code == 200:

            events.append(
                {
                    "Event": "AWS Live Events Portal",
                    "Type": "Workshop",
                    "Mode": "Online",
                    "Date": "Live",
                    "Fee": "Check Website",
                    "Priority": "High",
                    "Source": "AWS",
                    "Register": "https://aws.amazon.com/events/"
                }
            )

            events.append(
                {
                    "Event": "AWS GenAI Executive Summit TEST",
                    "Type": "Workshop",
                    "Mode": "Online",
                    "Date": "15-Aug-2026",
                    "Fee": "Free",
                    "Priority": "High",
                    "Source": "AWS",
                    "Register": "https://aws.amazon.com/events/"
                }
            )

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
                    "Register": "https://aws.amazon.com/events/"
                }
            )

    except Exception as e:

        print("AWS Error:", e)

    return events