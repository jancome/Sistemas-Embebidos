# Marco teórico – Semana 03

# Alimentación, regulación, desacoplamiento y protecciones

## 1. Propósito

Diseñar la alimentación del nodo embebido con criterios de ingeniería. La fuente no es un elemento secundario: condiciona la estabilidad del ADC, el funcionamiento de las comunicaciones, la vida útil de los componentes y la seguridad del prototipo.

## 2. Resultados de aprendizaje

Al finalizar la semana, el estudiante estará en capacidad de:

- Elaborar un presupuesto de corriente y potencia.
- Diferenciar regulador lineal y convertidor conmutado.
- Seleccionar tensión de entrada, salida y margen de corriente.
- Calcular disipación aproximada de un regulador.
- Definir capacitores de entrada, salida y desacoplamiento.
- Incorporar protección por polaridad, sobrecorriente y transitorios.
- Separar alimentación lógica y alimentación de potencia cuando corresponda.
- Representar la cadena de energía en EasyEDA.

## 3. Presupuesto de potencia

El consumo total no se obtiene sumando valores típicos sin contexto. Deben considerarse condiciones máximas, picos de transmisión, arranque de cargas y margen de diseño.

```text
Itotal = IESP32 + Isensores + Iinterfaces + Iindicadores + Iactuadores
```

La potencia de una carga de corriente continua es:

```text
P = V × I
```

La fuente debe incluir un margen razonable. Usar una fuente exactamente igual al consumo calculado deja al sistema sin capacidad para soportar tolerancias, picos o ampliaciones.

## 4. Dominios de alimentación

Un proyecto puede tener varios niveles:

- entrada principal;
- 5 V para módulos;
- 3,3 V para lógica;
- tensión independiente para motores o relés;
- referencia analógica.

Estos dominios deben identificarse con etiquetas claras y un retorno de corriente definido.

## 5. Reguladores lineales

Un regulador lineal reduce tensión disipando la diferencia en forma de calor.

```text
Pregulador = (Vin - Vout) × Iout
```

Ejemplo:

```text
Vin = 12 V
Vout = 5 V
Iout = 0,3 A
Pregulador = 2,1 W
```

Ese nivel de disipación puede exigir disipador y vuelve poco eficiente la solución. También debe comprobarse el `dropout`, es decir, la diferencia mínima entre entrada y salida necesaria para regular.

Ventajas:

- simplicidad;
- bajo ruido en muchas aplicaciones;
- pocos componentes.

Limitaciones:

- baja eficiencia con gran diferencia de tensión;
- calentamiento;
- corriente limitada.

## 6. Convertidores DC-DC

Los convertidores conmutados transfieren energía mediante elementos de conmutación y almacenamiento.

- Buck: reduce tensión.
- Boost: eleva tensión.
- Buck-boost: puede elevar o reducir, según topología.

La potencia de entrada aproximada depende de la eficiencia:

```text
Pin ≈ Pout / η
```

Aunque son más eficientes, requieren atención a rizado, disposición de componentes, lazos de corriente y compatibilidad electromagnética.

## 7. Desacoplamiento

Los capacitores de desacoplamiento suministran corriente local durante cambios rápidos y reducen perturbaciones en la alimentación.

Buenas prácticas:

- colocar un capacitor cerámico de 100 nF cerca de cada integrado;
- utilizar capacitores de mayor valor cerca de módulos o cargas pulsantes;
- mantener conexiones cortas hacia VCC y GND;
- respetar polaridad en capacitores electrolíticos;
- seguir el datasheet del regulador.

Un capacitor mal ubicado puede ser poco eficaz aunque su valor sea correcto.

## 8. Filtrado

Un filtro simple puede atenuar ruido, pero debe diseñarse según la frecuencia de interés y la impedancia de la carga.

Para un filtro RC de primer orden:

```text
fc = 1 / (2πRC)
```

Este filtro puede utilizarse en señales o alimentaciones de baja corriente, pero no reemplaza el diseño correcto de la fuente.

## 9. Protección por polaridad inversa

Opciones comunes:

- diodo en serie;
- diodo en paralelo con fusible;
- MOSFET de protección;
- conector polarizado.

Cada opción tiene ventajas y pérdidas. Un diodo en serie es sencillo, pero introduce caída de tensión y disipación.

## 10. Protección por sobrecorriente

Se pueden emplear:

- fusible;
- fusible rearmable PTC;
- limitador electrónico;
- fuente con protección;
- resistencia fusible.

La protección se selecciona según corriente normal, corriente de falla, velocidad requerida y energía disponible.

## 11. Protección de cargas inductivas

Motores, relés, válvulas y bobinas almacenan energía magnética. Al interrumpir la corriente pueden producir una sobretensión.

Una solución básica para una carga DC es el diodo de rueda libre:

```text
Cátodo → positivo de la carga
Ánodo  → lado conmutado por el transistor
```

La selección debe considerar corriente y tensión inversa.

## 12. Tierra y retorno de corriente

La tierra no es un punto ideal sin impedancia. Toda corriente retorna a la fuente por un camino físico.

Problemas frecuentes:

- compartir un camino del motor con el ADC;
- pistas delgadas en alimentación;
- lazos largos;
- ubicación incorrecta del capacitor;
- falta de plano de tierra;
- conectar dominios sin estrategia.

La corriente de potencia debe evitar atravesar zonas sensibles.

## 13. Ejemplo guiado

Un nodo contiene:

- ESP32: 250 mA máximos estimados durante transmisión;
- sensor: 20 mA;
- display: 80 mA;
- LED y periféricos: 30 mA;
- margen: 30 %.

```text
Ibase = 250 + 20 + 80 + 30 = 380 mA
Ifuente ≈ 380 × 1,3 = 494 mA
```

Se seleccionaría una fuente de al menos 5 V y 0,5 A, aunque en la práctica puede elegirse 1 A para margen adicional. Si además existe un motor, su fuente y corriente de arranque se analizan por separado.

## 14. Actividad práctica

Cada grupo debe:

1. listar todos los bloques;
2. extraer consumo típico y máximo de datasheets;
3. calcular corriente total;
4. seleccionar fuente;
5. definir regulación;
6. calcular disipación;
7. agregar desacoplamiento;
8. seleccionar protección;
9. dibujar el diagrama de potencia;
10. medir tensión sin carga y bajo carga.

## 15. Conexión con EasyEDA y el ABP

La cadena de alimentación debe aparecer en el esquemático con:

- conectores identificados;
- protección de entrada;
- regulador;
- capacitores;
- indicadores;
- etiquetas de red;
- puntos de prueba;
- separación entre lógica y potencia.

La evidencia no es solo el diagrama. Debe incluir cálculos, selección de partes y mediciones.

## 16. Diagnóstico de fallas

Si el ESP32 se reinicia al transmitir:

1. medir tensión durante el evento;
2. comprobar capacidad de la fuente;
3. revisar cable USB o conductor;
4. medir caída en regulador;
5. revisar desacoplamiento;
6. separar temporalmente cargas;
7. observar ruido con osciloscopio;
8. comprobar tierra.

Si la lectura ADC cambia al activar una carga:

- revisar retorno de corriente;
- separar alimentación;
- mejorar filtrado;
- verificar referencia;
- reducir acoplamiento entre pistas;
- medir el ruido real antes de modificar valores al azar.

## 17. Errores comunes

- Usar corriente típica como corriente máxima.
- Ignorar picos de Wi-Fi o arranque.
- Conectar motor y lógica a la misma fuente sin análisis.
- Colocar capacitores lejos del integrado.
- Seleccionar regulador sin revisar disipación.
- No verificar tensión máxima de entrada.
- Confiar en que un cable USB siempre entrega la corriente necesaria.
- Diseñar la tierra como una etiqueta y no como un camino físico.

## 18. Trabajo independiente

- Completar presupuesto de potencia.
- Seleccionar componentes reales y footprints.
- Preparar la etapa de alimentación en EasyEDA.
- Simular o medir una condición de carga.
- Registrar riesgos térmicos y eléctricos.

## 19. Referencias de apoyo

- Datasheets de reguladores y fuentes seleccionadas.
- Documentación oficial de ESP32 sobre alimentación y hardware.
- EasyEDA, documentación oficial de esquemáticos y PCB.
- `MATERIALES.md`, `NORMAS_DE_CLASE.md` y `ABP_PROYECTO_DE_CURSO.md`.
