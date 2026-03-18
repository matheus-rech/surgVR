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
        pos = f["position"]
        rot = f["rotation"]

        # Handle both dict (Unity JSON) and list formats
        if isinstance(pos, dict):
            pos_values = [pos["x"], pos["y"], pos["z"]]
        else:
            pos_values = list(pos)

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
