"""Consultas de aprendizaje sobre los datos reales, sin modificar la base."""
from contextlib import closing  # Cierra la conexión al terminar
from pathlib import Path  # Localiza la base junto a este programa
import sqlite3  # Acceso a SQLite desde Python

ARCHIVO = Path(__file__).resolve().parent / "mediciones.sqlite3"
VARIABLE = "temperatura"  # Debe corresponder a los datos de la práctica
UNIDAD = "C"  # Evita mezclar magnitudes o unidades al resumir

# Cada ejemplo contiene título, instrucción SQL y parámetros.
CONSULTAS = [
    (
        "1. Últimas cinco lecturas",
        """SELECT id, fecha_hora, nodo, valor, unidad, estado
           FROM mediciones
           WHERE variable = ? AND unidad = ?
           ORDER BY id DESC LIMIT 5""",
        (VARIABLE, UNIDAD),
    ),
    (
        "2. Cantidad de mediciones guardadas",
        """SELECT COUNT(*) AS cantidad FROM mediciones
           WHERE variable = ? AND unidad = ?""",
        (VARIABLE, UNIDAD),
    ),
    (
        "3. Últimas cinco alertas guardadas",
        """SELECT id, fecha_hora, nodo, valor, unidad, umbral
           FROM mediciones
           WHERE variable = ? AND unidad = ? AND estado = 'ALERTA'
           ORDER BY id DESC LIMIT 5""",
        (VARIABLE, UNIDAD),
    ),
    (
        "4. Cantidad y resumen por nodo",
        """SELECT nodo, COUNT(*) AS cantidad,
                  MIN(valor) AS minimo, ROUND(AVG(valor), 2) AS promedio,
                  MAX(valor) AS maximo
           FROM mediciones
           WHERE variable = ? AND unidad = ?
           GROUP BY nodo ORDER BY nodo""",
        (VARIABLE, UNIDAD),
    ),
    (
        "5. Mediciones sin umbral configurado",
        """SELECT COUNT(*) AS sin_umbral FROM mediciones
           WHERE variable = ? AND unidad = ? AND umbral IS NULL""",
        (VARIABLE, UNIDAD),
    ),
    (
        "6. Últimos cinco eventos de operación",
        """SELECT id, fecha_hora, tipo, detalle
           FROM eventos ORDER BY id DESC LIMIT 5""",
        (),
    ),
]


def main():
    if not ARCHIVO.is_file():
        raise SystemExit(
            "No existe mediciones.sqlite3 junto a este archivo. "
            "Ejecuta primero app.py para crearla y recibir datos."
        )

    # mode=ro abre en solo lectura y evita crear un archivo por error.
    direccion = ARCHIVO.as_uri() + "?mode=ro"
    with closing(sqlite3.connect(direccion, uri=True)) as db:
        db.row_factory = sqlite3.Row  # Permite identificar columnas por su nombre
        print("Base consultada:", ARCHIVO)
        print("Selección:", VARIABLE, "| Unidad:", UNIDAD)
        print("Se muestran datos recibidos; no se insertan valores de ejemplo.")

        for titulo, sql, parametros in CONSULTAS:
            print("\n" + titulo)
            print(sql)
            print("Parámetros:", parametros)
            filas = db.execute(sql, parametros).fetchall()
            if not filas:
                print("Sin filas para esta consulta.")
            for fila in filas:
                print(dict(fila))


if __name__ == "__main__":
    try:
        main()
    except sqlite3.Error as error:
        raise SystemExit(
            f"No se pudo consultar la base: {error}. "
            "Comprueba que pertenece a esta aplicación."
        )
