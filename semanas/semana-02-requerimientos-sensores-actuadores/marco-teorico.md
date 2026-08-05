# Marco teórico – Semana 02

## Selección de sensores, actuadores e interfaces

### Propósito formativo

Seleccionar un dispositivo no consiste en escoger el primero disponible. Consiste en demostrar que su rango, incertidumbre, dinámica, interfaz, consumo y condiciones de uso satisfacen los requisitos y son compatibles con la placa que se diseñará en EasyEDA.

## 1. Cadena de medición y actuación

Una cadena de medición transforma una magnitud física en información digital:

$$
x(t)\rightarrow \text{sensor}\rightarrow \text{acondicionamiento}\rightarrow ADC/entrada\rightarrow \hat{x}[k]
$$

La cadena de actuación recorre el camino inverso desde una decisión digital hasta potencia física. Un GPIO no es una fuente de potencia: un relé, motor, solenoide o lámpara requiere una etapa de mando, protección y fuente apropiadas.

## 2. Parámetros que no deben confundirse

- **Rango:** intervalo de entrada admitido.
- **Resolución:** cambio mínimo representable o discernible.
- **Exactitud:** cercanía al valor verdadero, expresada con tolerancia.
- **Precisión/repetibilidad:** dispersión entre mediciones repetidas.
- **Sensibilidad:** pendiente de la salida respecto a la entrada.
- **Offset:** salida distinta de cero cuando la entrada es cero.
- **Tiempo de respuesta y ancho de banda:** rapidez con la que el dispositivo sigue cambios.
- **Deriva:** variación con tiempo, temperatura o alimentación.

Para un ADC ideal de $N$ bits y rango $V_{FS}$:

$$
LSB=\frac{V_{FS}}{2^N}, \qquad |e_q|\leq \frac{LSB}{2}
$$

La resolución nominal no garantiza exactitud: ruido, referencia, no linealidad y acondicionamiento forman parte del error total. Una aproximación conservadora suma errores máximos; cuando son independientes puede emplearse raíz de suma de cuadrados:

$$
u_c=\sqrt{u_1^2+u_2^2+\cdots+u_n^2}
$$

Para evitar aliasing, la frecuencia de muestreo debe superar dos veces el mayor contenido espectral de interés, acompañada de filtrado analógico cuando existan componentes por encima de Nyquist.

## 3. Compatibilidad eléctrica y lógica

La tabla de selección debe responder:

- ¿la salida es analógica, digital, frecuencia, resistencia o corriente?
- ¿qué tensión alimenta el dispositivo y qué niveles entrega?
- ¿requiere `pull-up`, referencia común, divisor, amplificador o aislamiento?
- ¿qué corriente demanda en reposo, medida y arranque?
- ¿qué pines o buses del ESP32 quedan comprometidos?
- ¿la dirección o chip-select evita conflictos?

Para una entrada resistiva con divisor:

$$
V_o=V_{CC}\frac{R_2}{R_1+R_2}
$$

Para accionar una carga inductiva, la etapa de conmutación debe incluir camino de descarga de energía. La energía almacenada es:

$$
E_L=\frac{1}{2}LI^2
$$

## 4. Ejemplo guiado adaptado

**Requisito:** medir 0–60 °C con error de sistema ≤ ±1 °C, periodo de 1 s y cable de 2 m.

1. Se comparan un sensor analógico, uno I²C local y uno digital tolerante a cable.
2. La matriz incluye exactitud en todo el rango, resolución, tensión, corriente, tiempo de conversión, longitud de enlace y disponibilidad.
3. Un sensor con “12 bits” no se elige automáticamente: se verifica que su error absoluto cumpla ±1 °C.
4. Si el cable introduce ruido o caída de tensión, se evalúa interfaz diferencial, salida de corriente o conversión local.
5. La selección queda ligada a una prueba con dos puntos conocidos y repetición.

## 5. Matriz mínima para el ABP

| Criterio | Unidad | Peso sugerido | Fuente de evidencia |
|---|---:|---:|---|
| Rango y sobrecarga | unidad física | eliminatorio | datasheet |
| Error total | ± unidad o % | 25 % | tablas de especificación |
| Compatibilidad eléctrica | V, mA | eliminatorio | máximos absolutos e interfaz |
| Dinámica | ms o Hz | 15 % | timing diagram |
| Consumo | mA, mWh | 15 % | modos de operación |
| Integración | pines/bus | 15 % | diagrama y registros |
| Costo/disponibilidad | COP y plazo | 15 % | cotización |
| Riesgo/calibración | cualitativo | 15 % | plan de prueba |

Los pesos deben derivarse del proyecto; no se usa la suma ponderada para “compensar” un incumplimiento eliminatorio.

## 6. Procedimiento de laboratorio o simulación

1. Definir rango y error permitido antes de buscar referencias.
2. Descargar datasheets del fabricante, no solo fichas comerciales.
3. Identificar máximos absolutos, condiciones recomendadas y características garantizadas.
4. Dibujar en EasyEDA la interfaz completa, incluidas alimentación y protección.
5. Simular el acondicionamiento analógico cuando aplique.
6. Probar valores mínimo, medio, máximo y fuera de rango.
7. Registrar error, repetibilidad, tiempo de respuesta y consumo.

## 7. Diagnóstico de fallas

| Síntoma | Hipótesis | Prueba |
|---|---|---|
| Lectura fija en 0 o escala completa | pin flotante, referencia incorrecta o saturación | medir señal antes del ADC |
| Saltos periódicos | aliasing, ruido de fuente o interferencia de radio | variar muestreo y observar alimentación |
| Dispositivo digital no responde | dirección, niveles o `pull-up` incorrectos | revisar ACK y forma de onda |
| ESP32 se reinicia al actuar | corriente de arranque y retorno compartido | capturar caída de 3,3 V |
| Actuador daña el GPIO | conexión directa o transitorio inductivo | verificar etapa de potencia y diodo |

## 8. Preguntas orientadoras

1. ¿La incertidumbre del sensor deja margen para los demás errores?
2. ¿Qué especificación está garantizada y cuál es solo típica?
3. ¿Qué ocurre durante arranque, desconexión o entrada fuera de rango?
4. ¿Cómo se calibra y cómo se detecta un sensor abierto?
5. ¿Qué evidencia permite defender la selección frente a otra alternativa?

## 9. Trabajo independiente

- Completar tres alternativas de sensor y dos de actuador.
- Anotar sección y página de cada parámetro tomado del datasheet.
- Diseñar la interfaz preliminar en EasyEDA.
- Proponer cuatro casos de prueba, incluido un caso de falla.

## 10. Referencias precisas

- Analog Devices, “Seven Steps to Successful Analog-to-Digital Signal Conversion”, pasos 1–7: rango, ruido, resolución, muestreo y acondicionamiento. [Artículo técnico](https://www.analog.com/en/resources/technical-articles/seven-steps-to-successful-analog-to-digital-signal-conversion.html).
- Analog Devices, *Electronics I and II*, cap. 20 “Analog to Digital Conversion”, §§20.1–20.6. [Texto universitario abierto](https://wiki.analog.com/university/courses/electronics/text/chapter-20).
- Espressif Systems, *ESP32 Series Datasheet*, v5.3, §§2.3–2.5, pp. 17–19; §§4.8–4.9, pp. 36–45; §§5.1–5.4, pp. 51–52. [PDF oficial](https://www.espressif.com/documentation/esp32_datasheet_en.pdf).
- El datasheet del sensor y del actuador concretos del grupo es fuente obligatoria; deben citarse versión, tabla y página usadas.

> Consulta de documentación web: 5 de agosto de 2026. No se reproducen figuras de fabricante.
