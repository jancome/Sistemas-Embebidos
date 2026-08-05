# Marco teórico – Semana 11

## FreeRTOS: tareas, colas, sincronización y cierre del nodo ESP32

### Propósito formativo

Un RTOS organiza trabajo concurrente con restricciones temporales; no hace que el código sea automáticamente rápido ni seguro. La arquitectura debe asignar periodos, plazos, prioridades, recursos y mecanismos de comunicación, y luego medir que se cumplen.

## 1. Tareas y estados

Una tarea puede estar ejecutándose, lista, bloqueada o suspendida. Bloquearse esperando tiempo, cola o evento libera procesador; un ciclo que consulta continuamente desperdicia CPU y puede impedir otras tareas.

Para una actividad periódica:

- $T_i$: periodo;
- $C_i$: peor tiempo de ejecución;
- $D_i$: plazo;
- $J_i$: variación temporal o jitter.

La utilización aproximada es:

$$
U=\sum_i\frac{C_i}{T_i}
$$

Un valor menor que 1 no garantiza planificabilidad cuando hay bloqueos, prioridades, dos núcleos o secciones críticas, pero detecta arquitecturas imposibles y obliga a medir $C_i$.

`vTaskDelayUntil()` favorece periodicidad respecto de una referencia; encadenar `vTaskDelay()` acumula el tiempo de ejecución en el periodo observado.

## 2. Comunicación frente a protección

- **Cola:** transfiere datos y desacopla productor/consumidor.
- **Notificación de tarea:** señal ligera dirigida a una tarea.
- **Semáforo binario/de conteo:** representa evento o cantidad de recursos.
- **Mutex:** protege un recurso compartido y aplica herencia de prioridad donde esté soportada.
- **Event group:** representa combinación de banderas de estado.

Una cola comunica propiedad de datos; un mutex no transporta datos. Mantener un mutex durante una operación de red o espera larga amplía bloqueo y riesgo de inversión de prioridad.

## 3. Condiciones de carrera y secciones críticas

Una operación `x = x + 1` implica leer, modificar y escribir; dos tareas pueden intercalarse y perder una actualización. Se evita compartición, se usa paso de mensajes o se protege la sección mínima necesaria.

Las interrupciones deben hacer trabajo corto y usar variantes de API permitidas desde ISR. El procesamiento pesado se difiere a una tarea mediante notificación o cola.

## 4. Memoria, watchdog y recuperación

Cada tarea consume stack. El tamaño se mide con marcas de agua y escenarios de peor caso; desbordar stack puede producir fallas no locales. Las asignaciones dinámicas repetidas y cadenas extensas favorecen fragmentación.

El watchdog detecta falta de progreso, pero no repara la causa. Antes de alimentarlo, el sistema debe demostrar que completó actividades críticas. Timeouts y estado seguro son parte del diseño.

## 5. Ejemplo guiado de arquitectura

| Tarea | Periodo/evento | Prioridad relativa | Entrada | Salida |
|---|---|---:|---|---|
| adquisición | 100 ms | alta | driver sensor | cola de muestras |
| control | 100 ms | alta | última muestra | actuador/estado |
| publicación | evento/10 s | media | cola de mensajes | MQTT/HTTP |
| diagnóstico | 1 s | baja | contadores | log/telemetría |

La adquisición nunca espera a la red. Si la cola de publicación se llena, se aplica una política explícita: descartar más antigua, conservar alarma o registrar pérdida. El control usa timestamp/calidad y pasa a estado seguro si la muestra está vencida.

## 6. Procedimiento de laboratorio

1. Medir tiempos de las funciones antes de crear tareas.
2. Definir tabla $C,T,D$, prioridad, stack y recurso.
3. Implementar adquisición y control con cola o buffer explícito.
4. Añadir comunicación sin bloquear la tarea crítica.
5. Medir jitter, uso de stack, longitud máxima de cola y fallas.
6. Forzar sensor lento, red caída y cola llena.
7. Verificar watchdog, estado seguro y recuperación.

## 7. Diagnóstico

| Síntoma | Causa probable | Evidencia | Corrección |
|---|---|---|---|
| Tarea crítica pierde plazo | prioridad/bloqueo/CPU | timestamps y duración | reducir bloqueo o reestructurar |
| Datos inconsistentes | carrera | secuencia/valores imposibles | cola o exclusión mínima |
| Deadlock | orden distinto de mutex | tareas esperando recursos | orden global y timeout |
| Reinicio watchdog | tarea no cede o ISR larga | último log/trace | bloquear correctamente y acortar ISR |
| Falla al crecer carga | stack/heap | high-water mark y heap | dimensionar y evitar fragmentación |
| Cola siempre llena | productor > consumidor | ocupación temporal | política de carga/backpressure |

## 8. Preguntas y trabajo independiente

1. ¿Qué plazo tiene cada función y de dónde proviene?
2. ¿Qué dato puede perderse y cuál debe preservarse?
3. ¿Qué ocurre si una tarea nunca recibe el recurso?
4. ¿Cómo se demuestra ausencia de bloqueo largo?
5. ¿Qué información debe llegar a Raspberry Pi para diagnosticar el nodo?

Entregar tabla temporal, diagrama de tareas, evidencia de colas/sincronización, mediciones de stack y tres pruebas de falla para el Preproyecto 2.

## 9. Referencias precisas

- FreeRTOS, *Mastering the FreeRTOS Real Time Kernel*, capítulos 3 “Task Management”, 4 “Queue Management”, 7 “Resource Management” y 8 “Event Groups”. [Libro oficial](https://www.freertos.org/Documentation/RTOS_book.html).
- Espressif Systems, *ESP-IDF Programming Guide*, “FreeRTOS (IDF)”, §§“Overview”, “Symmetric Multiprocessing”, “Tasks”, “Scheduler” y “Critical Sections”. [Documentación estable](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/freertos_idf.html).
- Espressif Systems, *ESP-IDF Programming Guide*, “Watchdogs” y “Heap Memory Debugging”. [API de sistema](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/).
- Lee y Seshia, *Introduction to Embedded Systems*, 2.ª ed., cap. 11 “Multitasking” y cap. 12 “Scheduling”. [UC Berkeley](https://ptolemy.berkeley.edu/books/leeseshia/).

> Consulta: 5 de agosto de 2026. Debe distinguirse la API de FreeRTOS usada por Arduino-ESP32 de la versión de ESP-IDF seleccionada por el curso.
