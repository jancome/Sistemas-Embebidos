# Proyecto de curso – Aprendizaje Basado en Proyectos

## Situación problema

> **¿Cómo diseñar e implementar un sistema embebido distribuido, robusto y de bajo costo, que adquiera una variable física, controle un actuador y utilice una Raspberry Pi 4 para procesar, almacenar y visualizar información útil en una aplicación real de ingeniería electrónica en Barranquilla y la región Caribe?**

## Condiciones obligatorias

El proyecto debe incluir:

- una variable física medible;
- al menos un sensor conectado al ESP32;
- al menos un actuador o indicador con etapa electrónica apropiada;
- placa base diseñada por el grupo;
- firmware modular en C/C++;
- un driver desarrollado o adaptado mediante consulta de datasheet;
- una comunicación cableada y una comunicación de red;
- FreeRTOS con tareas y un mecanismo de intercambio o sincronización;
- Raspberry Pi 4 con Linux y Python;
- almacenamiento local de datos;
- dashboard o interfaz de operación;
- ejecución automática, logs y recuperación ante fallas.

## Fase 1 – Arquitectura y placa base

**Pregunta:** ¿qué debe medir, decidir y controlar el sistema, y qué electrónica necesita para hacerlo de forma segura?

Entregables:

1. Necesidad y contexto.
2. Requerimientos funcionales y no funcionales.
3. Diagrama de bloques.
4. Selección justificada de sensor y actuador.
5. Presupuesto de potencia y alimentación.
6. Regulación y protecciones.
7. Esquemático.
8. PCB, footprints y DRC.
9. Gerber, BOM y cotización.
10. Presentación y sustentación del Preproyecto 1.

## Fase 2 – Firmware y comunicaciones

**Pregunta:** ¿cómo organizar el firmware para adquirir, controlar y comunicar datos sin bloquear el sistema?

Entregables:

1. Arquitectura de firmware por capas.
2. Módulos de sensores, actuadores, comunicación y aplicación.
3. Driver basado en datasheet.
4. Integración SPI.
5. Wi-Fi o Bluetooth/BLE.
6. HTTP o MQTT.
7. Tareas FreeRTOS.
8. Cola, mutex, semáforo o notificación, según necesidad.
9. Manejo de errores y reconexión.
10. Presentación y sustentación del Preproyecto 2.

## Fase 3 – Computador de borde con Raspberry Pi 4

**Pregunta:** ¿cómo convertir los datos del nodo en información confiable y operable desde una plataforma Linux?

Entregables:

1. Raspberry Pi OS y configuración de red.
2. Acceso SSH.
3. Aplicación Python organizada por módulos.
4. Prueba GPIO segura.
5. Comunicación ESP32–Raspberry Pi.
6. Validación y procesamiento de tramas.
7. Base de datos SQLite.
8. Dashboard o interfaz web local.
9. Servicio de inicio automático.
10. Logs y recuperación ante fallas.
11. Prototipo integrado, informe, video y sustentación.

## Enfoque de ingeniería

Cada decisión debe responder:

- ¿qué requisito satisface?;
- ¿qué límite eléctrico o temporal debe respetar?;
- ¿cómo se probó?;
- ¿qué evidencia demuestra que funciona?;
- ¿qué sucede cuando falla un sensor, la red o la alimentación?;
- ¿cómo se recupera el sistema?
