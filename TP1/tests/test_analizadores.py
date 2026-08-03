import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from analizadores import cpu, fds, memoria, scheduling, senales as anal_senales, sistema, threads, resumen


class TestCpuAnalyzer(unittest.TestCase):
    def test_calcular_cpu(self):
        anterior = {
            "cpu": {"user": 100, "system": 100, "idle": 100, "iowait": 0},
            "procesos": {1: {"stat": {"utime": 10, "stime": 5}}},
        }
        actual = {
            "cpu": {"user": 110, "system": 110, "idle": 100, "iowait": 0},
            "procesos": {1: {"stat": {"utime": 20, "stime": 5}}},
        }
        self.assertEqual(cpu.calcular_cpu(anterior, actual), {1: 50.0})


class TestSistemaAnalyzer(unittest.TestCase):
    def test_porcentaje_zero(self):
        self.assertEqual(sistema.porcentaje(10, 0), 0.0)

    def test_analizar_con_top_cpu(self):
        snapshot = {
            "cpu": {"user": 100, "system": 50, "idle": 200, "iowait": 10},
            "memoria": {
                "MemTotal": 1000,
                "MemFree": 400,
                "MemAvailable": 500,
                "Buffers": 50,
                "Cached": 100,
                "SwapTotal": 200,
                "SwapFree": 180,
            },
            "loadavg": {"one": "0.10"},
            "uptime": 100,
            "boot_time": 1600000000,
            "procesos": {
                1: {
                    "stat": {"state": "R", "comm": "python"},
                    "status": {"VmRSS": "25 kB"},
                    "cmdline": "python script.py",
                    "usuario": "danat",
                }
            },
            "cpu_pct": {1: 42.0},
        }
        datos = sistema.analizar(snapshot, None)
        self.assertEqual(datos["mem_pct"], 60.0)
        self.assertEqual(datos["top_cpu"][0]["pid"], 1)
        self.assertEqual(datos["top_cpu"][0]["cpu_pct"], 42.0)
        self.assertEqual(datos["mem_available"], 500)
        self.assertEqual(datos["uptime"], 100)
        self.assertEqual(datos["top_mem"][0]["rss_kb"], 25)


class TestThreadsAnalyzer(unittest.TestCase):
    @patch("analizadores.threads.leer_threads", return_value=[{"tid": 1, "cpu": 5}, {"tid": 2, "cpu": 2}])
    def test_analizar_ordenes_por_cantidad(self, mock_leer_threads):
        snapshot = {
            "procesos": {
                1: {"stat": {"comm": "bash"}, "cmdline": "bash"}
            },
            "cpu_pct": {1: 1.0},
        }
        procesos, _ = threads.analizar(snapshot, {})
        self.assertEqual(procesos[0]["cantidad"], 2)


class TestMemoriaAnalyzer(unittest.TestCase):
    @patch("analizadores.memoria.resumir_segmentos", return_value={"heap": 12})
    def test_analizar_usa_kb_y_resumir_segmentos(self, mock_resumir):
        snapshot = {
            "procesos": {
                1: {
                    "stat": {"comm": "bash", "minflt": 5, "majflt": 2},
                    "status": {"VmRSS": "10 kB", "VmSize": "20 kB", "VmSwap": "0 kB"},
                    "cmdline": "bash",
                    "usuario": "root",
                }
            },
            "cpu_pct": {1: 0.0},
        }
        procesos = memoria.analizar(snapshot)
        self.assertEqual(procesos[0]["VmRSS"], "10 kB")
        self.assertEqual(procesos[0]["segmentos"], {"heap": 12})


class TestFdsAnalyzer(unittest.TestCase):
    def test_analizar_orden_por_fd(self):
        snapshot = {
            "procesos": {
                1: {"stat": {"comm": "bash"}, "cmdline": "bash", "fds": [{"fd": "0"}]},
                2: {"stat": {"comm": "sleep"}, "cmdline": "sleep", "fds": [{"fd": "0"}, {"fd": "1"}]},
            }
        }
        procesos = fds.analizar(snapshot)
        self.assertEqual(procesos[0]["pid"], 2)
        self.assertEqual(procesos[0]["cantidad_fds"], 2)


class TestSenalesAnalyzer(unittest.TestCase):
    def test_decodificar_mascara(self):
        self.assertEqual(anal_senales.decodificar_mascara("3"), ["SIGHUP", "SIGINT"])


class TestSchedulingAnalyzer(unittest.TestCase):
    def test_policy_name_known(self):
        self.assertEqual(scheduling.policy_name(2), "RR")

    def test_policy_name_unknown(self):
        self.assertEqual(scheduling.policy_name(99), "99")


class TestResumenAnalyzer(unittest.TestCase):
    @patch("analizadores.resumen.leer_threads", return_value=[{"cpu": 1}])
    def test_analizar_con_anterior(self, mock_leer_threads):
        anterior = {
            "procesos": {
                1: {"stat": {"utime": 5, "stime": 5}}
            }
        }
        snapshot = {
            "procesos": {
                1: {
                    "stat": {"utime": 10, "stime": 10, "state": "R"},
                    "status": {"PPid": "0", "Uid": "1000 1000 1000 1000", "Gid": "1000 1000 1000 1000"},
                    "cmdline": "bash",
                    "usuario": "root",
                }
            },
            "cpu_pct": {1: 5.0},
        }
        procesos = resumen.analizar(snapshot, anterior)
        self.assertEqual(procesos[0]["cpu_jiffies"], 10)
        self.assertEqual(procesos[0]["cpu_pct"], 5.0)


if __name__ == "__main__":
    unittest.main()