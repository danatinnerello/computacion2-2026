import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import senales


class TestSenales(unittest.TestCase):
    def setUp(self):
        senales.reset_state()
        senales.setup_signal_pipe()

    def test_consume_signal_events(self):
        os.write(senales._signal_pipe_w, b"SIGUSR1\n")
        eventos = senales.consume_signal_events()
        self.assertEqual(eventos, ["SIGUSR1"])

    def test_apply_signal_event_toggle_verbose(self):
        senales.apply_signal_event("SIGUSR2")
        self.assertTrue(senales.verbose)

    def test_setup_signal_pipe_is_non_blocking(self):
        senales.setup_signal_pipe()
        self.assertFalse(os.get_blocking(senales._signal_pipe_r))
        self.assertFalse(os.get_blocking(senales._signal_pipe_w))


class TestSenalesExtra(unittest.TestCase):
    def setUp(self):
        senales.reset_state()
        senales.setup_signal_pipe()

    def test_apply_signal_event_dump_reload_shutdown(self):
        senales.apply_signal_event("SIGUSR1")
        self.assertTrue(senales.dump_requested)
        senales.apply_signal_event("SIGHUP")
        self.assertTrue(senales.reload_requested)
        senales.apply_signal_event("SIGWINCH")
        self.assertTrue(senales.resize_requested)
        senales.apply_signal_event("SIGINT")
        self.assertTrue(senales.shutdown)

    def test_consume_signal_events_vacio(self):
        self.assertEqual(senales.consume_signal_events(), [])


    def test_reset_state_resetea_variables(self):
        senales.dump_requested = True
        senales.reload_requested = True
        senales.reset_state()
        self.assertFalse(senales.dump_requested)
        self.assertFalse(senales.reload_requested)

if __name__ == "__main__":
    unittest.main()
