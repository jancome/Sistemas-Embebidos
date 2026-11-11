"""Consultar el histórico real; no crea una base vacía si se equivocó la carpeta."""
from contextlib import closing
from pathlib import Path
import sqlite3

ARCHIVO = Path(__file__).resolve().parent / "mediciones.sqlite3"

if not ARCHIVO.exists():
    raise SystemExit("Primero ejecutar app.py y recibir lecturas válidas del ESP32.")

with closing(sqlite3.connect(ARCHIVO)) as db:
    db.row_factory = sqlite3.Row
    cantidad = db.execute("SELECT COUNT(*) FROM mediciones").fetchone()[0]
    print("Mediciones guardadas:", cantidad)
    filas = db.execute("""
        SELECT id, fecha_hora, nodo, valor, unidad, estado, humedad_pct
        FROM mediciones
        ORDER BY id DESC
        LIMIT 5
    """).fetchall()
    for fila in filas:
        print(dict(fila))
    print("\nÚltimos eventos:")
    for fila in db.execute(
        "SELECT fecha_hora, tipo, detalle FROM eventos ORDER BY id DESC LIMIT 5"
    ):
        print(dict(fila))
