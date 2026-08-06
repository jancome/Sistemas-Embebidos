# Marco teórico – Semana 07

# Bus SPI e integración de periféricos con ESP32

## 1. Propósito

Comprender SPI como una interfaz síncrona que exige coherencia entre conexiones, modo temporal, frecuencia y formato de datos. El objetivo no es únicamente lograr que una librería entregue valores, sino interpretar la transacción y verificarla mediante evidencia.

## 2. Resultados de aprendizaje

Al finalizar la semana, el estudiante estará en capacidad de:

- Explicar las señales MOSI, MISO, SCLK y CS.
- Diferenciar comunicación síncrona y asíncrona.
- Seleccionar modo SPI, frecuencia y orden de bits.
- Leer una secuencia de transacción desde un datasheet.
- Integrar un periférico SPI con ESP32.
- Capturar e interpretar señales con analizador lógico.
- Diagnosticar errores de cableado, selección y temporización.

## 3. Arquitectura del bus SPI

SPI utiliza normalmente un controlador y uno o varios periféricos.

```text
ESP32                     Periférico
SCLK  ──────────────────→ SCLK
MOSI  ──────────────────→ SDI / MOSI
MISO  ←────────────────── SDO / MISO
CS    ──────────────────→ CS / SS
GND   ─────────────────── GND
```

- `SCLK`: reloj generado por el controlador.
- `MOSI`: datos desde el controlador hacia el periférico.
- `MISO`: datos desde el periférico hacia el controlador.
- `CS`: selecciona el periférico.

Algunos dispositivos usan tres hilos, datos bidireccionales o nombres diferentes. Siempre debe consultarse el datasheet.

## 4. Comunicación síncrona

En SPI, el reloj indica cuándo se presenta y cuándo se captura cada bit. No existe un único modo universal. El controlador y el periférico deben coincidir en:

- polaridad del reloj —CPOL—;
- fase del reloj —CPHA—;
- frecuencia;
- orden de bits;
- longitud de palabra;
- comportamiento de CS.

## 5. Modos SPI

Los cuatro modos surgen de combinar CPOL y CPHA:

| Modo | CPOL | CPHA |
|---:|---:|---:|
| 0 | 0 | 0 |
| 1 | 0 | 1 |
| 2 | 1 | 0 |
| 3 | 1 | 1 |

CPOL define el estado inactivo del reloj. CPHA define en qué transición se captura el dato. El modo correcto se obtiene del datasheet.

## 6. Frecuencia

El periférico especifica una frecuencia máxima. La comunicación puede fallar aunque el cableado sea correcto si:

- la frecuencia excede el límite;
- los cables son largos;
- existen problemas de integridad de señal;
- el montaje en protoboard introduce capacitancia;
- el firmware no respeta tiempos entre comandos.

Para depurar, es útil comenzar con una frecuencia baja y aumentarla después.

## 7. Chip Select

CS identifica el periférico activo. En muchos dispositivos es activo en bajo:

```text
CS = 0 → transacción activa
CS = 1 → periférico no seleccionado
```

Al compartir SCLK, MOSI y MISO entre varios periféricos, cada uno requiere normalmente su propio CS. Si dos periféricos activan MISO al mismo tiempo, puede existir contención.

## 8. Comandos y registros

Una transacción típica puede contener:

```text
CS bajo
→ byte de comando
→ dirección de registro
→ datos de escritura o bytes ficticios
→ respuesta
→ CS alto
```

Los detalles varían. Algunos dispositivos incorporan el bit de lectura/escritura en la dirección. Otros requieren varios bytes o una pausa.

## 9. Orden de bits y bytes

Se debe diferenciar:

- bit más significativo primero o menos significativo primero;
- orden de bytes en palabras de 16 o 32 bits;
- signo del dato;
- campos empaquetados.

Ejemplo para dos bytes:

```cpp
uint16_t raw = (static_cast<uint16_t>(highByte) << 8) | lowByte;
```

Si el periférico entrega orden inverso, la unión debe adaptarse.

## 10. Integridad eléctrica

Antes de conectar:

- verificar tensión lógica;
- compartir GND cuando corresponda;
- evitar entradas de 5 V al ESP32;
- mantener cables cortos;
- usar desacoplamiento;
- revisar pull-ups/pull-downs exigidos;
- evitar alimentar el periférico desde un GPIO.

SPI no define por sí mismo niveles de tensión ni conectores.

## 11. Analizador lógico

El analizador permite observar:

- frecuencia;
- modo;
- activación de CS;
- bytes transmitidos;
- respuesta;
- pausas;
- repetición de comandos.

Una captura es más útil cuando se relaciona con el datasheet. No basta con mostrar una pantalla sin explicar qué significa cada byte.

## 12. Ejemplo guiado

Un periférico hipotético tiene:

- modo 0;
- máximo 5 MHz;
- comando `0x80 | dirección` para lectura;
- registro de identidad en `0x0F`;
- valor esperado `0x42`.

Secuencia:

1. configurar SPI en modo 0 a 500 kHz;
2. colocar CS en bajo;
3. transmitir `0x8F`;
4. transmitir `0x00` para generar reloj;
5. leer respuesta;
6. colocar CS en alto;
7. comparar con `0x42`.

Si se recibe `0xFF`, puede existir MISO desconectado o pull-up. Si se recibe `0x00`, puede existir corto, periférico sin alimentación o modo incorrecto.

## 13. Actividad práctica

Cada grupo debe:

1. identificar pinout y tensión;
2. indicar modo y frecuencia máxima;
3. dibujar la conexión;
4. realizar una lectura de identificación;
5. capturar la transacción;
6. explicar cada byte;
7. modificar el modo o frecuencia para provocar un error;
8. restaurar la configuración correcta;
9. integrar el periférico al driver de la Semana 06.

## 14. Conexión con el ABP

El periférico debe tener una función real:

- memoria externa;
- pantalla;
- ADC;
- sensor;
- interfaz de comunicación;
- convertidor o expansor.

La evidencia debe demostrar:

```text
requisito → periférico → registro/comando → transacción → dato útil
```

## 15. Diagnóstico de fallas

Orden recomendado:

1. alimentación;
2. tierra;
3. pinout;
4. CS;
5. presencia de reloj;
6. datos MOSI;
7. respuesta MISO;
8. modo;
9. frecuencia;
10. orden de bits;
11. secuencia del datasheet;
12. prueba de registro de identidad.

## 16. Errores comunes

- Confundir MOSI y MISO.
- Usar el modo por defecto sin revisar el datasheet.
- Dejar CS flotante.
- Compartir CS entre periféricos.
- Exceder la frecuencia máxima.
- No colocar bytes ficticios para leer.
- Interpretar mal el orden de bytes.
- Usar cables largos en protoboard.
- Conectar un periférico de 5 V directamente.
- Depender de una librería sin comprender la transacción.

## 17. Trabajo independiente

- Documentar el protocolo del periférico.
- Añadir manejo de timeout y respuesta inválida.
- Integrar la lectura al servicio de adquisición.
- Preparar una captura comentada.
- Relacionar el periférico con la arquitectura inalámbrica de la Semana 08.

## 18. Referencias de apoyo

- Datasheet del periférico SPI.
- Documentación oficial de ESP32 sobre SPI.
- Documentación de la herramienta de análisis lógico.
- `SYLLABUS.md` y `guias-laboratorio/lab-05-spi/README.md`.
