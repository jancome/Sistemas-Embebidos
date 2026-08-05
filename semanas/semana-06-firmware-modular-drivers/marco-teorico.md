# Marco teórico – Semana 06

## Firmware modular, capas y drivers en ESP32

### Propósito formativo

El firmware convierte la arquitectura electrónica del Corte 1 en comportamiento verificable. Su calidad no se mide por cuántas líneas hay dentro de `loop()`, sino por la separación de responsabilidades, el manejo explícito de estados y errores, y la posibilidad de probar cada módulo sin depender del sistema completo.

## 1. Capas de firmware

Una organización útil para el proyecto es:

```text
aplicación: reglas del proyecto y estados globales
servicios: adquisición, control, registro, conectividad
drivers: protocolo y comportamiento de cada periférico
HAL/BSP: GPIO, buses, temporizadores y pines de la placa
hardware: ESP32, sensores, actuadores y placa base
```

La dirección de dependencia debe ir hacia abajo. La aplicación solicita `leer_temperatura()`; no debería construir manualmente una trama SPI ni conocer el pin de chip-select. La capa inferior informa éxito, dato y causa de error sin decidir la política global.

## 2. Interfaz, implementación y estado

El archivo de interfaz declara tipos, constantes y operaciones públicas. La implementación conserva detalles privados. Una API de driver mínima puede incluir:

- configuración o contexto del dispositivo;
- `init()` con secuencia verificable;
- `read()`/`write()` con límite de tiempo;
- estado y códigos de error;
- función de diagnóstico o identidad;
- `deinit()` cuando el recurso pueda liberarse.

Los códigos deben distinguir al menos argumento inválido, dispositivo ausente, timeout, dato inválido y error de bus. Un `bool` único borra información diagnóstica.

## 3. Datasheet convertido en driver

La lectura técnica sigue este orden:

1. condiciones recomendadas y máximos absolutos;
2. pinout e interfaz;
3. secuencia de encendido y reset;
4. temporización;
5. mapa de registros, valores de reset y bits reservados;
6. conversión de datos crudos a unidades físicas;
7. estados de error e identidad del dispositivo.

Para un registro de $n$ bits dentro de una palabra:

$$
campo=(registro\gg desplazamiento)\ \&\ (2^n-1)
$$

La conversión típica se documenta como:

$$
x=a\cdot raw+b
$$

incluyendo signo, endianness, saturación y unidades.

## 4. Tiempo, bloqueo y presupuesto de memoria

Una llamada bloqueante tiene un tiempo máximo. Si el periférico tarda $T_c$ y se consulta cada $T_s$, el diseño debe comprobar $T_c<T_s$ y reservar margen para las demás tareas. Los reintentos acotados cumplen:

$$
T_{fallo}\leq N(T_{timeout}+T_{espera})
$$

Una variable compartida modificada desde interrupción se trata con mecanismos apropiados; `volatile` evita ciertas optimizaciones, pero no vuelve atómica una operación ni resuelve una condición de carrera.

## 5. Ejemplo guiado adaptado

**Driver de sensor con registro de identidad y medida:**

1. `sensor_init()` configura bus, lee `WHO_AM_I` y compara el valor esperado.
2. Escribe configuración preservando bits reservados mediante máscara.
3. Espera estado `data_ready` con timeout.
4. Lee bytes alto y bajo, arma el valor con el orden indicado.
5. Verifica rango y convierte a unidad física.
6. Devuelve estructura `{valor, timestamp, calidad}` o error preciso.
7. Una prueba sustituye el bus por respuestas conocidas para validar conversión y errores.

## 6. Aplicación al ABP

El firmware del grupo debe separar como mínimo:

- configuración de placa (`board_config`);
- driver del sensor o periférico;
- servicio de adquisición;
- control del actuador con estado seguro;
- transporte de datos;
- aplicación y máquina de estados;
- registro diagnóstico.

La política de reconexión pertenece al servicio o aplicación; la generación exacta de una transacción pertenece al driver.

## 7. Procedimiento de laboratorio

1. Dibujar el diagrama de capas y dependencias.
2. Crear `.h`/`.cpp` o módulos equivalentes sin lógica duplicada.
3. Implementar primero identidad, inicialización y una operación.
4. Probar conversión con entradas conocidas antes del hardware.
5. Probar periférico desconectado, respuesta errónea y timeout.
6. Registrar tiempos, memoria libre y código de error.
7. Integrar con la aplicación solo después de aprobar el driver.

## 8. Diagnóstico de fallas

| Síntoma | Causa probable | Prueba | Corrección |
|---|---|---|---|
| Funciona solo con un sensor | pines/dirección codificados globalmente | crear dos contextos | parametrizar instancia |
| Error siempre “false” | interfaz demasiado pobre | forzar fallas diferentes | enumerar causas |
| Lectura absurda | signo, escala o endianness | usar patrón conocido | corregir armado/conversión |
| Arranque intermitente | secuencia o tiempo ignorado | registrar estados y tiempos | implementar datasheet |
| Cambiar pin rompe toda la app | hardware filtrado a capas altas | buscar referencias de GPIO | centralizar BSP/HAL |

## 9. Preguntas y trabajo independiente

1. ¿Qué sabe la aplicación que no debería saber?
2. ¿Cuál es el tiempo máximo de cada llamada?
3. ¿Cómo se distingue “cero medido” de “lectura inválida”?
4. ¿Qué prueba puede ejecutarse sin el sensor físico?

Entregar árbol del proyecto, diagrama de capas, tabla registro–bit–función, API documentada, tres pruebas positivas y tres de falla.

## 10. Referencias precisas

- Espressif Systems, *ESP-IDF Programming Guide*, “API Conventions”, “Error Codes and Helper Functions”, “GPIO & RTC GPIO” y periférico elegido. [Documentación estable](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/).
- Espressif Systems, *ESP32 Series Datasheet*, v5.3, §4 “Functional Description”, pp. 26–50; §4.8 “Digital Peripherals”, pp. 36–42. [PDF oficial](https://www.espressif.com/documentation/esp32_datasheet_en.pdf).
- Lee y Seshia, *Introduction to Embedded Systems*, 2.ª ed., cap. 10 “Input and Output” y cap. 11 “Multitasking”. [UC Berkeley](https://ptolemy.berkeley.edu/books/leeseshia/).
- Datasheet del periférico del proyecto: “Register map”, “Timing characteristics” y “Power-up sequence”, con versión y páginas indicadas por el grupo.

> Consulta de documentación web: 5 de agosto de 2026. Los fragmentos conceptuales y ejemplos son originales del curso.
