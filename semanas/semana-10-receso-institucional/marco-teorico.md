# Guía de consolidación – Semana 10

## Receso institucional: integración sin contenido nuevo

Esta semana no introduce contenidos ni exige una entrega. El material sirve únicamente para que cada grupo audite lo construido en los dos primeros cortes y llegue a FreeRTOS con una arquitectura limpia.

## 1. Auditoría voluntaria de trazabilidad

Para cada requisito del ABP comprobar:

```text
requisito → bloque → componente → módulo de firmware → prueba → evidencia
```

Una celda vacía indica trabajo pendiente o un requisito que no puede demostrarse.

## 2. Lista de consolidación de EasyEDA

- esquemático y PCB corresponden a la misma revisión;
- footprints cotejados con datasheet y componente real;
- alimentación y protecciones justificadas;
- ERC/DRC sin errores no resueltos;
- Gerber inspeccionado en visor independiente;
- BOM con MPN y alternativas aprobadas;
- puntos de prueba y programación accesibles.

## 3. Lista de consolidación de ESP32

- aplicación, servicios, drivers y HAL separados;
- no existen esperas indefinidas;
- cada interfaz devuelve errores interpretables;
- SPI tiene captura o evidencia decodificada;
- Wi-Fi y Bluetooth/BLE se probaron por separado;
- HTTP/MQTT tiene payload documentado;
- el control local continúa cuando se pierde la red;
- credenciales no están en el código versionado.

## 4. Medición de deuda técnica

Clasificar cada pendiente:

| Prioridad | Definición | Ejemplo |
|---|---|---|
| P0 | riesgo de daño o seguridad | nivel eléctrico incompatible |
| P1 | bloquea integración | driver no distingue timeout |
| P2 | degrada prueba/mantenimiento | constantes duplicadas |
| P3 | mejora deseable | formato de mensajes de log |

Corregir primero P0 y P1. El grupo puede estimar progreso con:

$$
Cobertura=\frac{requisitos\ con\ prueba\ aprobada}{requisitos\ totales}\times100\%
$$

El porcentaje no sustituye la revisión: un requisito crítico incumplido no se compensa con muchos requisitos menores.

## 5. Pruebas voluntarias de regresión

1. Arranque en frío y reset.
2. Sensor presente y ausente.
3. Actuador habilitado y en estado seguro.
4. SPI válido y periférico desconectado.
5. Wi-Fi disponible y no disponible.
6. Servidor/broker disponible y caído.
7. Recuperación sin intervención manual.

Registrar versión, condición, esperado, observado y evidencia. No se asigna una entrega nueva.

## 6. Preguntas de preparación para Semana 11

1. ¿Qué actividades son periódicas y con qué plazo?
2. ¿Qué recursos comparten adquisición, control y red?
3. ¿Qué función bloquea más tiempo?
4. ¿Qué datos deberían circular por cola y cuáles necesitan exclusión mutua?
5. ¿Qué tarea puede perder una ejecución y cuál no?

## 7. Referencias de repaso

- Marcos teóricos de semanas 1–9 y fuentes primarias citadas en ellos.
- FreeRTOS, *Mastering the FreeRTOS Real Time Kernel*, capítulos 3–8 como lectura anticipada opcional. [Libro oficial](https://www.freertos.org/Documentation/RTOS_book.html).

> Esta guía respeta el receso del 5 al 11 de octubre de 2026: no añade horas presenciales, contenido evaluable ni evidencia obligatoria.
