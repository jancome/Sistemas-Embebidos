# Matriz de alineación con el syllabus aprobado

Esta matriz relaciona cada contenido numerado del syllabus con la semana y la evidencia del curso.

## Unidad 1 – Arquitectura y diseño de la placa base

| Código del syllabus | Contenido aprobado | Semana | Evidencia |
|---|---|---:|---|
| 1.1 | Problemática y requerimientos del proyecto ABP | 1 | Situación, usuario, requerimientos iniciales |
| 1.2 | Arquitectura del sistema embebido | 1 | Diagrama de bloques |
| 1.3 | Selección de sensores y actuadores | 2 | Matriz comparativa y datasheets |
| 1.4 | Alimentación, regulación y protecciones | 3 | Cálculos, esquema y mediciones |
| 1.5 | Diseño esquemático | 4 | Esquemático revisado |
| 1.6 | Diseño de PCB, footprints y reglas DRC | 4 | PCB, footprints y reporte DRC |
| 1.7 | Generación de Gerber, BOM y cotización | 5 | Gerber, BOM y cotización |
| 1.8 | Placa base con el microcontrolador | 5 | Diseño final de la placa base |
| 1.9 | Preproyecto ABP 1: arquitectura y placa base | 5 | Entrega y sustentación |

## Unidad 2 – Firmware, drivers y comunicaciones

| Código del syllabus | Contenido aprobado | Semana | Evidencia |
|---|---|---:|---|
| 2.1 | Programación modular en C/C++ y firmware por capas | 6 | Estructura modular |
| 2.2 | Datasheets y desarrollo de drivers propios | 6 | Driver documentado |
| 2.3 | Bus SPI e integración de periféricos | 7 | Transacción SPI verificada |
| 2.4 | Comunicación inalámbrica: Wi-Fi y Bluetooth/BLE | 8 | Experiencias con ambas tecnologías y selección para el proyecto |
| 2.5 | Comunicación HTTP o MQTT | 9 | Intercambio de datos mediante uno de los dos protocolos |
| 2.6 | RTOS: tareas, colas y sincronización | 11 | Arquitectura concurrente |
| 2.7 | Preproyecto ABP 2: firmware y comunicaciones | 11 | Entrega y sustentación |

## Unidad 3 – Integración de microcontrolador y SBC

| Código del syllabus | Contenido aprobado | Semana | Evidencia |
|---|---|---:|---|
| 3.1 | Diferencia entre microcontrolador y SBC | 12 | Cuadro comparativo y arquitectura |
| 3.2 | Sistema operativo del SBC y fundamentos de Linux | 12 | Raspberry Pi OS configurado |
| 3.3 | Configuración de red y acceso SSH | 13 | Acceso remoto documentado |
| 3.4 | Programación en un lenguaje de alto nivel | 13 | Aplicación inicial en Python |
| 3.5 | GPIO del SBC | 14 | Práctica segura de entrada/salida |
| 3.6 | Comunicación microcontrolador–SBC: UART, Wi-Fi, HTTP o MQTT | 14 | Enlace seleccionado y documentado |
| 3.7 | Recepción y procesamiento de datos | 15 | Validación y transformación de datos |
| 3.8 | Base de datos local | 15 | Registros y consultas |
| 3.9 | Dashboard o interfaz web | 16 | Visualización funcional |
| 3.10 | Ejecución automática como servicio | 16 | Servicio configurado |
| 3.11 | Registro de eventos y recuperación ante fallas | 16 | Logs y prueba de recuperación |
| 3.12 | Integración, muestra y sustentación final | 17 | Proyecto final y defensa |

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
| Uso de TIC | EDA, IDE, control de versiones, Linux y acceso remoto |

## Diferencia entre contenido e implementación

El syllabus establece conceptos generales: microcontrolador, SBC, lenguaje de alto nivel, base de datos, dashboard y servicio. El curso utiliza ESP32, Raspberry Pi 4, Python, SQLite y `systemd` como implementaciones concretas para desarrollar esos resultados.
