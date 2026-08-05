# Mapa del curso

## Progresión de plataformas

```text
CORTE 1 – EasyEDA
Arquitectura + esquemático + PCB de la placa base ESP32
                      ↓
CORTE 2 – ESP32
Firmware modular + drivers + SPI + Wi-Fi/BLE + HTTP/MQTT + FreeRTOS
                      ↓
CORTE 3 – Raspberry Pi 4
Linux + SSH + Python + GPIO + comunicación + SQLite + dashboard + servicio
```

## Arquitectura general del proyecto

```text
Variable física
      ↓
Sensor y acondicionamiento
      ↓
Placa base diseñada en EasyEDA
      ↓
ESP32
      ↓
Firmware modular + drivers + FreeRTOS
      ↓
UART / Wi-Fi / HTTP / MQTT
      ↓
Raspberry Pi 4 + Linux
      ↓
Procesamiento + SQLite + dashboard
      ↓
Decisión, registro y operación robusta
```

## Fase 1 – EasyEDA: diseñar la placa base

El grupo formula una necesidad real, establece requerimientos, selecciona sensores y actuadores, calcula alimentación y protecciones y diseña en EasyEDA el esquemático y PCB de una placa base para ESP32.

**Evidencias:** arquitectura, cálculos, esquemático, footprints, PCB, DRC, vistas 2D/3D, Gerber, BOM y cotización.

## Fase 2 – ESP32: desarrollar firmware y comunicaciones

El grupo programa el nodo ESP32, implementa firmware por capas, desarrolla al menos un driver a partir de datasheet, integra un periférico SPI, realiza experiencias con Wi-Fi y Bluetooth/BLE, comunica datos mediante HTTP o MQTT y organiza tareas mediante FreeRTOS.

**Evidencias:** código modular, driver, pruebas, transacciones, comunicaciones, tiempos, manejo de errores y demostración funcional.

## Fase 3 – Raspberry Pi 4: implementar el computador de borde

La Raspberry Pi 4 recibe datos del ESP32, los valida, procesa, almacena y visualiza. La aplicación se ejecuta como servicio, registra eventos y se recupera de interrupciones de comunicación.

**Evidencias:** Raspberry Pi OS configurado, acceso SSH, Python, GPIO, comunicación ESP32–Raspberry Pi 4, SQLite, dashboard, servicio, logs y pruebas de recuperación.

## Regla de diseño

Cada bloque debe tener:

1. Una función definida.
2. Una interfaz eléctrica o de software conocida.
3. Una prueba verificable.
4. Una evidencia medible.
5. Un responsable dentro del equipo.
