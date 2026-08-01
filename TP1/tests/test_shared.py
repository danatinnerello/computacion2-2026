import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from shared import SharedState


class TestSharedState(unittest.TestCase):
    def test_shared_state_exposes_snapshot_and_intervalos(self):
        state = SharedState({"resumen": 2})
        self.assertTrue(hasattr(state, "snapshot"))
        self.assertTrue(hasattr(state, "intervalos"))
        self.assertEqual(state.intervalos["resumen"], 2)
        state.shutdown()


if __name__ == "__main__":
    unittest.main()
