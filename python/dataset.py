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
        time = x[-1,0]
        collisions = x[-1,-1]
        max_time = x[:,0].max()
        efficiency = x.shape[0] / max_time if max_time > 0 else 1.0

        score = 100 - (0.5*time + 10*collisions + 50*(1-efficiency))
        return torch.tensor(score, dtype=torch.float32)
