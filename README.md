# Sistemas Embebidos – 2026-2

Repositorio académico de apoyo para la asignatura **Sistemas Embebidos** del programa de **Ingeniería Electrónica**.

El curso se desarrolla mediante **ABP – Aprendizaje Basado en Proyectos** y sigue las tres unidades aprobadas en el syllabus:

1. Arquitectura y diseño de la placa base.
2. Firmware, drivers y comunicaciones.
3. Integración de microcontrolador y computador de placa única — SBC.

## Plataformas oficiales por corte

La progresión práctica del curso será:

| Corte | Plataforma principal | Aplicación durante el curso |
|---|---|---|
| Corte 1 | **EasyEDA** | Arquitectura electrónica, esquemático, selección de componentes, footprints, PCB, DRC, Gerber, BOM y cotización de una placa base para ESP32. |
| Corte 2 | **ESP32** | Programación modular en C/C++, drivers propios, SPI, Wi-Fi, Bluetooth/BLE, HTTP o MQTT y FreeRTOS. |
| Corte 3 | **Raspberry Pi 4** | Raspberry Pi OS/Linux, red, SSH, Python, GPIO, integración con ESP32, procesamiento, base de datos local, dashboard, servicio y recuperación ante fallas. |

Aunque el ESP32 aparece en el diseño electrónico desde el primer corte, la plataforma central de trabajo de ese corte será **EasyEDA**. La programación y explotación completa del ESP32 se desarrollará principalmente en el segundo corte. La Raspberry Pi 4 será la plataforma central del tercer corte.

## Situación problema del curso

> **¿Cómo desarrollar una aplicación basada en sistemas embebidos que integre una placa base diseñada en EasyEDA, un nodo ESP32 y una Raspberry Pi 4 como computador de borde para adquirir, controlar, procesar, almacenar y visualizar información de una situación real de ingeniería electrónica?**

Esta situación contextualiza la gran pregunta institucional: **¿Cómo desarrollar aplicaciones basadas en sistemas embebidos?**

## Organización por fases

| Fase | Corte | Producto principal |
|---|---|---|
| Fase 1 | Corte 1 – EasyEDA | Problemática, requerimientos, arquitectura, sensores, actuadores, alimentación, protecciones, esquemático, PCB, Gerber, BOM y cotización. |
| Fase 2 | Corte 2 – ESP32 | Firmware modular, drivers propios, SPI, Wi-Fi, Bluetooth/BLE, HTTP o MQTT y RTOS. |
| Fase 3 | Corte 3 – Raspberry Pi 4 | Linux, red, SSH, Python, GPIO, integración con ESP32, procesamiento, base de datos, dashboard, servicio y recuperación ante fallas. |

## Implementaciones seleccionadas

| Resultado del syllabus | Implementación del curso |
|---|---|
| Software EDA | EasyEDA |
| Nodo basado en microcontrolador | ESP32 |
| Computador de placa única — SBC | Raspberry Pi 4 |
| Sistema operativo del SBC | Raspberry Pi OS basado en Linux |
| Lenguaje de alto nivel | Python |
| Base de datos local | SQLite |
| Dashboard o interfaz web | Solución local basada en Python |
| Ejecución automática como servicio | `systemd` |
| Registro de eventos | Logs de la aplicación y del servicio |

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
- El ESP32 y los GPIO de la Raspberry Pi trabajan con lógica de 3,3 V.
- No se conectan cargas de potencia directamente a un GPIO.
- Se deben emplear etapas de potencia, protección y fuentes apropiadas.
- No se permite conectar montajes estudiantiles directamente a la red eléctrica de 120 V.
