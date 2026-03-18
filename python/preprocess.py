import json
import numpy as np

def load_session(path):
    with open(f"{path}/telemetry.json") as f:
        telemetry = json.load(f)["items"]

    with open(f"{path}/events.json") as f:
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

        if isinstance(rot, dict):
            rot_values = [rot["x"], rot["y"], rot["z"]]
        else:
            rot_values = list(rot)

        data.append([
            f["time"],
            *pos_values,
            *rot_values,
            f["speed"],
            f["collisions"]
        ])
    return np.array(data)
