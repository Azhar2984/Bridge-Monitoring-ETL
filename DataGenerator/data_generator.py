import os
import json
import time
import random
from datetime import datetime, timedelta, timezone

base_dir = "streams"
sensor_types = ["bridge_temperature", "bridge_vibration", "bridge_tilt"]
bridge_ids = [1, 2, 3, 4, 5]

for s in sensor_types:
    os.makedirs(os.path.join(base_dir, s), exist_ok=True)

def create_event(sensor, bridge):
    event_time = datetime.now(timezone.utc) - timedelta(seconds=random.randint(0, 60))
    if sensor == "bridge_temperature":
        reading = round(random.uniform(-10, 40), 2)
    elif sensor == "bridge_vibration":
        reading = round(random.uniform(0, 5), 2)
    else:
        reading = round(random.uniform(0, 90), 2)

    return {
        "event_time": event_time.isoformat(),
        "bridge_id": bridge,
        "sensor_type": sensor.split("_")[1],
        "value": reading,
        "ingest_time": datetime.now(timezone.utc).isoformat()
    }

def main():
    counter = 0
    print("Generating sensor data... Press Ctrl+C to stop.")
    while True:
        for sensor in sensor_types:
            for bridge in bridge_ids:
                event = create_event(sensor, bridge)
                file_name = f"{int(time.time())}_{bridge}_{counter}.json"
                file_path = os.path.join(base_dir, sensor, file_name)
                with open(file_path, "w") as file:
                    json.dump(event, file)
                counter += 1
        time.sleep(30)

if __name__ == "__main__":
    main()
