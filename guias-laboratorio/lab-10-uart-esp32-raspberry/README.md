# Lab 10 – Comunicación entre microcontrolador y Raspberry Pi 4

## Propósito

Implementar y verificar una alternativa de comunicación entre el nodo basado en microcontrolador y el SBC.

## Alternativas del syllabus

- UART.
- Wi-Fi.
- HTTP.
- MQTT.

## Procedimiento general

1. Seleccionar la alternativa según los requerimientos.
2. Verificar niveles eléctricos cuando exista conexión física.
3. Definir formato y campos de datos.
4. Establecer timeout y validación.
5. Enviar datos desde el microcontrolador.
6. Recibir y procesar en la Raspberry Pi.
7. Probar un dato inválido o una interrupción.
8. Documentar la recuperación.

## Requisito adicional para UART

Cuando se utilice UART se deben verificar TX, RX, GND, tensión lógica, baud rate y formato de trama.

## Evidencia

Diagrama, selección justificada, especificación del mensaje, código o configuración, datos válidos e inválidos y prueba de recuperación.
