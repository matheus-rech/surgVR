import argparse
import glob
import os

from dataset import compute_label
from preprocess import load_session, to_array

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SESSIONS_ROOT = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "dataset", "sessions"))


def build_parser():
    parser = argparse.ArgumentParser(description="Train VRTransformer on VRDataset sessions.")
    parser.add_argument(
        "--sessions-root",
        default=DEFAULT_SESSIONS_ROOT,
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
    parser.add_argument(
        "--epochs",
        type=int,
        default=10,
        help="Number of epochs to train for (default: %(default)s).",
    )
    return parser


def resolve_session_paths(args, parser):
    if args.epochs < 1:
        parser.error("--epochs must be at least 1")

    if args.sessions:
        session_paths = []
        for session_dir in args.sessions:
            if not os.path.isdir(session_dir):
                parser.error(f"Session path does not exist or is not a directory: {session_dir}")
            session_paths.append(session_dir)
        return session_paths

    pattern = os.path.join(args.sessions_root, "*/")
    session_paths = sorted(glob.glob(pattern))
    if not session_paths:
        parser.error(f"No session directories found matching pattern: {pattern}")
    return session_paths


def train_with_torch(session_paths, epochs):
    import torch
    from torch.utils.data import DataLoader

    from dataset import VRDataset
    from model import VRTransformer

    dataset = VRDataset(session_paths)
    loader = DataLoader(dataset, batch_size=1)

    model = VRTransformer()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

    for epoch in range(epochs):
        total_loss = 0.0
        num_batches = 0
        for x, y in loader:
            pred = model(x).squeeze(-1)
            loss = ((pred - y) ** 2).mean()

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            num_batches += 1

        avg_loss = total_loss / num_batches if num_batches > 0 else 0.0
        print(f"Epoch {epoch} Loss: {avg_loss:.6f}")


def build_demo_features(session_path):
    telemetry, events = load_session(session_path)
    x = to_array(telemetry)
    if len(x) == 0:
        raise ValueError(f"Session {session_path} has no telemetry frames.")

    positions = [row[1:4] for row in x]
    if len(positions) < 2:
        total_distance = 0.0
    else:
        total_distance = 0.0
        for current, previous in zip(positions[1:], positions[:-1]):
            total_distance += sum((float(a) - float(b)) ** 2 for a, b in zip(current, previous)) ** 0.5

    speeds = [float(row[7]) for row in x]
    features = [
        float(x[-1][0]),
        total_distance,
        sum(speeds) / len(speeds),
        max(speeds),
        float(x[-1][8]),
        float(len(events)),
    ]
    return features, float(compute_label(x))


def train_with_fallback(session_paths, epochs):
    labels = []
    for session_path in session_paths:
        _features, label = build_demo_features(session_path)
        labels.append(label)

    prediction = sum(labels) / len(labels)
    loss = sum((prediction - label) ** 2 for label in labels) / len(labels)

    print("PyTorch not installed; using standard-library demo fallback.")
    for epoch in range(epochs):
        print(f"Epoch {epoch} Loss: {loss:.6f}")


def main():
    parser = build_parser()
    args = parser.parse_args()
    session_paths = resolve_session_paths(args, parser)

    try:
        train_with_torch(session_paths, args.epochs)
    except ModuleNotFoundError:
        train_with_fallback(session_paths, args.epochs)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
