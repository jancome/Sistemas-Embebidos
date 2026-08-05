# Matriz de alineación con el syllabus aprobado

Esta matriz relaciona cada contenido numerado del syllabus con la semana, la plataforma y la evidencia del curso.

## Unidad 1 – Arquitectura y diseño de la placa base con EasyEDA

| Código del syllabus | Contenido aprobado | Semana | Plataforma | Evidencia |
|---|---|---:|---|---|
| 1.1 | Problemática y requerimientos del proyecto ABP | 1 | EasyEDA / documentación | Situación, usuario y requerimientos iniciales |
| 1.2 | Arquitectura del sistema embebido | 1 | EasyEDA / diagramación | Diagrama de bloques |
| 1.3 | Selección de sensores y actuadores | 2 | EasyEDA + datasheets | Matriz comparativa y selección |
| 1.4 | Alimentación, regulación y protecciones | 3 | EasyEDA | Cálculos, esquema y mediciones |
| 1.5 | Diseño esquemático | 4 | EasyEDA | Esquemático revisado |
| 1.6 | Diseño de PCB, footprints y reglas DRC | 4 | EasyEDA | PCB, footprints y reporte DRC |
| 1.7 | Generación de Gerber, BOM y cotización | 5 | EasyEDA | Gerber, BOM y cotización |
| 1.8 | Placa base con el microcontrolador | 5 | EasyEDA + ESP32 | Diseño final de la placa base ESP32 |
| 1.9 | Preproyecto ABP 1: arquitectura y placa base | 5 | EasyEDA | Entrega y sustentación |

## Unidad 2 – Firmware, drivers y comunicaciones con ESP32

| Código del syllabus | Contenido aprobado | Semana | Plataforma | Evidencia |
|---|---|---:|---|---|
| 2.1 | Programación modular en C/C++ y firmware por capas | 6 | ESP32 | Estructura modular |
| 2.2 | Datasheets y desarrollo de drivers propios | 6 | ESP32 | Driver documentado |
| 2.3 | Bus SPI e integración de periféricos | 7 | ESP32 | Transacción SPI verificada |
| 2.4 | Comunicación inalámbrica: Wi-Fi y Bluetooth/BLE | 8 | ESP32 | Experiencias con ambas tecnologías |
| 2.5 | Comunicación HTTP o MQTT | 9 | ESP32 | Intercambio de datos mediante uno de los protocolos |
| 2.6 | RTOS: tareas, colas y sincronización | 11 | ESP32 / FreeRTOS | Arquitectura concurrente |
| 2.7 | Preproyecto ABP 2: firmware y comunicaciones | 11 | ESP32 | Entrega y sustentación |

## Unidad 3 – Integración de ESP32 y Raspberry Pi 4

| Código del syllabus | Contenido aprobado | Semana | Plataforma | Evidencia |
|---|---|---:|---|---|
| 3.1 | Diferencia entre microcontrolador y SBC | 12 | ESP32 + Raspberry Pi 4 | Cuadro comparativo y arquitectura |
| 3.2 | Sistema operativo del SBC y fundamentos de Linux | 12 | Raspberry Pi 4 | Raspberry Pi OS configurado |
| 3.3 | Configuración de red y acceso SSH | 13 | Raspberry Pi 4 | Acceso remoto documentado |
| 3.4 | Programación en un lenguaje de alto nivel | 13 | Raspberry Pi 4 / Python | Aplicación inicial |
| 3.5 | GPIO del SBC | 14 | Raspberry Pi 4 | Práctica segura de entrada/salida |
| 3.6 | Comunicación microcontrolador–SBC: UART, Wi-Fi, HTTP o MQTT | 14 | ESP32 + Raspberry Pi 4 | Enlace seleccionado y documentado |
| 3.7 | Recepción y procesamiento de datos | 15 | Raspberry Pi 4 | Validación y transformación de datos |
| 3.8 | Base de datos local | 15 | Raspberry Pi 4 / SQLite | Registros y consultas |
| 3.9 | Dashboard o interfaz web | 16 | Raspberry Pi 4 | Visualización funcional |
| 3.10 | Ejecución automática como servicio | 16 | Raspberry Pi 4 / Linux | Servicio configurado |
| 3.11 | Registro de eventos y recuperación ante fallas | 16 | Raspberry Pi 4 | Logs y prueba de recuperación |
| 3.12 | Integración, muestra y sustentación final | 17 | Sistema completo | Proyecto final y defensa |

## Competencias transversales

| Competencia del syllabus | Aplicación durante el curso |
|---|---|
| Razonamiento cuantitativo | Cálculos de alimentación, tiempos, consumo y análisis de datos |
| Lectura crítica e inglés | Consulta de datasheets y documentación técnica |
| Resolución de problemas | Diagnóstico de fallas y ajustes del proyecto |
| Comunicación escrita | Informes, bitácoras y documentación |
| Comunicación oral | Sustentaciones individuales y grupales |
| Analítica de datos | Procesamiento y consultas sobre la base local |
| Trabajo en equipo | Roles, integración y revisión por pares |
| Uso de TIC | EasyEDA, IDE, control de versiones, ESP32, Linux y acceso remoto |

## Secuencia oficial

1. **Corte 1:** EasyEDA para diseñar la placa base ESP32.
2. **Corte 2:** ESP32 para firmware, drivers, comunicaciones y FreeRTOS.
3. **Corte 3:** Raspberry Pi 4 para la capa Linux, procesamiento, almacenamiento, visualización y operación robusta.
