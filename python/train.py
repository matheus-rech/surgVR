import argparse
import glob
import os
import sys

import torch
from torch.utils.data import DataLoader
from dataset import VRDataset
from model import VRTransformer

parser = argparse.ArgumentParser(description="Train VRTransformer on VRDataset sessions.")
parser.add_argument(
    "--sessions-root",
    default="../dataset/sessions",
    help="Root directory containing session subdirectories (default: %(default)s).",
)
parser.add_argument(
    "--session",
    dest="sessions",
    action="append",
    help=(
        "Path to a session directory. Can be specified multiple times. "
        "If omitted, all subdirectories under --sessions-root are used."
    ),
)
args = parser.parse_args()

if args.sessions:
    session_paths = []
    for session_dir in args.sessions:
        if not os.path.isdir(session_dir):
            parser.error(f"Session path does not exist or is not a directory: {session_dir}")
        session_paths.append(session_dir)
else:
    pattern = os.path.join(args.sessions_root, "*/")
    session_paths = sorted(glob.glob(pattern))
    if not session_paths:
        parser.error(f"No session directories found matching pattern: {pattern}")

dataset = VRDataset(session_paths)
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
