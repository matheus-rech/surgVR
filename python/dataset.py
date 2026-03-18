import torch
from torch.utils.data import Dataset
from preprocess import load_session, to_array

class VRDataset(Dataset):
    def __init__(self, session_paths):
        self.sessions = session_paths

    def __len__(self):
        return len(self.sessions)

    def __getitem__(self, idx):
        telemetry, events = load_session(self.sessions[idx])
        x = to_array(telemetry)

        score = self.compute_label(x)

        return torch.tensor(x, dtype=torch.float32), score

    def compute_label(self, x):
        time = x[-1, 0]
        collisions = x[-1, -1]

        # Penalize: longer time, more collisions
        # Reward: shorter completion time
        score = 100 - (0.5 * time + 10 * collisions)
        return torch.tensor(max(0.0, score), dtype=torch.float32)
