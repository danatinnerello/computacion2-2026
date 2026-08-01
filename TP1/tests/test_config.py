import sys
import unittest
from pathlib import Path
from unittest.mock import mock_open, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import config


class TestConfig(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data='{"sistema": 3}')
    def test_cargar_config(self, mock_file):
        self.assertEqual(config.cargar_config(), {"sistema": 3})


if __name__ == "__main__":
    unittest.main()