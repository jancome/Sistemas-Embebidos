# Semana 11 – FreeRTOS y cierre de Fase 2

**Fecha:** 14 de octubre de 2026 · **Fase 2**

## Recurso principal

- [Marco teórico: FreeRTOS, concurrencia y cierre de la Fase 2](marco-teorico.md)

## Pregunta guía

¿Cómo organizar adquisición, control y comunicaciones con diferentes periodos sin crear bloqueos ni datos inconsistentes?

## Resultados

- Crear y planificar tareas.
- Seleccionar periodos y prioridades.
- Intercambiar datos mediante colas.
- Aplicar sincronización cuando sea necesaria.
- Identificar bloqueos y condiciones de carrera.

## Contenidos

- Tareas, estados y planificación.
- `vTaskDelay` y ejecución periódica.
- Colas, mutex, semáforos y notificaciones.
- Watchdog, memoria y tiempos de espera.
- Arquitectura del firmware del nodo.

## Entrega

**Preproyecto ABP 2:** firmware modular, driver propio, SPI, conectividad, HTTP o MQTT, tareas FreeRTOS, mecanismo de comunicación entre tareas, pruebas y manejo de fallas.

## Evaluación

- Parcial 2.
- Preproyecto ABP 2.
- Retroalimentación para integración con Raspberry Pi 4.
