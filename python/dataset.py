import math

try:
    import torch
    from torch.utils.data import Dataset
except ModuleNotFoundError:  # pragma: no cover - exercised through train.py fallback
    torch = None

    class Dataset:  # type: ignore[override]
        pass

from preprocess import load_session, to_array

BASE_SCORE = 100.0
TIME_WEIGHT = 1.5
COLLISION_WEIGHT = 10.0
EFFICIENCY_WEIGHT = 25.0


def compute_efficiency(x):
    if len(x) < 2:
        return 1.0

    positions = [row[1:4] for row in x]

    path_length = 0.0
    for current, previous in zip(positions[1:], positions[:-1]):
        path_length += math.dist(current, previous)

    straight_line_distance = math.dist(positions[-1], positions[0])

    if path_length <= 1e-6:
        return 1.0 if straight_line_distance <= 1e-6 else 0.0

    return max(0.0, min(1.0, straight_line_distance / path_length))


def compute_label(x):
    if len(x) == 0:
        raise ValueError("Telemetry must contain at least one frame.")

    elapsed_time = float(x[-1][0])
    collisions = float(x[-1][-1])
    efficiency = compute_efficiency(x)

    score = BASE_SCORE - (
        TIME_WEIGHT * elapsed_time
        + COLLISION_WEIGHT * collisions
        + EFFICIENCY_WEIGHT * (1.0 - efficiency)
    )
    return max(0.0, score)


class VRDataset(Dataset):
    def __init__(self, session_paths):
        self.sessions = session_paths

    def __len__(self):
        return len(self.sessions)

    def __getitem__(self, idx):
        telemetry, _events = load_session(self.sessions[idx])
        x = to_array(telemetry)
        score = self.compute_label(x)

        if torch is None:
            return x, score

        return torch.tensor(x, dtype=torch.float32), torch.tensor(score, dtype=torch.float32)

    def compute_label(self, x):
        return compute_label(x)
