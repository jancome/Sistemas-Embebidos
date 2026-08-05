# Marco teórico – Semana 03

## Alimentación, regulación, desacoplamiento y protección

### Propósito formativo

La alimentación es una función del sistema, no un accesorio. Una tensión nominal correcta puede fallar por corriente insuficiente, transitorios, caída en conductores, disipación o retorno compartido. Esta semana convierte el consumo de cada bloque en una red de potencia verificable para el PCB de EasyEDA.

## 1. Presupuesto de corriente y potencia

Se distinguen corriente típica, máxima continua y pico. Para una fuente común:

$$
I_{fuente}\geq M\sum I_{max,i}
$$

donde $M>1$ es margen de diseño justificado. La potencia de entrada debe considerar eficiencia:

$$
P_{in}=\frac{P_{out}}{\eta}, \qquad I_{in}=\frac{P_{out}}{\eta V_{in}}
$$

Los picos de radio del ESP32 y los arranques de motores o relés se evalúan en la escala temporal correspondiente; un multímetro lento puede ocultarlos.

## 2. Regulador lineal frente a convertidor conmutado

En un regulador lineal aproximado:

$$
P_D=(V_{in}-V_{out})I_{out}
$$

$$
T_J=T_A+P_D\theta_{JA}
$$

Si la temperatura de unión estimada se aproxima al límite, se cambia encapsulado, área de cobre, corriente o topología. Un convertidor conmutado suele ofrecer mayor eficiencia con grandes diferencias de tensión, pero exige seleccionar inductor, diodo/MOSFET, capacitores y trazado siguiendo su datasheet.

La caída en cables y pistas es:

$$
\Delta V=IR, \qquad R=\rho\frac{l}{A}
$$

## 3. Desacoplamiento y retorno de corriente

Un capacitor local entrega carga durante cambios rápidos:

$$
\Delta V\approx\frac{I\Delta t}{C}
$$

La ecuación orienta el orden de magnitud, pero el capacitor real tiene ESR y ESL. Por eso se combina capacitancia de reserva cerca de la entrada con capacitores cerámicos próximos a los pines, conectados mediante un lazo corto hacia tierra.

La corriente siempre retorna a su fuente. Una pista de señal sobre un plano continuo ofrece un retorno cercano; una ranura en el plano obliga a rodeos, aumenta el área del lazo y favorece ruido y emisiones. No debe separarse tierra analógica y digital sin comprender por dónde cerrará cada corriente.

## 4. Protecciones mínimas

- polaridad inversa: diodo o MOSFET de protección;
- sobrecorriente: fusible o elemento rearmable dimensionado por carga y conductor;
- transitorios: TVS seleccionada por tensión de trabajo, sujeción y energía;
- carga inductiva: diodo de rueda libre o red de supresión;
- entradas externas: resistencia serie, limitación, filtro y ESD cuando corresponda;
- conectores: pinout inequívoco, tierra suficiente y secuencia segura.

Un componente de protección se selecciona para que su tensión de operación no interfiera con el uso normal y su tensión de sujeción permanezca por debajo de lo tolerable por el circuito protegido.

## 5. Ejemplo guiado adaptado

Una entrada de 12 V alimenta un ESP32 (pico de 500 mA en la rama de 3,3 V), un sensor de 40 mA y un actuador de 12 V/600 mA.

1. Potencia lógica máxima: $3.3(0.54)=1.78\,W$.
2. Con un buck de 85 %, demanda aproximada desde 12 V: $1.78/(0.85\cdot12)=0.175\,A$.
3. Corriente de entrada conjunta aproximada: $0.175+0.600=0.775\,A$, antes del margen.
4. Se separan las ramas de lógica y actuador después de la protección de entrada.
5. Se colocan desacoplamientos locales y se dirige el retorno del actuador lejos de la referencia del sensor.
6. Se prueba con el actuador conmutando mientras se mide el mínimo de la línea de 3,3 V y se vigilan reinicios.

## 6. Flujo de diseño en EasyEDA

1. Crear bloques de entrada, protección, regulación, lógica y carga.
2. Nombrar cada red de potencia y no usar símbolos ambiguos.
3. Añadir valores, encapsulados, tensión y potencia nominal.
4. Ubicar conectores, fusible y TVS cerca del punto de entrada.
5. Definir reglas de ancho por clase de red.
6. Añadir puntos de prueba para entrada, salidas reguladas y tierra.
7. Ejecutar ERC y revisar manualmente corrientes y máximos absolutos.

## 7. Procedimiento de medición

1. Encender con límite de corriente y sin cargas sensibles.
2. Verificar polaridad y tensiones en vacío.
3. Aumentar carga por pasos y registrar $V$, $I$ y temperatura.
4. Conectar el ESP32 y observar arranque y transmisión inalámbrica.
5. Conmutar el actuador; capturar mínimo y rizado de 3,3 V con osciloscopio.
6. Interrumpir y restablecer alimentación para verificar un arranque limpio.

## 8. Diagnóstico de fallas

| Síntoma | Causa probable | Evidencia buscada | Acción |
|---|---|---|---|
| Reinicio al transmitir | caída transitoria en 3,3 V | mínimo de tensión coincidente | mejorar fuente, reserva y trazado |
| Regulador muy caliente | disipación o carga excesiva | $P_D$ y temperatura | cambiar topología o cobre |
| ADC ruidoso al accionar | retorno compartido | correlación ruido–corriente | rediseñar retorno y filtrado |
| Fusible actúa al arrancar | pico no considerado | corriente de irrupción | seleccionar curva y capacidad |
| TVS se calienta normalmente | tensión de trabajo incorrecta | corriente con entrada nominal | corregir selección |

## 9. Preguntas orientadoras y trabajo independiente

1. ¿Qué componente fija el peor pico y cuánto dura?
2. ¿Cuál es el camino completo de la corriente de carga y retorno?
3. ¿Qué falla abre el fusible y qué falla no puede resolver?
4. ¿Dónde se medirá cada riel sin provocar un corto?

Entregar presupuesto de potencia con fuentes, cálculo térmico, esquema EasyEDA, justificación de protecciones y plan de cinco mediciones.

## 10. Referencias precisas

- Espressif Systems, *ESP32 Hardware Design Guidelines*, Release master (21 julio 2026), §1.3.2 “Power Supply”, pp. 5–7; §1.3.3, pp. 7–8; §§1.4.1–1.4.2, pp. 19–22. [PDF oficial](https://documentation.espressif.com/esp-hardware-design-guidelines/en/latest/esp32/esp-hardware-design-guidelines-en-master-esp32.pdf).
- Espressif Systems, *ESP32 Series Datasheet*, v5.3, §2.5, pp. 17–19; §5.1–5.4, pp. 51–52. [PDF oficial](https://www.espressif.com/documentation/esp32_datasheet_en.pdf).
- Lee y Seshia, *Introduction to Embedded Systems*, 2.ª ed., cap. 9 “Memory Architectures” y cap. 10 “Input and Output”, para interacción entre cómputo y hardware. [UC Berkeley](https://ptolemy.berkeley.edu/books/leeseshia/).
- Datasheet del regulador y de cada protección elegida: sección “Recommended operating conditions”, diseño típico, selección de componentes y guía de layout.

> Las cifras del ejemplo son didácticas; cada equipo debe sustituirlas por datos garantizados de sus componentes.
