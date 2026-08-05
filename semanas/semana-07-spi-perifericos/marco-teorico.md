# Marco teórico – Semana 07

## SPI: temporización, transacciones y evidencia

### Propósito formativo

SPI no define por sí solo el significado de los bytes. El bus aporta reloj, desplazamiento y selección; el datasheet del periférico define comandos, registros, fases, límites temporales y respuesta. Una integración válida demuestra ambas capas con evidencia observable.

## 1. Señales y topología

- `SCLK`: reloj generado por el controlador/host.
- `MOSI`: datos desde host hacia periférico.
- `MISO`: datos desde periférico hacia host.
- `CS`: selección individual, normalmente activa en bajo.

Varios dispositivos pueden compartir reloj y datos si cada uno tiene `CS` independiente y libera MISO cuando no está seleccionado. Deben compartir referencia de tierra y usar niveles compatibles.

La tasa bruta de una transacción de $N$ bits es:

$$
T_{bits}=\frac{N}{f_{SCLK}}
$$

El rendimiento efectivo incluye selección, comando, dirección, bytes ficticios, pausas y software:

$$
R_{ef}=\frac{N_{datos}}{T_{CS}+T_{comando}+T_{datos}+T_{software}}
$$

## 2. CPOL y CPHA

`CPOL` define el nivel de reposo del reloj; `CPHA`, el borde usado para capturar respecto del borde de lanzamiento. Los cuatro modos son pares `(CPOL, CPHA)`: 0 `(0,0)`, 1 `(0,1)`, 2 `(1,0)` y 3 `(1,1)`.

No se selecciona el modo “por prueba y error”: se interpreta el diagrama temporal del datasheet. La captura debe ocurrir cuando el dato es estable, después del tiempo de establecimiento y antes del tiempo de retención requeridos.

## 3. Estructura de una transacción

Una operación puede contener:

```text
CS↓ | comando R/W | dirección | dummy | datos | CRC opcional | CS↑
```

Las decisiones de diseño incluyen orden de bits, endianness de palabras multibyte, polaridad de `CS`, frecuencia máxima, tiempo entre transacciones y si `CS` debe permanecer activo durante toda la ráfaga.

En el ESP32 clásico, SPI0/SPI1 están asociados internamente a memoria; SPI2/SPI3 son los controladores de propósito general según la documentación de Espressif. La asignación real depende del framework y del módulo.

## 4. Integridad eléctrica

Frecuencias mayores reducen margen frente a longitud, capacitancia, desadaptación y tiempos de subida. Los cables de protoboard no representan un PCB corto. Si aparecen errores al elevar frecuencia:

- reducir longitud y mejorar tierra;
- comprobar nivel y amplitud;
- disminuir frecuencia;
- revisar carga y múltiples derivaciones;
- considerar resistencia serie cerca del transmisor;
- verificar que MISO no tenga contención.

## 5. Ejemplo guiado adaptado

Un periférico usa modo 3, comando de 8 bits, dirección de 8 bits y dato de 16 bits a 2 MHz.

1. Bits mínimos: $8+8+16=32$.
2. Tiempo ideal: $32/2\,MHz=16\,\mu s$.
3. El datasheet exige `CS` alto 5 µs entre lecturas: mínimo físico 21 µs sin contar software.
4. Los bytes leídos `0x01 0x90` producen `raw=0x0190=400`.
5. Si la escala es 0,1 unidad/LSB, resultado = 40,0 unidades.
6. Se captura `CS`, `SCLK`, `MOSI` y `MISO`; la evidencia debe mostrar modo, comando, respuesta y frecuencia.

## 6. Procedimiento de laboratorio

1. Construir tabla de temporización desde el datasheet.
2. Verificar 3,3 V, tierra y continuidad con el sistema apagado.
3. Iniciar a frecuencia conservadora.
4. Leer un registro de identidad o valor de reset conocido.
5. Capturar una transacción y decodificarla manualmente.
6. Comparar bytes con monitor serial y conversión del driver.
7. Probar frecuencia, cable desconectado, `CS` incorrecto y respuesta fuera de rango.

## 7. Diagnóstico

| Captura/síntoma | Interpretación | Siguiente prueba |
|---|---|---|
| No hay reloj | driver no ejecuta o pin equivocado | revisar inicialización/GPIO |
| Reloj existe, `CS` no baja | selección mal configurada | controlar `CS` manualmente |
| MISO siempre alto | dispositivo ausente o línea flotante | alimentación y continuidad |
| Bits desplazados | CPHA/modo incorrecto | comparar bordes con datasheet |
| Funciona solo lento | margen eléctrico insuficiente | acortar conexiones y medir flancos |
| Primer byte correcto, resto no | `CS` o dummy incorrecto | revisar formato de ráfaga |

## 8. Preguntas y trabajo independiente

1. ¿Qué parte pertenece a SPI y cuál al protocolo del dispositivo?
2. ¿En qué borde cambia y en cuál se captura el dato?
3. ¿Cuál es el rendimiento útil, no solo la frecuencia de reloj?
4. ¿Qué registro ofrece una respuesta conocida para diagnóstico?

Entregar diagrama, cálculo temporal, captura anotada, tabla de bytes, código de driver y prueba de falla.

## 9. Referencias precisas

- Espressif Systems, *ESP32 Technical Reference Manual*, v5.8, cap. 20 “SPI Controller”, pp. 354–388; en especial §§20.1–20.4 sobre funciones, GP-SPI, CPOL/CPHA y temporización. [PDF oficial](https://www.espressif.com/sites/default/files/documentation/esp32_technical_reference_manual_en.pdf).
- Espressif Systems, *ESP-IDF Programming Guide*, “SPI Master Driver”, §§“Overview”, “Terminology”, “Driver Usage” y “Timing Considerations”. [Documentación oficial](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/spi_master.html).
- Espressif Systems, *ESP32 Series Datasheet*, v5.3, §4.8.2 “Serial Peripheral Interface (SPI)”, p. 36, y tabla de funciones de pin, pp. 46–50. [PDF oficial](https://www.espressif.com/documentation/esp32_datasheet_en.pdf).
- Datasheet del periférico: diagramas “SPI timing”, “serial interface” y mapa de registros, citados por versión y página.

> Consulta: 5 de agosto de 2026. No se reproducen diagramas protegidos; el estudiante debe interpretarlos desde la fuente.
