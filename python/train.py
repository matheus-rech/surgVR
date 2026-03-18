import torch
from torch.utils.data import DataLoader
from dataset import VRDataset
from model import VRTransformer

dataset = VRDataset(["../dataset/sessions/session_001"])
loader = DataLoader(dataset, batch_size=1)

model = VRTransformer()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

for epoch in range(10):
    total_loss = 0.0
    num_batches = 0
    for x, y in loader:
        pred = model(x)
        loss = ((pred - y)**2).mean()

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        num_batches += 1

    avg_loss = total_loss / num_batches if num_batches > 0 else 0.0
    print(f"Epoch {epoch} Loss: {avg_loss}")
