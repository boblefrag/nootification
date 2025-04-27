import random
import uuid
from random import choice
from time import sleep

import requests  # type: ignore

# URL to send the alerts to
url = "http://localhost:8000/webhooks/alerts"

# Locations from `initial_data.json`

locations = [
    "Carrefour" "Leclerc",
    "Auchan",
    "Intermarché",
    "Monoprix",
    "Super U",
    "Casino",
    "Franprix",
    "Cora",
    "Carrefour Market",
]


labels = ["theft", "suspicious", "normal"]


def generate_alert():
    label = choice(labels)

    # Generate a random UUID for the alert
    alert_uuid = str(uuid.uuid4())

    payload = {
        "url": f"https://media.veesion.io/{alert_uuid}.mp4",
        "location": choice(locations),
        "alert_uuid": alert_uuid,
        "label": label,
        "time_spotted": random.uniform(
            1742470260.0, 1742470260.083
        ),  # Random timestamp
    }

    return payload


def send_alert(payload):
    response = requests.post(url, json=payload)

    if response.status_code == 201:
        print(f"Alert {payload['alert_uuid']} sent successfully!")
    else:
        print(
            f"Failed to send alert {payload['alert_uuid']}. Status code: {response.status_code}"
        )


# Sending 10 alerts with different labels and locations
for _ in range(10):
    alert_payload = generate_alert()
    send_alert(alert_payload)
    sleep(random.uniform(1, 3))
