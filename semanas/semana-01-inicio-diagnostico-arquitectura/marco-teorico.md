# Marco teórico – Semana 01

## Sistemas embebidos, requisitos y arquitectura distribuida

### Propósito formativo

Esta semana establece el lenguaje común del curso. Al finalizar, el estudiante debe poder explicar qué hace embebido a un sistema, separar dominio físico, cómputo y comunicaciones, y convertir una necesidad abierta en requisitos que puedan comprobarse. El resultado no es todavía un circuito: es una arquitectura argumentada que servirá de entrada al diseño en EasyEDA.

## 1. ¿Qué es un sistema embebido?

Un sistema embebido es un sistema de cómputo integrado dentro de un producto o proceso mayor y dedicado a una función concreta. Interactúa con el mundo físico mediante sensores y actuadores, opera con restricciones de energía, memoria, costo y tiempo, y debe responder de manera predecible ante condiciones normales y fallas.

Conviene distinguir tres niveles:

- **Microcontrolador (MCU):** integra CPU, memoria y periféricos; ejecuta firmware y atiende eventos con baja latencia.
- **Sistema en chip (SoC):** integra más subsistemas, por ejemplo procesador, radio, seguridad y periféricos. El ESP32 es un SoC usado como nodo microcontrolado.
- **Computador de placa única (SBC):** ejecuta un sistema operativo completo, administra procesos, archivos y red. La Raspberry Pi 4 es el computador de borde del curso.

La arquitectura del proyecto distribuye responsabilidades:

```text
proceso físico → sensor → acondicionamiento → ESP32 → enlace → Raspberry Pi
                    ↑            ↓                         ↓
                 energía      actuador             base de datos/interfaz
```

El ESP32 conserva adquisición y control cuando la red o el SBC fallan. La Raspberry Pi asume almacenamiento, análisis, visualización y administración. Esta separación evita convertir una pérdida de red en una pérdida de control local.

## 2. Del problema al requisito verificable

Una necesidad expresa intención; un requisito fija una condición comprobable. Un requisito técnico útil contiene sujeto, obligación, condición y criterio:

> El nodo **deberá** medir temperatura entre 0 °C y 60 °C, con error total menor o igual a ±1 °C, una vez por segundo.

Los requisitos se agrupan en:

- funcionales: qué debe hacer el sistema;
- de desempeño: rango, error, periodo, latencia o capacidad;
- de interfaz: tensiones, conectores, protocolo y formato;
- de operación: ambiente, autonomía, arranque y recuperación;
- de seguridad: límites que evitan daño a personas o equipos;
- de evidencia: prueba o medición con la que se aceptará el resultado.

Una métrica debe tener unidad y método de prueba. “Rápido” no es verificable; “latencia extremo a extremo menor de 500 ms en el 95 % de las muestras” sí lo es.

## 3. Presupuestos iniciales de arquitectura

Antes de seleccionar componentes se estiman órdenes de magnitud:

$$
T_{total}=T_{sensor}+T_{procesamiento}+T_{enlace}+T_{SBC}
$$

$$
R_{datos}=f_s\,N_b\,N_c
$$

donde $f_s$ es la frecuencia de muestreo, $N_b$ los bits por muestra y $N_c$ el número de canales. El caudal real será mayor por cabeceras, identificadores, marcas de tiempo y retransmisiones.

La potencia media preliminar se aproxima con:

$$
P_{media}=\sum_i V_i I_i D_i
$$

donde $D_i$ es el ciclo de trabajo del bloque. Esta ecuación permite detectar desde la arquitectura si una fuente, batería o disipación propuesta es irreal.

## 4. Ejemplo guiado adaptado

**Situación:** vigilar temperatura en un gabinete eléctrico y activar ventilación local.

1. Entrada: temperatura del aire y, opcionalmente, corriente del ventilador.
2. ESP32: muestrea cada segundo, filtra, compara umbrales y acciona el ventilador.
3. Enlace: publica un resumen cada 10 s y una alarma inmediatamente.
4. Raspberry Pi: almacena históricos y muestra tendencia.
5. Modo degradado: si se pierde la Raspberry Pi, el control térmico sigue activo en el ESP32.
6. Criterio de aceptación: se inyectan valores conocidos y se verifica activación, latencia, registro y recuperación.

La arquitectura se rechaza si el actuador depende exclusivamente de una respuesta remota para una función crítica.

## 5. Aplicación al ABP

Cada grupo debe producir:

- una frase de problema que identifique usuario, contexto y consecuencia;
- entre cinco y diez requisitos numerados;
- diagrama de bloques con entradas, salidas, energía y enlaces;
- asignación explícita de responsabilidades entre ESP32 y Raspberry Pi;
- una prueba prevista para cada requisito;
- supuestos, riesgos y decisiones aún abiertas.

## 6. Procedimiento de taller

1. Dibujar el límite del sistema y los elementos externos.
2. Enumerar variables físicas, rangos y eventos.
3. Definir entradas, salidas y estados seguros.
4. Asignar cada función a sensor, acondicionamiento, ESP32, actuador o SBC.
5. Añadir alimentación, tierra y dirección de los datos.
6. Revisar cada requisito con la pregunta: “¿qué medición demostraría que se cumple?”.
7. Registrar la primera versión antes de modificarla.

## 7. Diagnóstico de errores frecuentes

| Síntoma | Causa probable | Comprobación | Corrección |
|---|---|---|---|
| El problema es demasiado amplio | No hay usuario ni variable observada | No puede definirse una prueba | Acotar contexto y magnitud física |
| El diagrama solo muestra módulos | Se omitieron interfaces y energía | No aparecen tensión, protocolo o dirección | Etiquetar cada conexión |
| Todo se ejecuta en la Raspberry Pi | No se separó control local de analítica | Una pérdida de red detiene el actuador | Llevar la función crítica al ESP32 |
| Requisitos como “preciso” o “estable” | Falta criterio cuantitativo | Dos evaluadores no coinciden | Añadir unidad, tolerancia y condición |

## 8. Preguntas orientadoras

1. ¿Qué función debe sobrevivir si se desconecta la red?
2. ¿Cuál es la variable física y qué incertidumbre es aceptable?
3. ¿Qué dato cruza cada interfaz y con qué periodicidad?
4. ¿Dónde se toma una decisión y dónde se conserva la evidencia?
5. ¿Qué condición conduce el sistema a un estado seguro?

## 9. Trabajo independiente

- Refinar requisitos con identificadores `RF`, `RD`, `RI` y `RS`.
- Elaborar una matriz requisito–bloque–prueba.
- Calcular caudal de datos y potencia media preliminares.
- Leer en inglés las secciones indicadas y construir un glosario de 15 términos.

## 10. Referencias precisas

- Lee, E. A. y Seshia, S. A., *Introduction to Embedded Systems: A Cyber-Physical Systems Approach*, 2.ª ed., versión 2.3, cap. 1 “Introduction” y cap. 2 “Dynamics of Physical Systems”. [Sitio oficial de UC Berkeley](https://ptolemy.berkeley.edu/books/leeseshia/).
- NASA, *Systems Engineering Handbook*, NASA/SP-2016-6105 Rev. 2, cap. 4, §§4.1–4.3: definición de expectativas, requisitos técnicos y solución lógica. [Edición oficial](https://www.nasa.gov/reference/4-0-system-design-processes/).
- Espressif Systems, *ESP32 Series Datasheet*, v5.3, “Product Overview”, pp. 2–5, y §4 “Functional Description”, pp. 26–50. [PDF oficial](https://www.espressif.com/documentation/esp32_datasheet_en.pdf).
- Raspberry Pi Ltd., *Raspberry Pi 4 Model B Datasheet*, Release 1.1, §§1–2, pp. 5–6. [PDF oficial](https://datasheets.raspberrypi.com/rpi4/raspberry-pi-4-datasheet.pdf).

> Consulta de documentación web: 5 de agosto de 2026. Las explicaciones y el ejemplo son elaboración propia para el curso.
