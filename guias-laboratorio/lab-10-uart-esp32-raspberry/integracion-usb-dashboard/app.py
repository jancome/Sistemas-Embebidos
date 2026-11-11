"""ESP32 por USB → validación → SQLite → dashboard local.

Ejecutar: python app.py
Abrir http://127.0.0.1:5000 en el navegador DE LA RASPBERRY.
El receptor y la página corren en una sola aplicación; no usar flask --debug.
"""
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
import csv
import io
import json
import logging
import math
import re
import sqlite3
import threading
import time

from flask import Flask, Response, jsonify, render_template
import serial
from serial.tools import list_ports

ROOT = Path(__file__).resolve().parent
LOG = logging.getLogger("integracion")
MAX_FRAME = 512  # Bytes por mensaje, incluida su terminación


def finite_number(value):
    try:
        return type(value) in (int, float) and math.isfinite(value)
    except OverflowError:
        return False


def load_config(path=ROOT / "config.json"):
    cfg = json.loads(path.read_text(encoding="utf-8"))
    for key in ("variable", "unidad"):
        if not isinstance(cfg.get(key), str) or not 1 <= len(cfg[key]) <= 40:
            raise ValueError(f"Configurar {key} con texto de 1 a 40 caracteres")
    if not isinstance(cfg.get("puerto"), str) or not cfg["puerto"]:
        raise ValueError("Configurar puerto como auto o una ruta de dispositivo")
    if type(cfg.get("baudrate")) is not int or cfg["baudrate"] <= 0:
        raise ValueError("baudrate debe ser entero positivo")
    timeout = cfg.get("sin_datos_s")
    if not finite_number(timeout) or timeout <= 0:
        raise ValueError("sin_datos_s debe ser finito y positivo")
    for key in ("minimo", "maximo", "umbral"):
        value = cfg.get(key)
        if value is not None and not finite_number(value):
            raise ValueError(f"{key} debe ser un número finito o null")
    if cfg.get("minimo") is not None and cfg.get("maximo") is not None:
        if cfg["minimo"] >= cfg["maximo"]:
            raise ValueError("minimo debe ser menor que maximo")
    return cfg


def validate_message(raw, cfg):
    """Trama: un objeto JSON UTF-8 por línea; no se acepta una lectura inventada."""
    if len(raw) > MAX_FRAME:
        raise ValueError("Trama demasiado larga")
    try:
        msg = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError) as exc:
        raise ValueError("Trama sin JSON UTF-8 válido") from exc
    if not isinstance(msg, dict):
        raise ValueError("El mensaje debe ser un objeto")
    required = {"nodo", "variable", "valor", "unidad", "secuencia", "estado"}
    if not required.issubset(msg):
        raise ValueError("Faltan campos del mensaje")
    if not isinstance(msg["nodo"], str) or not re.fullmatch(
        r"[A-Za-z0-9_-]{1,32}", msg["nodo"]
    ):
        raise ValueError("Identificador de nodo inválido")
    if msg["variable"] != cfg["variable"] or msg["unidad"] != cfg["unidad"]:
        raise ValueError("Variable o unidad no coincide con config.json")
    if type(msg["secuencia"]) is not int or not 0 <= msg["secuencia"] <= 4294967295:
        raise ValueError("Secuencia inválida")
    if msg["estado"] == "ERROR":
        if msg["valor"] is not None:
            raise ValueError("Un error de sensor debe tener valor null")
        msg["detalle"] = str(msg.get("detalle", "Fallo de lectura del sensor"))[:120]
        return msg
    if msg["estado"] != "OK":
        raise ValueError("Estado debe ser OK o ERROR")
    value = msg["valor"]
    if type(value) not in (int, float):
        raise ValueError("El valor debe ser numérico, no texto ni booleano")
    try:
        value = float(value)
    except OverflowError as exc:
        raise ValueError("Valor fuera de rango numérico") from exc
    if not math.isfinite(value):
        raise ValueError("Valor no finito")
    humidity = msg.get("humedad_pct")
    if humidity is not None and (not finite_number(humidity) or not 0 <= humidity <= 100):
        raise ValueError("Humedad inválida")
    volume = msg.get("volumen_l")
    if volume is not None and (not finite_number(volume) or volume < 0):
        raise ValueError("Volumen inválido")
    for key in ("pulsos", "periodo_ms"):
        value_extra = msg.get(key)
        if value_extra is not None and (
            type(value_extra) is not int or not 0 <= value_extra <= 4294967295
        ):
            raise ValueError(f"{key} inválido")
    if cfg["variable"] == "caudal":
        if volume is None or msg.get("pulsos") is None or not msg.get("periodo_ms"):
            raise ValueError("El ejemplo de caudal requiere volumen_l, pulsos y periodo_ms")
    if cfg.get("minimo") is not None and value < cfg["minimo"]:
        raise ValueError("Valor inferior al mínimo configurado")
    if cfg.get("maximo") is not None and value > cfg["maximo"]:
        raise ValueError("Valor superior al máximo configurado")
    msg["valor"] = value
    return msg


class LineFramer:
    """Conserva lecturas parciales; descarta una trama excesiva hasta el salto."""
    def __init__(self):
        self.buffer = bytearray()
        self.dropping = False

    def feed(self, data):
        frames = []
        discarded = 0
        for value in data:
            if self.dropping:
                if value == 10:
                    self.dropping = False
                continue
            self.buffer.append(value)
            if len(self.buffer) > MAX_FRAME:
                self.buffer.clear()
                self.dropping = value != 10
                discarded += 1
            elif value == 10:
                frame = bytes(self.buffer).strip()
                self.buffer.clear()
                if frame:
                    frames.append(frame)
        return frames, discarded


class Database:
    def __init__(self, path):
        self.path = str(path)
        with closing(self.connect()) as db, db:
            db.execute("PRAGMA journal_mode=WAL")
            db.execute("""
                CREATE TABLE IF NOT EXISTS mediciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha_hora TEXT NOT NULL,
                    nodo TEXT NOT NULL,
                    variable TEXT NOT NULL,
                    valor REAL NOT NULL,
                    unidad TEXT NOT NULL,
                    secuencia INTEGER NOT NULL,
                    estado TEXT NOT NULL,
                    umbral REAL,
                    pulsos INTEGER,
                    periodo_ms INTEGER,
                    volumen_l REAL,
                    humedad_pct REAL
                )
            """)
            db.execute("""
                CREATE TABLE IF NOT EXISTS eventos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha_hora TEXT NOT NULL,
                    tipo TEXT NOT NULL,
                    detalle TEXT NOT NULL
                )
            """)

    def connect(self):
        db = sqlite3.connect(self.path, timeout=10)
        db.row_factory = sqlite3.Row
        return db

    def insert(self, msg, cfg):
        threshold = cfg.get("umbral")
        status = "ALERTA" if threshold is not None and msg["valor"] >= threshold else "NORMAL"
        with closing(self.connect()) as db, db:
            db.execute(
                """INSERT INTO mediciones
                (fecha_hora,nodo,variable,valor,unidad,secuencia,estado,umbral,
                 pulsos,periodo_ms,volumen_l,humedad_pct)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
                 msg["nodo"], msg["variable"], msg["valor"], msg["unidad"],
                 msg["secuencia"], status, threshold, msg.get("pulsos"),
                 msg.get("periodo_ms"), msg.get("volumen_l"), msg.get("humedad_pct")),
            )

    def event(self, kind, detail):
        LOG.warning("%s: %s", kind, detail)
        with closing(self.connect()) as db, db:
            db.execute(
                "INSERT INTO eventos (fecha_hora,tipo,detalle) VALUES (?,?,?)",
                (datetime.now(timezone.utc).isoformat(timespec="seconds"), kind, detail),
            )

    def history(self, cfg, limit=120):
        with closing(self.connect()) as db:
            rows = db.execute(
                """SELECT * FROM mediciones WHERE variable=? AND unidad=?
                ORDER BY id DESC LIMIT ?""",
                (cfg["variable"], cfg["unidad"], limit),
            ).fetchall()
            count = db.execute(
                "SELECT COUNT(*) FROM mediciones WHERE variable=? AND unidad=?",
                (cfg["variable"], cfg["unidad"]),
            ).fetchone()[0]
        return [dict(row) for row in reversed(rows)], count

    def export_rows(self, cfg):
        # El generador mantiene abierta la conexión solo mientras se descarga.
        with closing(self.connect()) as db:
            cursor = db.execute(
                """SELECT * FROM mediciones WHERE variable=? AND unidad=?
                ORDER BY id""", (cfg["variable"], cfg["unidad"]),
            )
            yield [column[0] for column in cursor.description]
            for row in cursor:
                yield list(row)


class Runtime:
    def __init__(self, cfg, database):
        self.cfg, self.db = cfg, database
        self.lock = threading.Lock()
        self.stop = threading.Event()
        self.connected = False
        self.last_valid = None
        self.problem = None
        self.invalid = 0
        self.last_sequence = None
        self.last_node = None

    def process(self, frame):
        try:
            msg = validate_message(frame, self.cfg)
        except ValueError as exc:
            with self.lock:
                self.invalid += 1
            self.db.event("TRAMA_RECHAZADA", str(exc))
            return False
        if msg["estado"] == "ERROR":
            self.db.event("ERROR_SENSOR", msg["detalle"])
            with self.lock:
                self.problem = "El sensor informó un error de lectura"
            return False
        self.db.insert(msg, self.cfg)  # Confirmar persistencia antes de declarar dato nuevo
        if self.last_node == msg["nodo"] and self.last_sequence is not None:
            if msg["secuencia"] <= self.last_sequence:
                self.db.event("NUEVA_SECUENCIA", "Posible reinicio del ESP32 o trama repetida")
        self.last_node, self.last_sequence = msg["nodo"], msg["secuencia"]
        with self.lock:
            self.last_valid = time.monotonic()
            self.problem = None
        return True

    def port_name(self):
        if self.cfg["puerto"] != "auto":
            return self.cfg["puerto"]
        candidates = [port.device for port in list_ports.comports() if port.vid is not None]
        if len(candidates) != 1:
            raise serial.SerialException(
                f"Se encontraron {len(candidates)} puertos USB; indicar puerto en config.json"
            )
        return candidates[0]

    def collect(self):
        while not self.stop.is_set():
            try:
                name = self.port_name()
                with serial.Serial(name, self.cfg["baudrate"], timeout=0.5, exclusive=True) as port:
                    LOG.info("Puerto abierto: %s", name)
                    with self.lock:
                        self.connected = True
                    framer = LineFramer()
                    while not self.stop.is_set():
                        frames, discarded = framer.feed(port.read(128))
                        for _ in range(discarded):
                            with self.lock:
                                self.invalid += 1
                            self.db.event("TRAMA_RECHAZADA", "Trama demasiado larga")
                        for frame in frames:
                            self.process(frame)
            except (serial.SerialException, OSError) as exc:
                LOG.warning("USB no disponible: %s", exc)
            except sqlite3.Error:
                LOG.exception("No se pudo guardar o consultar SQLite")
                with self.lock:
                    self.problem = "Error de almacenamiento; revisar logs y espacio disponible"
            finally:
                with self.lock:
                    self.connected = False
            self.stop.wait(3)  # Reintentar sin bloquear el dashboard

    def snapshot(self):
        rows, count = self.db.history(self.cfg)
        with self.lock:
            age = None if self.last_valid is None else time.monotonic() - self.last_valid
            fresh = age is not None and age <= self.cfg["sin_datos_s"]
            if self.problem:
                state = "ERROR"
            elif not self.connected or not fresh:
                state = "SIN DATOS RECIENTES"
            else:
                state = rows[-1]["estado"] if rows else "SIN DATOS"
            return {
                "variable": self.cfg["variable"], "unidad": self.cfg["unidad"],
                "sin_datos_s": self.cfg["sin_datos_s"],
                "conexion": self.connected, "estado": state,
                "fresco": fresh and self.connected and not self.problem,
                "detalle": self.problem or "",
                "rechazadas": self.invalid, "total": count,
                "ultima": rows[-1] if rows else None, "historial": rows,
            }


def create_app(runtime):
    app = Flask(__name__)

    @app.get("/")
    def index():
        return render_template("dashboard.html")

    @app.get("/api/estado")
    def state():
        try:
            response = jsonify(runtime.snapshot())
            response.headers["Cache-Control"] = "no-store"
            return response
        except sqlite3.Error:
            LOG.exception("Consulta de base de datos fallida")
            return jsonify(error="No se pudo consultar el histórico"), 503

    @app.get("/descargar.csv")
    def download():
        def generate():
            buffer = io.StringIO()
            writer = csv.writer(buffer)
            for row in runtime.db.export_rows(runtime.cfg):
                writer.writerow(row)
                yield buffer.getvalue()
                buffer.seek(0)
                buffer.truncate(0)
        return Response(generate(), mimetype="text/csv",
                        headers={"Content-Disposition": "attachment; filename=mediciones.csv"})

    return app


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    config = load_config()
    database = Database(ROOT / "mediciones.sqlite3")
    runtime = Runtime(config, database)
    worker = threading.Thread(target=runtime.collect, daemon=True)
    worker.start()
    try:
        create_app(runtime).run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
    finally:
        runtime.stop.set()
        worker.join(timeout=5)
