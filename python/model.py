import torch
import torch.nn as nn

class VRTransformer(nn.Module):
    def __init__(self, input_dim=9, hidden=128):
        super().__init__()

        self.input_proj = nn.Linear(input_dim, hidden)

        self.encoder = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=hidden, nhead=4),
            num_layers=3
        )

        self.head = nn.Linear(hidden, 1)

    def forward(self, x):
        x = self.input_proj(x)
        x = self.encoder(x)
        x = x.mean(dim=1)
        return self.head(x)
