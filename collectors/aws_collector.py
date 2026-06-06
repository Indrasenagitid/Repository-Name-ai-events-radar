import requests

def collect_aws_events():

    try:

        response = requests.get(
            "https://aws.amazon.com/events/",
            timeout=15
        )

        print("AWS Status Code:", response.status_code)

        return response.status_code

    except Exception as e:

        print("AWS Error:", e)

        return None