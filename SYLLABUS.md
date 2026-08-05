# Syllabus resumido – Sistemas Embebidos

## Identificación

- Programa: Ingeniería Electrónica.
- Área de formación: Sistemas Digitales.
- Prerrequisito: Sistemas Microcontrolados.
- Créditos: 3.
- Trabajo presencial: 48 horas.
- Trabajo independiente: 96 horas.
- Total: 144 horas.

## Gran pregunta

> **¿Cómo desarrollar aplicaciones basadas en sistemas embebidos?**

## Propósito del curso

Diseñar soluciones electrónicas programables para problemas reales mediante un nodo basado en microcontrolador y un computador de placa única como computador de borde. El estudiante recorrerá el ciclo de requerimientos, electrónica, PCB, firmware, comunicaciones, Linux, procesamiento, almacenamiento, visualización y operación robusta.

## Unidad 1 – Arquitectura y diseño de la placa base

**Resultado:** diseña la arquitectura y PCB de un nodo embebido, justificando sensores, actuadores, alimentación, regulación y protecciones; genera esquemático, PCB, Gerber, BOM y cotización.

Contenidos:

1. Problemática y requerimientos del proyecto ABP.
2. Arquitectura del sistema embebido.
3. Selección de sensores y actuadores.
4. Alimentación, regulación y protecciones.
5. Diseño esquemático.
6. Diseño de PCB, footprints y DRC.
7. Gerber, BOM y cotización.
8. Placa base con microcontrolador.
9. Preproyecto ABP 1.

## Unidad 2 – Firmware, drivers y comunicaciones

**Resultado:** implementa firmware modular con drivers propios, RTOS y comunicaciones cableadas e inalámbricas para el intercambio de datos del proyecto.

Contenidos:

1. Programación modular en C/C++ y firmware por capas.
2. Datasheets y drivers propios.
3. SPI e integración de periféricos.
4. Wi-Fi y Bluetooth/BLE.
5. HTTP o MQTT.
6. FreeRTOS: tareas, colas y sincronización.
7. Preproyecto ABP 2.

## Unidad 3 – Integración de microcontrolador y SBC

**Resultado:** integra el nodo con una Raspberry Pi 4 como computador de borde para recibir, procesar, almacenar y visualizar datos, manteniendo operación robusta ante fallas.

Contenidos:

1. Microcontrolador frente a SBC.
2. Raspberry Pi OS y fundamentos de Linux.
3. Red y SSH.
4. Python de alto nivel.
5. GPIO de la Raspberry Pi.
6. Comunicación ESP32–Raspberry Pi por UART, Wi-Fi, HTTP o MQTT.
7. Recepción y procesamiento de datos.
8. Base de datos local.
9. Dashboard o interfaz web.
10. Ejecución como servicio.
11. Registro de eventos y recuperación ante fallas.
12. Integración y sustentación final.

## Competencias técnicas prioritarias

- Especificar, analizar, diseñar y modelar prototipos embebidos.
- Construir algoritmos y programas de ingeniería.
- Consultar datasheets y documentación técnica.
- Medir, probar, depurar y justificar decisiones electrónicas.
- Integrar hardware, firmware, comunicaciones y software sobre Linux.
