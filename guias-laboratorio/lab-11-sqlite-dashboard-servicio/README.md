# Lab 11 – SQLite, dashboard y servicio

## Propósito

Persistir y visualizar datos, ejecutar la aplicación automáticamente y recuperar operación tras una falla.

## Procedimiento

1. Diseñar tabla SQLite.
2. Insertar datos validados.
3. Consultar históricos.
4. Construir dashboard local.
5. Registrar eventos y errores.
6. Crear servicio `systemd`.
7. Reiniciar Raspberry Pi.
8. Verificar arranque automático.
9. Desconectar y reconectar el ESP32.

## Evidencia

Esquema de base, registros, dashboard, archivo de servicio, estado del servicio, logs y prueba de recuperación.

## Implementación guiada

[Guía de integración USB, SQLite y dashboard](../lab-10-uart-esp32-raspberry/integracion-usb-dashboard/README.md): receptor Python, SQLite, interfaz local, generador de servicio y evidencias. Incluye pasos explicados, ejemplos ejecutables y resultados esperados. El montaje debe comprobarse con el hardware real.

[Marco teórico de SQLite y dashboard](../lab-10-uart-esp32-raspberry/integracion-usb-dashboard/marco-teorico.md): conceptos, ejemplos de consultas y recorrido de los datos hasta la página.
