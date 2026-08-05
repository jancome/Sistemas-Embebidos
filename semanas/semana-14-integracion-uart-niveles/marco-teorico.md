# Marco teórico – Semana 14

## GPIO seguro e integración ESP32–Raspberry Pi

### Propósito formativo

Una interfaz tiene dimensión eléctrica y dimensión lógica. Compartir “3,3 V” no garantiza compatibilidad si se excede corriente, se conectan dos salidas o falta referencia común. Recibir bytes tampoco garantiza mensajes válidos si no hay delimitación, integridad, secuencia y timeout.

## 1. GPIO de Raspberry Pi

Los GPIO del encabezado trabajan con lógica de 3,3 V y no son tolerantes a 5 V. Un pin puede ser entrada, salida o función alternativa; su estado durante arranque puede diferir del estado de la aplicación.

Para un LED:

$$
R\geq\frac{V_{GPIO}-V_F}{I_{LED}}
$$

Motores, relés y otras cargas no se conectan directamente: requieren driver, fuente, protección y referencia apropiados. Debe distinguirse numeración física del conector y numeración BCM.

## 2. UART eléctrica y temporal

UART normalmente usa `TX`, `RX` y `GND`, con cruce TX→RX. Es asíncrona: ambos extremos acuerdan baud rate, bits, paridad y parada. Para formato 8N1, cada byte ocupa 10 bits en el enlace:

$$
R_{bytes,max}=\frac{baud}{10}
$$

El error relativo de reloj debe dejar margen para muestrear el último bit. La UART GPIO usa niveles lógicos, no RS-232; conectarla a tensiones RS-232 puede dañar el equipo.

## 3. Delimitación e integridad

Opciones de trama:

- línea de texto terminada en `\n`, fácil de inspeccionar;
- longitud + payload, adecuada para binario;
- delimitador con escape;
- encabezado, longitud, secuencia y CRC.

Un checksum simple detecta algunos errores; un CRC ofrece propiedades de detección definidas. En todo caso, el receptor valida longitud, tipo, rango, secuencia y antigüedad.

$$
edad=t_{actual}-t_{muestra}
$$

Si la edad supera el límite del requisito, el dato no debe usarse como actual aunque su valor sea plausible.

## 4. Comparación de enlaces

| Opción | Ventaja | Riesgo/condición |
|---|---|---|
| UART | directa, observable, sin infraestructura | distancia, cable y un enlace punto a punto |
| Wi-Fi/socket | flexible y mayor alcance | red, puertos y reconexión |
| HTTP | contrato solicitud/respuesta | overhead y acoplamiento al servidor |
| MQTT | desacoplamiento por broker | dependencia del broker y duplicados según QoS |

La elección debe corresponder a topología, tasa, latencia, cableado y recuperación del proyecto.

## 5. Ejemplo guiado de trama UART

Formato de texto:

```text
T,1842,31.4,OK*5A\n
```

1. `T` identifica tipo; `1842`, secuencia; `31.4`, valor; `OK`, calidad; `5A`, checksum ilustrativo.
2. A 115200 8N1 y 24 bytes, tiempo ideal ≈ $24\cdot10/115200=2.08\,ms$.
3. El receptor acumula hasta `\n` con límite de longitud y timeout.
4. Valida campos y checksum antes de publicar el objeto.
5. Si faltan tres periodos, genera estado `STALE`; no repite indefinidamente la última medida como válida.

## 6. Procedimiento de laboratorio

1. Con equipos apagados, verificar pinout y tierra común.
2. Medir niveles y confirmar que no existe 5 V en GPIO.
3. Probar GPIO con LED/resistencia o entrada protegida.
4. Configurar UART en ambos extremos y enviar patrón conocido.
5. Capturar señal o bytes y medir tasa real.
6. Forzar byte inválido, trama parcial, secuencia repetida y desconexión.
7. Implementar timeout, descarte y reconexión.

## 7. Diagnóstico

| Síntoma | Causa probable | Prueba |
|---|---|---|
| Caracteres ilegibles | baud/formato distintos | capturar tiempo de bit |
| No llegan datos | TX/RX sin cruzar o sin GND | continuidad y nivel |
| Primeras tramas corruptas | ruido/estado de arranque | retraso y limpieza de buffer |
| GPIO se calienta o falla | sobrecorriente/5 V/salidas enfrentadas | desconectar y revisar esquema |
| Mensajes se mezclan | sin delimitación/longitud | parser incremental |
| Dashboard muestra dato viejo | timeout no propagado | revisar timestamp/calidad |

## 8. Preguntas y trabajo independiente

1. ¿Qué estado tiene cada GPIO antes de iniciar la aplicación?
2. ¿Cómo se detecta una trama incompleta?
3. ¿Qué hace el sistema ante secuencia repetida o salto?
4. ¿Por qué se eligió UART, HTTP o MQTT para este proyecto?

Entregar diagrama eléctrico, contrato de trama, cálculo de tasa, captura y cuatro pruebas negativas.

## 9. Referencias precisas

- Raspberry Pi Ltd., *Raspberry Pi 4 Model B Datasheet*, Release 1.1, §4, pp. 7–8; §5.1 “GPIO Interface”, pp. 9–10; tabla 5 de funciones alternativas, p. 10. [PDF oficial](https://datasheets.raspberrypi.com/rpi4/raspberry-pi-4-datasheet.pdf).
- Raspberry Pi, “GPIO and the 40-pin header”, apartados “Outputs”, “Inputs”, “Voltage specifications” y “Safe current”. [Documentación oficial](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#gpio-and-the-40-pin-header).
- Espressif Systems, *ESP32 Hardware Design Guidelines*, §1.3.7 “UART”, p. 13, y §1.4.7, pp. 25–27. [PDF oficial](https://documentation.espressif.com/esp-hardware-design-guidelines/en/latest/esp32/esp-hardware-design-guidelines-en-master-esp32.pdf).
- Espressif Systems, *ESP32 Technical Reference Manual*, v5.8, cap. 19 “UART Controller”, §§19.1–19.3, pp. 311–318. [PDF oficial](https://www.espressif.com/sites/default/files/documentation/esp32_technical_reference_manual_en.pdf).

> Consulta: 5 de agosto de 2026. Los límites exactos del dispositivo usado prevalecen sobre reglas generales.
