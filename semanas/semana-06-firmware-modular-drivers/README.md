# Semana 06 – Firmware modular, capas y drivers

**Fecha:** 9 de septiembre de 2026 · **Fase 2**

## Recurso principal

- [Marco teórico: firmware modular, arquitectura por capas y drivers](marco-teorico.md)

## Pregunta guía

¿Cómo separar el firmware para que sensores, comunicación y lógica de aplicación puedan probarse y mantenerse de forma independiente?

## Resultados

- Organizar un proyecto C/C++ por módulos.
- Diferenciar HAL, driver, servicio y aplicación.
- Extraer requisitos de un datasheet.
- Diseñar una interfaz de driver.

## Contenidos

- Archivos `.h` y `.cpp`.
- Encapsulamiento, constantes y tipos.
- Estados y códigos de error.
- Datasheet: registros, tiempos y secuencia de inicio.
- Pruebas unitarias o funciones de diagnóstico básicas.

## Laboratorio

Crear la estructura del firmware del proyecto e implementar un driver sencillo sin esconder la lógica principal dentro de `loop()`.

## Evidencia ABP

- Árbol del proyecto.
- Diagrama por capas.
- Driver documentado.
- Prueba con entrada conocida.
- Error detectado y corrección.
