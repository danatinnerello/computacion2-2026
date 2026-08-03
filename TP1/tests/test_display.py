import sys
from pathlib import Path
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import display


class TestDisplay(unittest.TestCase):
    def test_filtrar_y_ordenar_por_usuario_y_cpu(self):
        datos = [
            {"pid": 2, "cpu_pct": 10.0, "comando": "python", "VmRSS": "20 kB"},
            {"pid": 1, "cpu_pct": 30.0, "comando": "bash", "VmRSS": "30 kB"},
        ]
        snapshot = {
            "snapshot": {
                "procesos": {
                    1: {"usuario": "danat"},
                    2: {"usuario": "root"},
                }
            }
        }
        estado = {"filtro": "", "filtro_usuario": "danat", "orden": "cpu"}
        resultado = display.filtrar_y_ordenar(datos, estado, snapshot)
        self.assertEqual([p["pid"] for p in resultado], [1])

    def test_toggle_order_uses_pid_when_requested(self):
        datos = [
            {"pid": 20, "cpu_pct": 10.0, "comando": "python", "VmRSS": "20 kB"},
            {"pid": 5, "cpu_pct": 30.0, "comando": "bash", "VmRSS": "30 kB"},
        ]
        estado = {"filtro": "", "filtro_usuario": "", "orden": "pid"}
        resultado = display.filtrar_y_ordenar(datos, estado, {})
        self.assertEqual([p["pid"] for p in resultado], [5, 20])

    def test_enter_pins_selected_pid(self):
        estado = {"selected_index": 1, "selected_pid": 42, "pinned_pid": None, "mensaje": ""}
        display.procesar_tecla(10, estado, {}, None)
        self.assertEqual(estado["pinned_pid"], 42)
        self.assertIn("Pin", estado["mensaje"])

    def test_procesar_tecla_with_string_input_changes_view(self):
        estado = {"vista": "sistema", "mensaje": "", "selected_index": 0, "salir": False, "needs_refresh": False}
        display.procesar_tecla("1", estado, {}, None)
        self.assertEqual(estado["vista"], "resumen")
        self.assertTrue(estado["needs_refresh"])

    @patch("display.curses", None)
    @patch("display.run_fallback_loop")
    def test_run_display_without_curses_exits_cleanly(self, mock_fallback):
        snapshot = {"sistema": {"datos": []}}
        intervalos = {"sistema": 1}
        display.run_display(snapshot, intervalos)
        mock_fallback.assert_called_once()

    @patch("display.curses")
    def test_run_display_propagates_curses_wrapper_error(self, mock_curses):
        snapshot = {"sistema": {"datos": []}}
        intervalos = {"sistema": 1}
        mock_curses.wrapper.side_effect = RuntimeError("curses failed")

        with patch("display.run_fallback_loop") as fallback:
            with self.assertRaises(RuntimeError):
                display.run_display(snapshot, intervalos)
            fallback.assert_not_called()

class TestDisplayExtra(unittest.TestCase):
    def test_parse_kb_invalid_devuelve_0(self):
        self.assertEqual(display.parse_kb("abc"), 0)
        self.assertEqual(display.parse_kb(None), 0)
        self.assertEqual(display.parse_kb(""), 0)

    @patch("display.curses", None)
    def test_procesar_tecla_plus_minus(self):
        from shared import IntervalStore

        estado = {"vista": "resumen", "orden": "pid", "intervalo": 2, "mensaje": "", "needs_refresh": False}
        intervalos = IntervalStore({"resumen": 2})
        display.procesar_tecla("+", estado, intervalos, None)
        self.assertEqual(estado["intervalo"], 1.5)
        display.procesar_tecla("-", estado, intervalos, None)
        self.assertEqual(estado["intervalo"], 2)

    @patch("display.curses", None)
    def test_procesar_tecla_help(self):
        estado = {"mensaje": "", "needs_refresh": False}
        display.procesar_tecla("h", estado, {}, None)
        self.assertIn("Ayuda", estado["mensaje"])

    def test_procesar_tecla_quit(self):
        estado = {"salir": True}
        display.procesar_tecla(ord("q"), estado, {}, None)
        self.assertTrue(estado["salir"])
        self.assertTrue(display.senales.shutdown)

    def test_procesar_tecla_escape(self):
        estado = {"salir": False}
        display.procesar_tecla(27, estado, {}, None)
        self.assertTrue(estado["salir"])

    def test_procesar_tecla_order_cycle(self):
        estado = {"orden": "pid", "mensaje": "", "needs_refresh": False}
        display.procesar_tecla("c", estado, {}, None)
        self.assertEqual(estado["orden"], "cpu")
        display.procesar_tecla("c", estado, {}, None)
        self.assertEqual(estado["orden"], "rss")

    def test_procesar_tecla_clear_filters(self):
        estado = {"filtro": "a", "filtro_usuario": "b", "mensaje": "", "needs_refresh": False}
        display.procesar_tecla("x", estado, {}, None)
        self.assertEqual(estado["filtro"], "")
        self.assertEqual(estado["filtro_usuario"], "")

    @patch("display.pedir_texto", return_value="python")
    @patch("display.curses", None)
    def test_procesar_tecla_filter_command(self, mock_pedir_texto):
        estado = {"filtro": "", "mensaje": "", "needs_refresh": False}
        display.procesar_tecla("/", estado, {}, None)
        self.assertEqual(estado["filtro"], "python")
        self.assertIn("Filtro comando", estado["mensaje"])

    @patch("display.pedir_texto", return_value="danat")
    @patch("display.curses", None)
    def test_procesar_tecla_filter_usuario(self, mock_pedir_texto):
        estado = {"filtro_usuario": "", "mensaje": "", "needs_refresh": False}
        display.procesar_tecla("u", estado, {}, None)
        self.assertEqual(estado["filtro_usuario"], "danat")
        self.assertIn("Filtro usuario", estado["mensaje"])

    def test_format_row_resumen(self):
        fila = display.format_row({"pid": 1, "usuario": "u", "ppid": 0, "estado": "R", "threads": 1, "cpu_pct": 0.0, "comando": "bash"}, "resumen")
        self.assertIn("bash", fila)

if __name__ == "__main__":
    unittest.main()
