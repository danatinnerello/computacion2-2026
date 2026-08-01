import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import mock_open, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import procfs


class TestProcfs(unittest.TestCase):
    @patch("procfs.pwd.getpwuid")
    def test_obtener_usuario_devuelve_nombre(self, mock_getpwuid):
        mock_getpwuid.return_value.pw_name = "danat"
        self.assertEqual(procfs.obtener_usuario(1000), "danat")

    @patch("procfs.pwd.getpwuid", side_effect=KeyError)
    def test_obtener_usuario_con_uid_invalido_devuelve_string(self, mock_getpwuid):
        self.assertEqual(procfs.obtener_usuario(9999), "9999")

    def test_obtener_pids(self):
        entries = [
            SimpleNamespace(name="1", is_dir=lambda: True),
            SimpleNamespace(name="abc", is_dir=lambda: True),
            SimpleNamespace(name="2", is_dir=lambda: False),
        ]
        with patch("procfs.Path.iterdir", return_value=entries):
            self.assertEqual(procfs.obtener_pids(), [1])

    @patch("procfs.open", new_callable=mock_open, read_data="cpu 10 20 30 40 50 60 70 80\n")
    def test_leer_cpu_global(self, mock_file):
        esperado = {
            "user": 10,
            "nice": 20,
            "system": 30,
            "idle": 40,
            "iowait": 50,
            "irq": 60,
            "softirq": 70,
            "steal": 80,
        }
        self.assertEqual(procfs.leer_cpu_global(), esperado)

    @patch("procfs.open", new_callable=mock_open, read_data="0.12 0.34 0.56 0.78 0.90\n")
    def test_leer_loadavg(self, mock_file):
        self.assertEqual(procfs.leer_loadavg(), {"one": "0.12", "five": "0.34", "fifteen": "0.56"})

    @patch("procfs.open", new_callable=mock_open, read_data="123.45 678.90\n")
    @patch("procfs.time.time", return_value=200.0)
    def test_leer_uptime(self, mock_time, mock_file):
        uptime, boot_time = procfs.leer_uptime()
        self.assertAlmostEqual(uptime, 123.45)
        self.assertEqual(boot_time, 76)

    @patch("procfs.open", new_callable=mock_open, read_data="1 (bash) S 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\n")
    def test_leer_stat(self, mock_file):
        stat = procfs.leer_stat(1)
        self.assertEqual(stat["pid"], 1)
        self.assertEqual(stat["comm"], "bash")
        self.assertEqual(stat["state"], "S")

    @patch("procfs.open", new_callable=mock_open, read_data="Name:   bash\nUid:    1000 1000 1000 1000\n")
    def test_leer_status(self, mock_file):
        status = procfs.leer_status(1)
        self.assertEqual(status["Name"], "bash")
        self.assertEqual(status["Uid"], "1000 1000 1000 1000")

    @patch("procfs.open", new_callable=mock_open, read_data=b"python\x00arg1\x00")
    def test_leer_cmdline(self, mock_file):
        self.assertEqual(procfs.leer_cmdline(1), "python arg1")

    def test_leer_fds(self):
        def fake_readlink(path):
            if path.endswith("/0"):
                return "socket:[123]"
            return "/tmp/archivo"
        with patch("procfs.os.listdir", return_value=["0", "1"]), \
             patch("procfs.os.readlink", side_effect=fake_readlink):
            resultado = procfs.leer_fds(1)
            self.assertEqual(len(resultado), 2)
            self.assertEqual(resultado[0]["tipo"], "socket")
            self.assertEqual(resultado[1]["tipo"], "file")

    @patch("procfs.open", new_callable=mock_open, read_data="7f000000-7f010000 r-xp 00000000 08:01 123456 /bin/bash\n")
    def test_leer_maps_parses_segmentos(self, mock_file):
        resultado = procfs.leer_maps(1)
        self.assertEqual(resultado[0]["tipo"], "text")
        self.assertEqual(resultado[0]["path"], "/bin/bash")

    @patch("procfs.leer_maps", return_value=[
        {"tipo": "heap", "size_kb": 10},
        {"tipo": "stack", "size_kb": 5},
        {"tipo": "heap", "size_kb": 15},
    ])
    def test_resumir_segmentos(self, mock_leer_maps):
        resumen = procfs.resumir_segmentos(1)
        self.assertEqual(resumen["heap"], 25)
        self.assertEqual(resumen["stack"], 5)


if __name__ == "__main__":
    unittest.main()