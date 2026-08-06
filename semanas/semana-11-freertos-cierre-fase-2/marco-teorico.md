# Marco teórico – Semana 11

# FreeRTOS, concurrencia y cierre de la Fase 2

## 1. Propósito

Organizar el firmware del ESP32 mediante tareas concurrentes y mecanismos de intercambio seguros. El objetivo no es crear muchas tareas, sino asignar responsabilidades, periodos y prioridades coherentes, evitando bloqueos, condiciones de carrera y pérdida de datos.

## 2. Resultados de aprendizaje

Al finalizar la semana, el estudiante estará en capacidad de:

- Diferenciar concurrencia y paralelismo.
- Crear tareas periódicas en FreeRTOS.
- Seleccionar prioridades y periodos.
- Intercambiar datos mediante colas.
- Utilizar mutex, semáforos o notificaciones cuando corresponda.
- Reconocer bloqueos, inanición y condiciones de carrera.
- Incorporar timeout y watchdog.
- Sustentar la arquitectura del Preproyecto ABP 2.

## 3. Planificador y tareas

FreeRTOS administra tareas con estados como:

- ejecutándose;
- lista;
- bloqueada;
- suspendida.

Una tarea no debe ocupar la CPU continuamente. Debe bloquearse o esperar cuando no tiene trabajo.

## 4. Tarea periódica

Una tarea de adquisición puede ejecutarse cada segundo:

```text
leer sensor
→ validar
→ enviar a cola
→ esperar hasta el siguiente periodo
```

Para mantener un periodo más estable se utiliza un mecanismo de retardo periódico, evitando acumular el tiempo de ejecución de cada ciclo.

## 5. Prioridades

La prioridad representa urgencia de ejecución, no importancia general del módulo.

Criterios:

- una tarea de seguridad puede requerir respuesta rápida;
- una tarea de dashboard no debe desplazar adquisición crítica;
- una prioridad alta mal diseñada puede impedir que otras tareas se ejecuten;
- tareas con igual prioridad pueden compartir tiempo según configuración.

El estudiante debe justificar cada prioridad.

## 6. Colas

Las colas permiten transferir copias de datos entre tareas.

```text
Tarea sensor → cola de mediciones → tarea de control
                               └→ tarea de comunicación
```

Ventajas:

- desacoplamiento;
- almacenamiento temporal;
- sincronización implícita;
- control de tamaño.

Se debe definir qué ocurre si la cola está llena o vacía.

## 7. Mutex

Un mutex protege un recurso compartido, por ejemplo:

- bus SPI compartido;
- puerto serial;
- estructura global;
- archivo o registro común.

El mutex no debe mantenerse durante esperas largas. La sección crítica debe ser breve.

## 8. Semáforos

Un semáforo puede representar un evento o disponibilidad de recursos.

- binario: evento disponible/no disponible;
- contador: varios eventos o recursos.

No debe utilizarse como sustituto de una cola cuando se necesita transportar datos.

## 9. Notificaciones de tarea

Las notificaciones son mecanismos ligeros para avisar o enviar valores simples a una tarea específica. Son útiles cuando existe un productor y un consumidor claramente definidos.

## 10. Condición de carrera

Ocurre cuando el resultado depende del orden temporal de accesos concurrentes.

Ejemplo:

```text
Tarea A lee contador = 5
Tarea B lee contador = 5
Tarea A escribe 6
Tarea B escribe 6
```

Se esperaban dos incrementos, pero se obtiene uno. La solución puede requerir mutex, operación atómica o rediseño del flujo.

## 11. Bloqueo mutuo

Puede ocurrir si dos tareas esperan recursos en orden opuesto.

```text
Tarea A toma mutex 1 y espera mutex 2
Tarea B toma mutex 2 y espera mutex 1
```

La prevención incluye:

- orden único de adquisición;
- timeout;
- menos recursos compartidos;
- arquitectura por mensajes.

## 12. Inversión de prioridad

Una tarea de alta prioridad puede quedar esperando un recurso retenido por una tarea de baja prioridad. Los mutex de RTOS pueden incluir herencia de prioridad, pero el diseño debe reducir secciones críticas prolongadas.

## 13. Memoria de pila

Cada tarea necesita pila. Una asignación insuficiente produce fallas difíciles de diagnosticar; una excesiva desperdicia RAM.

Se deben observar:

- variables locales grandes;
- llamadas anidadas;
- bibliotecas;
- serialización JSON;
- profundidad mínima de pila registrada.

## 14. Watchdog

El watchdog detecta tareas o sistema que dejan de responder. No reemplaza la corrección del firmware. Reiniciar continuamente puede ocultar un bloqueo.

El registro debe permitir conocer:

- tarea implicada;
- último estado;
- tiempo;
- causa probable.

## 15. Ejemplo guiado

Sistema con cuatro responsabilidades:

| Tarea | Periodo/evento | Prioridad relativa | Comunicación |
|---|---|---:|---|
| adquisición | 1 s | media | envía medición |
| control | recibe medición | alta | recibe cola |
| comunicación | 30 s o datos disponibles | baja/media | consume buffer |
| diagnóstico | 5 s | baja | observa estados |

Flujo:

```text
SensorTask → MeasurementQueue → ControlTask
                       └──────→ NetworkTask
```

Si la red falla, `NetworkTask` no bloquea `SensorTask`. Puede almacenar un número limitado de mediciones y descartar o resumir según política.

## 16. Actividad práctica

Cada grupo debe:

1. identificar responsabilidades;
2. crear al menos tres tareas justificadas;
3. definir periodos y prioridades;
4. usar una cola;
5. usar un mecanismo adicional si es necesario;
6. eliminar retardos bloqueantes de la aplicación;
7. medir tiempos;
8. observar uso de pila;
9. provocar cola llena o pérdida de red;
10. demostrar recuperación.

## 17. Preproyecto ABP 2

Debe incluir:

- arquitectura por capas;
- driver propio;
- periférico SPI;
- experiencia Wi-Fi y Bluetooth/BLE;
- HTTP o MQTT;
- tareas FreeRTOS;
- cola o sincronización;
- manejo de errores;
- evidencias temporales;
- sustentación individual.

## 18. Diagnóstico de fallas

Si el sistema se congela:

1. revisar qué tarea dejó de registrar actividad;
2. identificar recurso esperado;
3. comprobar mutex y colas;
4. revisar bucles sin bloqueo;
5. observar watchdog;
6. revisar pila;
7. reducir el sistema a dos tareas;
8. añadir marcas temporales;
9. reproducir la condición.

Si se pierden datos:

- revisar tamaño de cola;
- comprobar tiempos de producción y consumo;
- registrar desbordamiento;
- verificar copia y vida útil de estructuras;
- revisar acceso concurrente.

## 19. Errores comunes

- Crear una tarea por cada función pequeña.
- Asignar prioridad máxima a todo.
- Usar colas sin comprobar retorno.
- Proteger operaciones largas con mutex.
- Compartir variables sin sincronización.
- Usar `delay()` dentro de tareas críticas.
- Reiniciar como única estrategia de recuperación.
- Ignorar uso de pila.
- No registrar eventos de error.

## 20. Trabajo independiente

- Completar arquitectura de tareas.
- Documentar periodos y prioridades.
- Registrar pruebas de cola y reconexión.
- Preparar entrega del Preproyecto 2.
- Definir qué datos enviará el ESP32 a Raspberry Pi en el Corte 3.

## 21. Referencias de apoyo

- Documentación oficial FreeRTOS.
- Documentación oficial ESP-IDF sobre FreeRTOS en ESP32.
- `SYLLABUS.md`, `EVALUACION.md` y `evaluaciones/preproyectos/README.md`.
