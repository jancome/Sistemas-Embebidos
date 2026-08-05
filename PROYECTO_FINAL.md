# Proyecto final – Sistema embebido distribuido

## Producto esperado

Un prototipo funcional que integre:

```text
Sensor / variable física
        ↓
Placa base con ESP32
        ↓
Firmware modular + FreeRTOS
        ↓
UART / Wi-Fi / HTTP / MQTT
        ↓
Raspberry Pi 4
        ↓
Procesamiento + SQLite + dashboard
        ↓
Registro, control y recuperación ante fallas
```

## Entregables finales

1. Prototipo físico organizado y seguro.
2. PCB o placa base fabricada o validada, según alcance acordado.
3. Repositorio de firmware del ESP32.
4. Repositorio o carpeta de aplicación Python.
5. Diagrama de arquitectura y conexiones.
6. BOM final y costos.
7. Evidencias de comunicación.
8. Base de datos con registros.
9. Dashboard o interfaz.
10. Servicio de inicio automático.
11. Logs y prueba de recuperación.
12. Informe técnico.
13. Video de funcionamiento.
14. Sustentación y demostración en vivo.

## Pruebas mínimas

- Encendido y arranque completo.
- Adquisición de sensor.
- Activación segura del actuador o indicador.
- Comunicación durante operación normal.
- Validación de una trama incorrecta.
- Pérdida temporal de comunicación.
- Reconexión automática.
- Reinicio de la Raspberry Pi.
- Inicio automático de la aplicación.
- Consulta de datos históricos.

## Criterios técnicos

| Criterio | Evidencia |
|---|---|
| Diseño electrónico | Esquemático, PCB, cálculos y protecciones |
| Firmware | Modularidad, driver, concurrencia y manejo de errores |
| Comunicaciones | Tramas, protocolo, pruebas y reconexión |
| Raspberry Pi | Linux, Python, GPIO, servicio y logs |
| Datos | Validación, SQLite y visualización |
| Integración | Funcionamiento continuo y recuperación |
| Sustentación | Dominio individual y decisiones justificadas |

## Restricciones

- No usar tensión de red directamente en protoboard.
- No conectar cargas de potencia a GPIO.
- Usar tierra común cuando corresponda y aislamiento cuando sea necesario.
- Verificar niveles lógicos antes de conectar UART, SPI o GPIO.
- Mantener copias del código y de la base de datos.
