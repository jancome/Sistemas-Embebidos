# Sistemas Embebidos – 2026-2

Repositorio académico de apoyo para la asignatura **Sistemas Embebidos** del programa de **Ingeniería Electrónica**.

El curso se desarrolla mediante **ABP – Aprendizaje Basado en Proyectos** y recorre el ciclo completo de un sistema embebido distribuido:

1. Diseño electrónico y PCB de un nodo basado en **ESP32**.
2. Firmware modular, drivers, comunicaciones y **FreeRTOS**.
3. Integración del ESP32 con una **Raspberry Pi 4** como computador de borde sobre Linux.

## Situación problema

> **¿Cómo diseñar e implementar un sistema embebido distribuido, robusto y de bajo costo, que adquiera una variable física, controle un actuador y utilice una Raspberry Pi 4 para procesar, almacenar y visualizar información útil en una aplicación real de ingeniería electrónica en Barranquilla y la región Caribe?**

## Estrategia por fases

| Fase | Corte | Producto principal |
|---|---|---|
| Fase 1 | Corte 1 | Requerimientos, arquitectura, selección electrónica, esquemático, PCB, Gerber, BOM y cotización. |
| Fase 2 | Corte 2 | Firmware modular, drivers propios, SPI, Wi-Fi/BLE, HTTP/MQTT y arquitectura FreeRTOS. |
| Fase 3 | Corte 3 | Integración ESP32–Raspberry Pi 4, Linux, SSH, Python, GPIO, base de datos, dashboard, servicio y recuperación ante fallas. |

## Plataformas base

| Componente | Plataforma |
|---|---|
| Nodo de adquisición y control | ESP32 |
| Diseño electrónico | EasyEDA o KiCad |
| Firmware | C/C++ con Arduino IDE o entorno compatible |
| Simulación | Wokwi y herramientas EDA |
| Computador de borde | Raspberry Pi 4 |
| Sistema operativo | Raspberry Pi OS basado en Linux |
| Software de alto nivel | Python |
| Persistencia | SQLite |
| Visualización | Dashboard o interfaz web local |

## GitHub y Microsoft Teams

| GitHub | Microsoft Teams |
|---|---|
| Rutas semanales, guías, cronograma, ejemplos, documentación y plantillas. | Avisos, tareas, entregas, rúbricas, quizzes, parciales, retroalimentación y calificaciones. |

Los enunciados controlados de evaluación se publicarán en Teams. El repositorio contiene los recursos académicos que pueden permanecer disponibles durante el semestre.

## Para comenzar

- [Guía rápida para estudiantes](GUIA_RAPIDA_ESTUDIANTES.md)
- [Syllabus resumido](SYLLABUS.md)
- [Mapa del curso](MAPA_DEL_CURSO.md)
- [Cronograma 2026-2](CRONOGRAMA_2026_2.md)
- [Semanas de clase](semanas/README.md)
- [Estrategia ABP](ABP_PROYECTO_DE_CURSO.md)
- [Evaluación](EVALUACION.md)
- [Proyecto final](PROYECTO_FINAL.md)
- [Normas de clase y laboratorio](NORMAS_DE_CLASE.md)
- [Referencias técnicas](REFERENCIAS.md)

## Enfoque de Ingeniería Electrónica

El curso no se limita a conectar módulos o copiar programas. Cada equipo debe justificar requerimientos eléctricos, selección de sensores y actuadores, alimentación, protecciones, niveles lógicos, esquemático, PCB, estructura de firmware, concurrencia, comunicaciones, integridad de datos, mediciones y pruebas.

## Seguridad

- Todos los prototipos académicos deben operar en baja tensión.
- La lógica del ESP32 y de la Raspberry Pi utiliza **3,3 V**.
- No se conectan motores, relés ni cargas directamente a un GPIO.
- Se debe usar etapa de potencia, protección y fuente independiente cuando corresponda.
- No se permite conectar protoboards o montajes estudiantiles directamente a la red eléctrica de 120 V.
