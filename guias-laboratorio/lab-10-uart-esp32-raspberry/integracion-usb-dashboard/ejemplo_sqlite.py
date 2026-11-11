"""Ejemplo de SQLite con datos ilustrativos, separado del sensor real.

Guardar este archivo y ejecutar con Python en la Raspberry.
Cada ejecución añade una fila a ejemplo.sqlite3.
"""
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
import sqlite3

ARCHIVO = Path(__file__).resolve().parent / "ejemplo.sqlite3"

with closing(sqlite3.connect(ARCHIVO)) as db:
    # Crear la tabla no borra una tabla existente con este nombre.
    db.execute("""
        CREATE TABLE IF NOT EXISTS ejemplo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_hora TEXT NOT NULL,
            valor REAL NOT NULL,
            unidad TEXT NOT NULL
        )
    """)
    fecha = datetime.now(timezone.utc).isoformat(timespec="seconds")
    db.execute(
        "INSERT INTO ejemplo (fecha_hora, valor, unidad) VALUES (?, ?, ?)",
        (fecha, 25.4, "C"),  # Valor ilustrativo; no proviene de un sensor
    )
    db.commit()  # Confirmar la inserción

    filas = db.execute(
        "SELECT id, fecha_hora, valor, unidad FROM ejemplo ORDER BY id DESC LIMIT 5"
    ).fetchall()
    for fila in filas:
        print(fila)

print("Archivo de aprendizaje:", ARCHIVO)
print("Los datos son ilustrativos; no se añadieron a mediciones.sqlite3.")
