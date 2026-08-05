# Sistemas Embebidos – 2026-2

Repositorio académico de apoyo para la asignatura **Sistemas Embebidos** del programa de **Ingeniería Electrónica**.

El curso se desarrolla mediante **ABP – Aprendizaje Basado en Proyectos** y sigue las tres unidades aprobadas en el syllabus:

1. Arquitectura y diseño de la placa base.
2. Firmware, drivers y comunicaciones.
3. Integración de microcontrolador y computador de placa única — SBC.

## Plataformas utilizadas

El syllabus no obliga a utilizar una referencia específica de microcontrolador. Para el desarrollo práctico del curso se utilizará un **kit basado en microcontrolador**, con **ESP32 como plataforma de referencia** por los materiales disponibles. También pueden estudiarse STM32 o RP2040 cuando la actividad lo requiera.

Para la Unidad 3 se utilizará **Raspberry Pi 4** como implementación concreta del computador de placa única — SBC solicitado en el syllabus.

## Situación problema del curso

> **¿Cómo desarrollar una aplicación basada en sistemas embebidos que integre un nodo con microcontrolador y una Raspberry Pi 4 como computador de borde para adquirir, controlar, procesar, almacenar y visualizar información de una situación real de ingeniería electrónica?**

Esta situación contextualiza la gran pregunta institucional: **¿Cómo desarrollar aplicaciones basadas en sistemas embebidos?**

## Organización por fases

| Fase | Corte | Producto principal |
|---|---|---|
| Fase 1 | Corte 1 | Problemática, requerimientos, arquitectura, sensores, actuadores, alimentación, protecciones, esquemático, PCB, Gerber, BOM y cotización. |
| Fase 2 | Corte 2 | Firmware modular, drivers propios, SPI, Wi-Fi, Bluetooth/BLE, HTTP o MQTT y RTOS. |
| Fase 3 | Corte 3 | Raspberry Pi 4, Linux, red, SSH, lenguaje de alto nivel, GPIO, integración con el microcontrolador, procesamiento, base de datos, dashboard, servicio y recuperación ante fallas. |

## Implementaciones seleccionadas

Las siguientes herramientas permiten materializar los resultados del syllabus, pero no sustituyen sus conceptos generales:

| Resultado del syllabus | Implementación propuesta |
|---|---|
| Kit basado en microcontrolador | ESP32 como referencia principal |
| Software EDA | EasyEDA o KiCad; Proteus o Altium cuando estén disponibles |
| Lenguaje de alto nivel en el SBC | Python |
| Base de datos local | SQLite |
| Dashboard o interfaz web | Solución local basada en Python |
| Ejecución automática como servicio | `systemd` en Raspberry Pi OS |
| Registro de eventos | Sistema de logs de la aplicación y del servicio |

## GitHub y Microsoft Teams

| GitHub | Microsoft Teams |
|---|---|
| Rutas semanales, guías, cronograma, ejemplos, documentación y plantillas. | Avisos, tareas, entregas, rúbricas, quizzes, parciales, retroalimentación y calificaciones. |

## Para comenzar

- [Matriz de alineación con el syllabus](MATRIZ_ALINEACION_SYLLABUS.md)
- [Syllabus resumido](SYLLABUS.md)
- [Mapa del curso](MAPA_DEL_CURSO.md)
- [Cronograma 2026-2](CRONOGRAMA_2026_2.md)
- [Semanas de clase](semanas/README.md)
- [Estrategia ABP](ABP_PROYECTO_DE_CURSO.md)
- [Evaluación](EVALUACION.md)
- [Proyecto final](PROYECTO_FINAL.md)
- [Materiales](MATERIALES.md)
- [Instalación de software](INSTALACION_SOFTWARE.md)

## Enfoque de Ingeniería Electrónica

Cada equipo debe justificar requerimientos eléctricos y funcionales, selección de sensores y actuadores, alimentación, regulación, protecciones, niveles lógicos, diseño esquemático, PCB, estructura del firmware, concurrencia, comunicaciones, procesamiento, almacenamiento, visualización y recuperación ante fallas.

## Seguridad

- Los prototipos académicos deben operar en baja tensión.
- Deben verificarse los niveles lógicos de cada plataforma.
- No se conectan cargas de potencia directamente a un GPIO.
- Se deben emplear etapas de potencia, protección y fuentes apropiadas.
- No se permite conectar montajes estudiantiles directamente a la red eléctrica de 120 V.
