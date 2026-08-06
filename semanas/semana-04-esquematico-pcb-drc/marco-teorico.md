# Marco teórico – Semana 04

# Diseño esquemático, footprints, PCB y verificación DRC en EasyEDA

## 1. Propósito

Transformar la arquitectura del sistema en documentación electrónica fabricable. El objetivo no es producir una placa visualmente atractiva, sino un diseño coherente, verificable, ensamblable y mantenible.

## 2. Resultados de aprendizaje

Al finalizar la semana, el estudiante estará en capacidad de:

- Organizar un esquemático por bloques funcionales.
- Verificar símbolos, pines, referencias y valores.
- Seleccionar footprints compatibles con componentes reales.
- Convertir el esquemático en PCB dentro de EasyEDA.
- Ubicar componentes según flujo de señal, alimentación y restricciones mecánicas.
- Definir reglas de ancho, separación, vías y plano de tierra.
- Ejecutar ERC y DRC e interpretar sus advertencias.
- Preparar puntos de prueba y serigrafía útil.

## 3. El esquemático como documento de ingeniería

El esquemático representa relaciones eléctricas, no posiciones físicas. Debe comunicar:

- cómo se alimenta cada bloque;
- qué señales entran y salen;
- qué protecciones existen;
- qué valores y referencias se utilizan;
- qué conectores permiten montaje y prueba;
- qué componentes requieren proximidad.

Una buena práctica es organizar el diseño de izquierda a derecha:

```text
Entrada de energía
      ↓
Protección y regulación
      ↓
ESP32 y lógica
      ↓
Sensores y comunicaciones
      ↓
Etapas de salida
```

## 4. Jerarquía y etiquetas de red

En circuitos medianos, las etiquetas de red reducen cables cruzados y mejoran la lectura. Sin embargo, deben utilizarse nombres inequívocos.

Ejemplos adecuados:

- `+5V_IN`;
- `+3V3`;
- `SENSOR_TEMP`;
- `SPI_SCLK`;
- `UART_TX_RPI`;
- `MOTOR_EN`.

Nombres como `A`, `B` o `SIGNAL` dificultan la revisión.

## 5. Reglas de revisión esquemática

Antes de convertir a PCB se verifica:

1. alimentación de todos los integrados;
2. polaridad de diodos y capacitores;
3. numeración de pines;
4. valores y potencias;
5. conexiones de pines no utilizados;
6. resistencias pull-up o pull-down;
7. desacoplamiento;
8. conectores y orientación;
9. puntos de prueba;
10. referencias únicas;
11. existencia de footprint;
12. compatibilidad con el componente comprado.

## 6. Símbolo y footprint

El símbolo representa la función eléctrica. El footprint representa la geometría física de pads, perforaciones y contorno.

Un error de footprint puede producir una placa eléctricamente correcta pero imposible de ensamblar.

Deben comprobarse:

- paso entre pines;
- diámetro de perforación;
- tamaño de pad;
- orientación del pin 1;
- dimensiones del encapsulado;
- espacio para conectores;
- altura y acceso mecánico.

La verificación debe hacerse con el datasheet y, cuando sea posible, midiendo el componente real.

## 7. Conversión a PCB

EasyEDA puede transferir las redes del esquemático al editor PCB. Antes de hacerlo:

- resolver errores de componentes sin footprint;
- actualizar referencias;
- confirmar conectores;
- revisar unidades;
- definir contorno de placa.

La conversión no realiza el diseño automáticamente. Solo crea los componentes y redes que deben ubicarse y rutearse.

## 8. Ubicación de componentes

La colocación debe seguir criterios funcionales:

### Componentes de alimentación

- cercanos al conector de entrada;
- lazos de corriente cortos;
- regulador y capacitores próximos;
- separación térmica cuando sea necesario.

### Desacoplamiento

Los capacitores cerámicos deben ubicarse junto al pin de alimentación del integrado, con retorno corto a tierra.

### Conectores

Deben quedar accesibles y con orientación lógica respecto al montaje final.

### Sensores

Algunos sensores requieren exposición al ambiente, separación térmica o aislamiento de ruido.

### Antena del ESP32

Si se utiliza un módulo con antena integrada, la zona de antena debe mantenerse libre de cobre, pistas y obstáculos según la recomendación del fabricante.

## 9. Ancho de pista

El ancho depende de corriente, cobre, temperatura permitida y proceso de fabricación. Las pistas de alimentación suelen ser más anchas que las señales.

No existe un ancho universal. Debe definirse una regla para:

- señales digitales;
- alimentación de lógica;
- alimentación de cargas;
- tierra;
- señales sensibles.

## 10. Separación y aislamiento

La separación mínima depende del fabricante y de la tensión. En prototipos de baja tensión, las reglas estándar del fabricante pueden ser suficientes, pero el estudiante debe evitar pistas innecesariamente próximas y mantener distancia de bordes, tornillos y zonas de potencia.

## 11. Planos de tierra

Un plano de tierra puede reducir impedancia de retorno y simplificar el ruteo. No sustituye el análisis de caminos de corriente.

Debe evitarse:

- cortar el plano con muchas pistas;
- dejar islas de cobre sin conexión;
- mezclar retornos de potencia y señales sensibles;
- pasar señales rápidas sobre discontinuidades del plano.

## 12. Vías

Las vías conectan capas. Cada vía agrega resistencia, inductancia y complejidad. Se utilizan cuando mejoran el ruteo, pero no deben colocarse sin criterio.

En alimentación o corriente elevada pueden requerirse varias vías en paralelo.

## 13. ERC y DRC

### ERC

La comprobación de reglas eléctricas detecta problemas del esquemático, como entradas sin conducir, pines de alimentación o conexiones incompatibles.

### DRC

La comprobación de reglas de diseño verifica:

- separación;
- ancho;
- solapamiento;
- vías;
- pads;
- contorno;
- redes sin rutear.

Una advertencia no debe ignorarse automáticamente. Debe clasificarse como:

- error real;
- excepción justificada;
- limitación de la biblioteca;
- conexión pendiente.

## 14. Ejemplo guiado

Para una placa base ESP32 con sensor I2C y salida MOSFET:

1. ubicar conector de alimentación en el borde;
2. colocar protección y regulación cerca;
3. situar el ESP32 en zona central con antena libre;
4. colocar pull-ups I2C cerca del bus;
5. ubicar el conector del sensor accesible;
6. separar la etapa MOSFET de señales analógicas;
7. colocar diodo cerca de la carga inductiva;
8. agregar puntos de prueba en 5 V, 3,3 V, GND, SDA, SCL y salida;
9. rutear alimentación con mayor ancho;
10. llenar plano de tierra y ejecutar DRC.

## 15. Actividad práctica

Cada grupo debe presentar:

- esquemático completo;
- lista de bloques;
- footprints verificados;
- contorno de placa;
- ubicación inicial;
- reglas DRC definidas;
- ruteo de alimentación;
- plano de tierra;
- capturas 2D y 3D;
- reporte de errores y correcciones.

## 16. Conexión con el ABP

La placa base es la infraestructura física del proyecto. Debe permitir:

- alimentación segura;
- conexión del ESP32;
- sensores intercambiables;
- actuadores protegidos;
- acceso a comunicaciones;
- medición y diagnóstico.

No se evalúa solamente que el DRC muestre cero errores. Se evalúa que las decisiones sean explicables.

## 17. Diagnóstico de fallas de diseño

Antes de fabricar se debe provocar una revisión sistemática:

- comprobar continuidad de cada red importante;
- buscar pines invertidos;
- revisar conectores reflejados;
- verificar polaridad;
- comparar footprint con datasheet;
- inspeccionar zonas de antena;
- confirmar acceso a botones y puertos;
- revisar pistas de alimentación;
- confirmar que el contorno esté cerrado.

## 18. Errores comunes

- Confiar ciegamente en bibliotecas comunitarias.
- Elegir footprint por nombre sin revisar dimensiones.
- Colocar capacitores lejos del integrado.
- Rutear señales debajo de la antena.
- Ignorar pistas sin conectar.
- Usar un único ancho para todo.
- Crear serigrafía sobre pads.
- No dejar puntos de prueba.
- Diseñar conectores sin considerar el montaje real.
- Interpretar la vista 3D como validación eléctrica.

## 19. Trabajo independiente

- Corregir ERC y DRC.
- Revisar el PCB con otro grupo.
- Imprimir el diseño a escala 1:1 y colocar componentes reales sobre la impresión.
- Preparar archivos Gerber y BOM para la Semana 05.
- Registrar todas las decisiones en la bitácora.

## 20. Referencias de apoyo

- EasyEDA Std User Guide: captura esquemática, conversión a PCB, reglas DRC y generación de Gerber.
- Datasheets y dibujos mecánicos de los componentes.
- Guía de hardware del módulo ESP32 seleccionado.
- `SYLLABUS.md` y `ABP_PROYECTO_DE_CURSO.md`.
