"""Pruebas de software con datos identificados como prueba.
No utiliza un sensor físico ni escribe en la base de operación.
Ejecutar: python verificar_software.py
"""
from pathlib import Path
from contextlib import closing
import copy
import csv
import io
import json
import os
import tempfile
import threading
import time
import tty
import unittest

from app import Database, LineFramer, Runtime, create_app, load_config, validate_message


def packet(seq=1, value=25.4):
    return json.dumps({
        "nodo": "prueba-01", "variable": "temperatura",
        "valor": value, "unidad": "C", "secuencia": seq,
        "estado": "OK", "humedad_pct": 61.2,
    }).encode()


class SoftwareTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.cfg = load_config()
        self.database = Database(Path(self.tmp.name) / "prueba.sqlite3")
        self.runtime = Runtime(self.cfg, self.database)

    def test_validacion_y_persistencia(self):
        self.assertTrue(self.runtime.process(packet()))
        for value in [True, "25.4", float("nan"), float("inf"), 100]:
            self.assertFalse(self.runtime.process(packet(2, value)))
        self.assertFalse(self.runtime.process(b'{"valor":"incompleto"}'))
        rows, count = self.database.history(self.cfg)
        self.assertEqual(count, 1)
        self.assertEqual(rows[-1]["humedad_pct"], 61.2)
        self.assertEqual(self.runtime.invalid, 6)
        bad_extra = json.loads(packet())
        bad_extra["humedad_pct"] = int("9" * 310)
        self.assertFalse(self.runtime.process(json.dumps(bad_extra).encode()))
        reopened = Database(self.database.path)
        self.assertEqual(reopened.history(self.cfg)[1], 1)

    def test_estado_fresco_alerta_error_y_antiguo(self):
        self.runtime.connected = True
        self.runtime.process(packet())
        self.assertEqual(self.runtime.snapshot()["estado"], "NORMAL")
        self.cfg["umbral"] = 20
        self.runtime.process(packet(2))
        self.assertEqual(self.runtime.snapshot()["estado"], "ALERTA")
        error = json.loads(packet())
        error.update(estado="ERROR", valor=None, detalle="Fallo inducido")
        self.runtime.process(json.dumps(error).encode())
        self.assertEqual(self.runtime.snapshot()["estado"], "ERROR")
        self.assertEqual(self.database.history(self.cfg)[1], 2)
        self.runtime.process(packet(3))
        self.runtime.last_valid -= 20
        self.assertEqual(self.runtime.snapshot()["estado"], "SIN DATOS RECIENTES")
        restarted = Runtime(self.cfg, self.database)
        self.assertFalse(restarted.snapshot()["fresco"])

    def test_tramas_parciales_y_excesivas(self):
        framer = LineFramer()
        part = packet()
        self.assertEqual(framer.feed(part[:12]), ([], 0))
        self.assertEqual(framer.feed(part[12:] + b"\n")[0], [part])
        frames, rejected = framer.feed(b"x" * 600 + b"\n" + part + b"\n")
        self.assertEqual(rejected, 1)
        self.assertEqual(frames, [part])

    def test_dashboard_api_y_exportacion(self):
        self.runtime.process(packet())
        client = create_app(self.runtime).test_client()
        self.assertEqual(client.get("/").status_code, 200)
        data = client.get("/api/estado").get_json()
        self.assertEqual(data["total"], 1)
        self.assertEqual(data["ultima"]["valor"], 25.4)
        rows = list(csv.DictReader(io.StringIO(client.get("/descargar.csv").text)))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["nodo"], "prueba-01")

    @unittest.skipUnless(os.name == "posix", "Requiere pseudo-terminal POSIX")
    def test_usb_simulado_desconexion_y_reconexion(self):
        import pty
        link = Path(self.tmp.name) / "usb_prueba"
        masters = []
        slaves = []
        def make_port():
            master, slave = pty.openpty()
            masters.append(master)
            slaves.append(slave)
            tty.setraw(slave)
            if link.is_symlink():
                link.unlink()
            link.symlink_to(os.ttyname(slave))
            return master

        def wait_for(condition, seconds=8):
            deadline = time.monotonic() + seconds
            while time.monotonic() < deadline:
                if condition():
                    return
                time.sleep(.05)
            self.fail("No llegó al estado esperado")

        first = make_port()
        cfg = copy.deepcopy(self.cfg)
        cfg["puerto"] = str(link)
        runtime = Runtime(cfg, self.database)
        worker = threading.Thread(target=runtime.collect, daemon=True)
        worker.start()
        try:
            wait_for(lambda: runtime.connected)
            os.write(first, packet() + b"\n")
            wait_for(lambda: self.database.history(cfg)[1] == 1)
            os.close(first)
            masters.remove(first)
            wait_for(lambda: not runtime.connected)
            second = make_port()
            wait_for(lambda: runtime.connected)
            os.write(second, packet(2, 26.0) + b"\n")
            wait_for(lambda: self.database.history(cfg)[1] == 2)
            self.assertEqual(self.database.history(cfg)[0][-1]["valor"], 26.0)
        finally:
            runtime.stop.set()
            worker.join(timeout=5)
            for fd in masters + slaves:
                os.close(fd)


if __name__ == "__main__":
    unittest.main(verbosity=2)
