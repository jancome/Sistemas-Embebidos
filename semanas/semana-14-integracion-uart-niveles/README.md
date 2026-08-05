# Semana 14 – Integración ESP32–Raspberry Pi por UART

**Fecha:** 4 de noviembre de 2026 · **Fase 3**

## Pregunta guía

¿Cómo transportar datos entre dos plataformas sin perder integridad ni dañar sus entradas?

## Resultados

- Verificar niveles lógicos y tierra común.
- Configurar velocidad, bits y puerto serial.
- Diseñar una trama con delimitación y validación.
- Detectar desconexión o datos inválidos.

## Contenidos

- UART TX/RX.
- Lógica de 3,3 V.
- Tierra común y conversores de nivel.
- Baud rate y formato.
- Tramas de texto o binarias.
- Checksum, CRC o validación de campos.
- Lectura no bloqueante.

## Laboratorio

Transmitir desde ESP32 una trama con identificación, secuencia, variable y estado. La Raspberry Pi debe validar, mostrar y rechazar una trama incorrecta.

## Evidencia ABP

- Diagrama de conexión.
- Especificación de trama.
- Captura de datos válidos e inválidos.
- Estrategia de timeout.
