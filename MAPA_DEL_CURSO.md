# Mapa del curso

## Arquitectura general

```text
Variable física
      ↓
Sensor y acondicionamiento
      ↓
ESP32 + placa base
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

## Fase 1 – Diseñar el nodo electrónico

El grupo formula una necesidad real, establece requerimientos, selecciona sensores y actuadores, calcula alimentación y protecciones, diseña el esquemático y PCB y genera la documentación de fabricación.

**Evidencias:** arquitectura, cálculos, esquemático, PCB, DRC, vistas 2D/3D, Gerber, BOM y cotización.

## Fase 2 – Construir el firmware y las comunicaciones

El grupo implementa firmware por capas, desarrolla al menos un driver a partir de datasheet, integra un periférico SPI, incorpora conectividad y organiza tareas concurrentes mediante FreeRTOS.

**Evidencias:** código modular, driver, pruebas, capturas del analizador lógico o monitor serial, tiempos, manejo de errores y demostración funcional.

## Fase 3 – Integrar la Raspberry Pi 4

La Raspberry Pi 4 recibe datos del ESP32, los valida, procesa, almacena y visualiza. La aplicación se ejecuta como servicio, registra eventos y se recupera de interrupciones de comunicación.

**Evidencias:** Raspberry Pi OS configurado, acceso SSH, Python, GPIO, comunicación, SQLite, dashboard, servicio, logs y pruebas de recuperación.

## Regla de diseño

Cada bloque debe tener:

1. Una función definida.
2. Una interfaz eléctrica o de software conocida.
3. Una prueba verificable.
4. Una evidencia medible.
5. Un responsable dentro del equipo.
