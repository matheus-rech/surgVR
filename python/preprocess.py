import json
import os
import numpy as np

def load_session(path):
    with open(os.path.join(path, "telemetry.json")) as f:
        telemetry = json.load(f)["items"]

    with open(os.path.join(path, "events.json")) as f:
        events = json.load(f)["items"]

    return telemetry, events

def to_array(telemetry):
    return np.array([
        [
            f["time"],
            f["position"]["x"], f["position"]["y"], f["position"]["z"],
            f["rotation"]["x"], f["rotation"]["y"], f["rotation"]["z"],
            f["speed"],
            f["collisions"]
        ]
        for f in telemetry
    ], dtype=np.float32)
