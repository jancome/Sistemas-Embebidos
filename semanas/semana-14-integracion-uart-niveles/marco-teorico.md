# Marco teórico – Semana 14

# Integración ESP32–Raspberry Pi 4, UART, niveles lógicos y validación de tramas

## 1. Propósito

Integrar físicamente y lógicamente el ESP32 con la Raspberry Pi 4. La comunicación debe diseñarse como una interfaz completa: niveles eléctricos, conexión, velocidad, formato, delimitación, validación, timeout y recuperación.

## 2. Resultados de aprendizaje

Al finalizar la semana, el estudiante estará en capacidad de:

- Verificar compatibilidad de niveles lógicos.
- Conectar correctamente TX, RX y GND.
- Configurar UART en ESP32 y Raspberry Pi.
- Diseñar una trama delimitada y versionada.
- Detectar mensajes incompletos, inválidos o duplicados.
- Implementar timeout y reconexión.
- Comparar UART con Wi-Fi, HTTP o MQTT como alternativas de enlace.

## 3. UART

UART es una comunicación serie asíncrona. Los equipos deben coincidir en:

- velocidad en baudios;
- número de bits de datos;
- paridad;
- bits de parada;
- nivel lógico;
- referencia de tierra.

Una configuración habitual es:

```text
115200 baudios, 8 bits, sin paridad, 1 bit de parada
```

Debe documentarse y no asumirse.

## 4. Conexión cruzada

```text
ESP32 TX  ─────────→ Raspberry Pi RX
ESP32 RX  ←───────── Raspberry Pi TX
ESP32 GND ────────── Raspberry Pi GND
```

TX de un equipo se conecta a RX del otro. La tierra común es necesaria para establecer una referencia cuando no hay aislamiento.

## 5. Niveles lógicos

Tanto ESP32 como Raspberry Pi trabajan con lógica de 3,3 V, pero se debe verificar la placa y el adaptador usados.

No conectar directamente:

- UART de 5 V;
- adaptadores USB–serial configurados a 5 V;
- señales RS-232 reales;
- salidas industriales de 12 V o 24 V.

RS-232 no es equivalente a UART TTL. Requiere transceptor apropiado.

## 6. Velocidad y error

Una velocidad mayor reduce tiempo de transmisión, pero puede aumentar sensibilidad a cableado, ruido y diferencias de reloj.

El tiempo aproximado para enviar un byte con 8N1 es:

```text
10 bits / baud rate
```

A 115200 baudios:

```text
≈ 86,8 μs por byte
```

Una trama de 50 bytes tarda aproximadamente 4,34 ms, sin incluir procesamiento.

## 7. Delimitación de tramas

Un receptor debe saber dónde empieza y termina un mensaje.

Opciones:

- salto de línea;
- carácter inicial y final;
- longitud explícita;
- codificación especial;
- protocolo binario.

Ejemplo de texto:

```text
V1,ESP32-01,152,31.4,OK*5A\n
```

Campos:

- versión;
- identificador;
- secuencia;
- valor;
- estado;
- checksum;
- terminador.

## 8. Texto frente a binario

### Texto

Ventajas:

- legible;
- fácil de depurar;
- útil en laboratorio.

Desventajas:

- mayor tamaño;
- conversión de tipos;
- riesgo de delimitadores dentro del contenido.

### Binario

Ventajas:

- compacto;
- eficiente;
- estructura fija.

Desventajas:

- menos legible;
- requiere manejo cuidadoso de orden de bytes y empaquetado.

Para la primera integración puede preferirse texto estructurado y luego justificar una alternativa binaria.

## 9. Validación

El receptor no debe aceptar una trama únicamente porque termina en salto de línea.

Se verifica:

- número de campos;
- versión;
- identificador;
- tipo de datos;
- rango físico;
- secuencia;
- checksum o CRC;
- longitud máxima;
- estado.

## 10. Checksum

Un checksum simple puede detectar algunas alteraciones. Un CRC ofrece mayor capacidad de detección.

La elección depende de:

- longitud;
- ruido;
- impacto del error;
- recursos;
- necesidad del proyecto.

La validación física del rango complementa la integridad del mensaje.

## 11. Secuencia y duplicados

Un contador de secuencia permite detectar:

- mensajes perdidos;
- duplicados;
- reinicio del nodo;
- desorden, en protocolos que lo permitan.

Ejemplo:

```text
150, 151, 153 → falta 152
```

El receptor debe definir qué hace ante la pérdida.

## 12. Timeout

Si no se recibe una trama completa dentro de un tiempo, el buffer debe descartarse o reiniciarse.

También debe existir un timeout de enlace:

```text
si no hay mensaje válido durante 10 s → estado DESCONECTADO
```

El sistema puede conservar el último valor, pero debe marcarlo como antiguo.

## 13. Recepción no bloqueante

La aplicación Python no debe quedar detenida indefinidamente esperando un byte. Se utilizan:

- timeout del puerto;
- lectura por bloques;
- bucle con control de tiempo;
- hilo o proceso, si se justifica;
- integración con eventos.

## 14. Alternativas de integración

El syllabus permite UART, Wi-Fi, HTTP o MQTT.

| Enlace | Ventaja | Riesgo/limitación |
|---|---|---|
| UART | simple, directo, sin red | cable y distancia limitada |
| Wi-Fi + HTTP | fácil integración con API | solicitud–respuesta y red |
| Wi-Fi + MQTT | desacoplamiento y telemetría | requiere broker |
| USB–serial | conveniente | depende de adaptador y puerto |

Cada grupo debe justificar el enlace principal y conservar una estrategia de diagnóstico.

## 15. Ejemplo guiado

### Trama

```text
V1,NODO03,0042,28.7,1,8F\n
```

Interpretación:

- `V1`: versión;
- `NODO03`: origen;
- `0042`: secuencia;
- `28.7`: medición;
- `1`: estado válido;
- `8F`: checksum.

La Raspberry Pi:

1. recibe hasta `\n`;
2. limita longitud;
3. separa campos;
4. valida versión;
5. convierte secuencia y valor;
6. verifica rango;
7. calcula checksum;
8. acepta o rechaza;
9. registra el resultado.

## 16. Actividad práctica

Cada grupo debe:

1. dibujar conexión;
2. comprobar niveles;
3. configurar UART;
4. transmitir tramas periódicas;
5. crear receptor Python;
6. validar campos;
7. provocar una trama incompleta;
8. modificar checksum;
9. desconectar el cable;
10. reconectar y recuperar;
11. registrar pérdida de secuencia.

## 17. Conexión con el ABP

La interfaz es el contrato entre el nodo y el computador de borde. Debe documentarse en una tabla:

| Campo | Tipo | Unidad | Rango | Obligatorio | Acción si falla |
|---|---|---|---|---|---|

Esta especificación debe mantenerse sincronizada con el código de ambos lados.

## 18. Diagnóstico de fallas

Si no se reciben datos:

1. verificar GND;
2. comprobar cruce TX/RX;
3. medir nivel lógico;
4. confirmar puerto;
5. verificar baud rate;
6. probar con terminal serial;
7. observar TX con analizador lógico;
8. comprobar permisos del puerto;
9. cerrar otros programas que usen el dispositivo.

Si los datos aparecen corruptos:

- revisar velocidad;
- comprobar ruido y cables;
- verificar formato;
- revisar codificación;
- comprobar orden de bytes;
- reducir frecuencia;
- añadir checksum;
- observar reinicios.

## 19. Errores comunes

- Conectar TX con TX.
- Olvidar tierra común.
- Usar adaptador a 5 V.
- Confundir UART con RS-232.
- Leer sin delimitación.
- No limitar tamaño de buffer.
- Aceptar datos fuera de rango.
- No detectar timeout.
- Usar el último valor sin marcar su antigüedad.
- Cambiar el formato en ESP32 sin actualizar Python.

## 20. Trabajo independiente

- Documentar la especificación de trama.
- Añadir checksum o CRC.
- Registrar secuencia y timestamp.
- Preparar datos para SQLite.
- Comparar UART con el protocolo inalámbrico del Corte 2.

## 21. Referencias de apoyo

- Documentación oficial de ESP32 sobre UART.
- Raspberry Pi Documentation sobre interfaces y acceso serial.
- PySerial Documentation.
- `guias-laboratorio/lab-10-uart-esp32-raspberry/README.md`.
