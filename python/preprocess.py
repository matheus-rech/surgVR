import json
import numpy as np

def load_session(path):
    with open(f"{path}/telemetry.json") as f:
        telemetry = json.load(f)["items"]

    with open(f"{path}/events.json") as f:
        events = json.load(f)["items"]

    return telemetry, events

def to_array(telemetry):
    data = []
    for f in telemetry:
        data.append([
            f["time"],
            *f["position"],
            *f["rotation"],
            f["speed"],
            f["collisions"]
        ])
    return np.array(data)
