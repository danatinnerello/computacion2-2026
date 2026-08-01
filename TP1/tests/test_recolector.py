import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import recolector


class TestRecolector(unittest.TestCase):
    @patch("recolector.time", return_value=1234.0)
    @patch("recolector.obtener_usuario", return_value="danat")
    @patch("recolector.leer_fds", return_value=[{"fd": "0", "destino": "/dev/null", "tipo": "file"}])
    @patch("recolector.leer_cmdline", return_value="python")
    @patch("recolector.leer_stat", return_value={"pid": 1, "utime": 10, "stime": 5})
    @patch("recolector.leer_status", return_value={"Uid": "1000 1000 1000 1000"})
    @patch("recolector.obtener_pids", return_value=[1])
    def test_recolectar_construye_snapshot(
        self,
        mock_pids,
        mock_status,
        mock_stat,
        mock_cmdline,
        mock_fds,
        mock_usuario,
        mock_time,
    ):
        snapshot = recolector.recolectar()
        self.assertIn("timestamp", snapshot)
        self.assertIn("procesos", snapshot)
        self.assertEqual(snapshot["procesos"][1]["usuario"], "danat")
        self.assertEqual(snapshot["procesos"][1]["cmdline"], "python")
        self.assertEqual(snapshot["procesos"][1]["fds"][0]["tipo"], "file")


if __name__ == "__main__":
    unittest.main()