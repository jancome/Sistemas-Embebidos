"""Demostración docente: temperatura real CPU → validación → CSV.
Raspberry Pi OS; biblioteca estándar. Los umbrales son didácticos.
Ejecutar con python3 monitor_temperatura.py; finalizar con Ctrl+C.
"""
from pathlib import Path  # Acceso a rutas y archivos
from datetime import datetime  # Fecha y hora
import csv  # Registro tabular
import math  # Validación de números finitos
import time  # Pausa entre lecturas

RUTA_SENSOR = Path("/sys/class/thermal/thermal_zone0/temp")
INTERVALO_S = 2.0  # Intervalo aproximado: lectura/escritura añaden tiempo
UMBRAL_C = 55.0  # No representa temperatura de daño ni controla el ventilador
ARCHIVO_CSV = Path(__file__).resolve().parent / "temperatura.csv"


def leer_temperatura():
    texto = RUTA_SENSOR.read_text().strip()  # Lectura Linux en milésimas de °C
    temperatura = float(texto) / 1000  # Conversión a °C
    # Rango amplio de plausibilidad; NO es un rango seguro de operación.
    if not math.isfinite(temperatura) or not -40 <= temperatura <= 150:
        raise ValueError("Temperatura fuera del rango de validación")
    return temperatura


def main():
    if not math.isfinite(INTERVALO_S) or INTERVALO_S <= 0:
        raise ValueError("INTERVALO_S debe ser finito y mayor que cero")
    if not math.isfinite(UMBRAL_C):
        raise ValueError("UMBRAL_C debe ser finito")

    nuevo = not ARCHIVO_CSV.exists() or ARCHIVO_CSV.stat().st_size == 0
    # Append conserva el registro; with cierra el archivo al salir.
    with ARCHIVO_CSV.open("a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        if nuevo:
            escritor.writerow([
                "fecha_hora", "temperatura_c", "umbral_c", "estado", "detalle"
            ])
        print(f"Archivo: {ARCHIVO_CSV}")
        print("Ctrl+C para finalizar.")

        while True:
            fecha = datetime.now().astimezone().isoformat(timespec="seconds")
            try:
                temperatura = leer_temperatura()
                estado = "ALERTA" if temperatura >= UMBRAL_C else "NORMAL"
                valor, detalle = f"{temperatura:.2f}", ""
            except (OSError, ValueError) as error:
                # Error de adquisición: no inventar un cero ni reutilizar otro dato.
                valor, estado, detalle = "", "ERROR", str(error)

            # Escritura fuera del try anterior: fallo de disco no es fallo del sensor.
            escritor.writerow([fecha, valor, UMBRAL_C, estado, detalle])
            archivo.flush()  # No garantiza protección ante corte de corriente
            print(f"{fecha} | {valor or 'Sin lectura'} °C | {estado} | {detalle}")
            time.sleep(INTERVALO_S)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nMedición detenida.")
    except OSError as error:
        raise SystemExit(f"No se pudo abrir o escribir el CSV: {error}")
    except ValueError as error:
        raise SystemExit(f"Configuración inválida: {error}")
