import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class TrainDemoTest(unittest.TestCase):
    def test_train_script_runs_end_to_end_with_demo_session(self):
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "python" / "train.py"), "--epochs", "1"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("Epoch 0 Loss:", result.stdout)


if __name__ == "__main__":
    unittest.main()
