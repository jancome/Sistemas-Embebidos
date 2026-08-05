# Proyecto de curso – Aprendizaje Basado en Proyectos

## Gran pregunta institucional

> **¿Cómo desarrollar aplicaciones basadas en sistemas embebidos?**

## Situación aplicada del curso

> **¿Cómo desarrollar una aplicación basada en sistemas embebidos que integre un nodo con microcontrolador y una Raspberry Pi 4 como computador de borde para adquirir, controlar, procesar, almacenar y visualizar información de una situación real de ingeniería electrónica?**

## Plataformas

- El nodo estará basado en un microcontrolador seleccionado para el curso; se utilizará ESP32 como referencia principal.
- El computador de placa única será una Raspberry Pi 4.
- Las herramientas concretas se seleccionan para materializar los resultados del syllabus, sin reemplazar sus conceptos generales.

## Fase 1 – Arquitectura y placa base

Debe incluir todos los contenidos 1.1 a 1.9 del syllabus:

1. Problemática y requerimientos.
2. Arquitectura del sistema embebido.
3. Selección de sensores y actuadores.
4. Alimentación, regulación y protecciones.
5. Diseño esquemático.
6. PCB, footprints y DRC.
7. Gerber, BOM y cotización.
8. Placa base con microcontrolador.
9. Preproyecto ABP 1 y sustentación.

## Fase 2 – Firmware, drivers y comunicaciones

Todos los grupos desarrollarán experiencias académicas sobre:

1. Programación modular en C/C++.
2. Firmware por capas.
3. Consulta de datasheets y driver propio.
4. Integración de un periférico SPI.
5. Wi-Fi.
6. Bluetooth o BLE.
7. HTTP o MQTT.
8. RTOS con tareas, colas y sincronización.
9. Preproyecto ABP 2 y sustentación.

Para el proyecto se seleccionará la combinación de comunicaciones que mejor responda a los requerimientos. La selección debe justificarse técnicamente.

## Fase 3 – Integración con Raspberry Pi 4

Debe incluir todos los contenidos 3.1 a 3.12:

1. Diferencias entre microcontrolador y SBC.
2. Raspberry Pi OS y fundamentos de Linux.
3. Red y SSH.
4. Programación en Python como lenguaje de alto nivel seleccionado.
5. GPIO de la Raspberry Pi.
6. Comunicación con el microcontrolador mediante UART, Wi-Fi, HTTP o MQTT, según el proyecto.
7. Recepción y procesamiento de datos.
8. Base de datos local; se propone SQLite.
9. Dashboard o interfaz web.
10. Ejecución automática como servicio; se propone `systemd`.
11. Registro de eventos y recuperación ante fallas.
12. Integración, muestra y sustentación final.

## Condiciones mínimas del proyecto

- Variable física o estado real verificable.
- Sensor y actuador o indicador.
- Placa base diseñada por el grupo.
- Firmware modular y driver propio.
- Integración SPI en una experiencia de la fase.
- Experiencias con Wi-Fi y Bluetooth/BLE.
- Protocolo HTTP o MQTT.
- Arquitectura RTOS con tareas y mecanismo de sincronización.
- Comunicación microcontrolador–Raspberry Pi seleccionada y justificada.
- Procesamiento, almacenamiento local y visualización.
- Servicio, logs y prueba de recuperación.
- Informe, video y sustentación individual y grupal.
