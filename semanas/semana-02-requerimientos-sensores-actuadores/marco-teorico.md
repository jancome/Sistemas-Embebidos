# Marco teórico – Semana 02

# Requerimientos, sensores, actuadores e interfaces eléctricas

## 1. Propósito

Convertir la necesidad del proyecto en especificaciones técnicas y seleccionar sensores y actuadores con base en datos verificables. La decisión no debe depender de que un módulo sea popular o económico; debe responder a rango, exactitud, interfaz, alimentación, disponibilidad y condiciones de operación.

## 2. Resultados de aprendizaje

Al finalizar la semana, el estudiante estará en capacidad de:

- Formular requisitos medibles y criterios de aceptación.
- Diferenciar sensibilidad, resolución, exactitud, precisión y rango.
- Interpretar parámetros básicos de un datasheet.
- Comparar sensores analógicos y digitales.
- Determinar si un actuador requiere transistor, MOSFET, relé o driver.
- Definir interfaces eléctricas compatibles con el ESP32.
- Elaborar una matriz de selección justificada.

## 3. De la necesidad al requisito

Una necesidad describe el problema; un requisito establece lo que el sistema debe hacer.

Ejemplo poco verificable:

> El sistema debe medir bien la temperatura.

Ejemplo verificable:

> El sistema debe medir temperaturas entre 10 °C y 60 °C con resolución de 0,5 °C y actualizar el dato cada 5 segundos.

Un requisito debe contener, cuando aplique:

- variable;
- rango;
- unidad;
- tolerancia;
- frecuencia de actualización;
- condición de operación;
- respuesta esperada;
- método de prueba.

## 4. Parámetros metrológicos básicos

### Rango

Intervalo de valores que el sensor puede medir.

### Resolución

Cambio mínimo que el sistema puede representar o detectar.

### Exactitud

Cercanía entre el valor medido y el valor real o de referencia.

### Precisión

Capacidad de producir resultados cercanos entre sí al repetir una medición.

### Sensibilidad

Relación entre el cambio de salida y el cambio de entrada:

```text
S = Δsalida / Δentrada
```

### Linealidad

Grado en que la salida sigue una relación aproximadamente lineal con la variable de entrada.

### Histéresis

Diferencia de respuesta cuando la variable aumenta y cuando disminuye.

### Tiempo de respuesta

Tiempo necesario para que la salida represente un cambio de entrada dentro de un margen definido.

## 5. Sensores analógicos y digitales

### Sensor analógico

Entrega una tensión, corriente, resistencia o frecuencia relacionada con la variable. Puede requerir:

- divisor resistivo;
- amplificación;
- filtrado;
- protección;
- adaptación al ADC;
- calibración.

### Sensor digital

Entrega datos mediante una interfaz o un nivel lógico. Puede usar:

- GPIO;
- I2C;
- SPI;
- UART;
- pulsos;
- salida de colector abierto.

Un sensor digital no elimina la necesidad de revisar alimentación, niveles lógicos, tiempos y resistencias de polarización.

## 6. Conversión analógica-digital

Para una entrada ADC ideal de `N` bits y rango de referencia `Vref`, la resolución teórica es:

```text
Resolución = Vref / (2^N - 1)
```

Ejemplo: para 12 bits y 3,3 V:

```text
Resolución ≈ 3,3 / 4095 ≈ 0,806 mV por cuenta
```

Este valor no equivale automáticamente a exactitud. El ruido, la no linealidad, la referencia, la impedancia de la fuente y la calibración afectan el resultado real.

## 7. Muestreo

La frecuencia de muestreo debe ser suficiente para seguir los cambios de la variable. Una temperatura ambiental puede medirse lentamente; una vibración requiere una frecuencia mucho mayor.

El estudiante debe preguntar:

- ¿qué tan rápido cambia la variable?;
- ¿se necesita detectar picos?;
- ¿qué latencia admite el control?;
- ¿qué cantidad de datos se generará?;

No tiene sentido medir miles de veces por segundo una variable que cambia lentamente, porque se desperdician energía, memoria y ancho de banda.

## 8. Actuadores e indicadores

Un actuador transforma una señal eléctrica en una acción física. Ejemplos:

- LED;
- zumbador;
- relé;
- motor;
- válvula;
- resistencia calefactora;
- servomotor.

La salida GPIO no debe considerarse una fuente de potencia. Debe revisarse:

- tensión de la carga;
- corriente nominal y de arranque;
- tipo de carga: resistiva, inductiva o capacitiva;
- necesidad de aislamiento;
- frecuencia de conmutación;
- disipación;
- protección contra transitorios.

## 9. Etapa de potencia

Una arquitectura típica es:

```text
GPIO ESP32
    ↓
Resistencia de control
    ↓
Transistor o MOSFET
    ↓
Carga y fuente independiente
```

Para una carga inductiva se incorpora un diodo de rueda libre o una protección equivalente. La tierra debe compartirse cuando la topología lo requiera, o aislarse mediante optoacoplamiento cuando sea necesario.

## 10. Compatibilidad eléctrica

Antes de conectar un sensor o módulo al ESP32 se comprueba:

- alimentación permitida;
- nivel lógico de salida;
- corriente de entrada o salida;
- existencia de pull-up o pull-down;
- tolerancia a 5 V;
- pinout;
- condiciones de arranque.

El ESP32 utiliza lógica de 3,3 V. Una salida de 5 V no debe conectarse directamente sin comprobar la tolerancia del pin o incorporar adaptación de nivel.

## 11. Ejemplo guiado

### Necesidad

Detectar sobretemperatura en un gabinete electrónico y activar ventilación.

### Requisitos posibles

- rango: 20 °C a 80 °C;
- resolución mínima: 1 °C;
- actualización: 2 segundos;
- activar ventilador al superar 45 °C;
- mantener alarma local si se pierde la red;
- registrar fecha y temperatura;
- alimentación del nodo: 5 V.

### Comparación de sensores

| Criterio | Sensor A | Sensor B | Sensor C |
|---|---:|---:|---:|
| Rango | suficiente | suficiente | limitado |
| Interfaz | analógica | I2C | 1-Wire |
| Alimentación | compatible | compatible | compatible |
| Exactitud | media | alta | media |
| Costo | bajo | medio | bajo |
| Disponibilidad | alta | media | alta |

La elección final debe justificar el equilibrio entre desempeño, integración y costo.

### Actuador

Un ventilador no se conecta directamente al GPIO. Se necesita MOSFET, diodo de protección si corresponde, fuente de carga y tierra común o aislamiento.

## 12. Actividad práctica

Cada grupo debe:

1. formular requisitos funcionales y no funcionales;
2. identificar tres sensores candidatos;
3. identificar dos actuadores o indicadores;
4. consultar datasheets;
5. construir una matriz comparativa;
6. seleccionar una alternativa;
7. dibujar la interfaz eléctrica;
8. registrar riesgos y pruebas.

## 13. Conexión con el ABP

La selección de esta semana condiciona todo el proyecto. Un sensor incompatible obliga a rediseñar la placa; un actuador subdimensionado puede dañar el sistema; una frecuencia de muestreo mal definida puede generar datos inútiles.

La evidencia debe mostrar la relación:

```text
requisito → parámetro del componente → circuito de interfaz → prueba
```

## 14. Diagnóstico de fallas

Cuando un sensor no entrega datos:

1. comprobar alimentación y tierra;
2. verificar pinout;
3. medir la salida o línea de comunicación;
4. revisar niveles lógicos;
5. comprobar resistencias pull-up/pull-down;
6. probar un código mínimo;
7. comparar con una referencia conocida;
8. sustituir temporalmente el sensor.

Cuando un actuador no responde:

1. verificar fuente de la carga;
2. medir señal de control;
3. comprobar transistor o driver;
4. revisar polaridad y diodo;
5. medir corriente;
6. probar la carga por separado con una fuente segura.

## 15. Errores comunes

- Elegir por precio sin verificar especificaciones.
- Confundir resolución con exactitud.
- Suponer que un módulo de 5 V entrega lógica de 3,3 V.
- Conectar motores o relés directamente a GPIO.
- Ignorar corriente de arranque.
- Copiar un circuito de internet sin revisar el datasheet.
- No considerar disponibilidad real del componente.
- Definir una frecuencia de muestreo sin relación con la variable.

## 16. Trabajo independiente

- Completar la matriz de selección.
- Descargar y archivar datasheets.
- Identificar símbolo y footprint de cada componente.
- Estimar consumo máximo.
- Preparar la cadena de alimentación de la Semana 03.

## 17. Referencias de apoyo

- Datasheets oficiales de los componentes seleccionados.
- Documentación oficial de ESP32 sobre GPIO, ADC e interfaces.
- `SYLLABUS.md`, `MATERIALES.md` y `ABP_PROYECTO_DE_CURSO.md`.
