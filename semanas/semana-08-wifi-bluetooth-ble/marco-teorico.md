# Marco teórico – Semana 08

## Wi-Fi, Bluetooth clásico y Bluetooth Low Energy

### Propósito formativo

La tecnología inalámbrica se selecciona por requisitos de alcance, energía, caudal, topología, interoperabilidad y operación; no por la facilidad de ejecutar un ejemplo. Esta semana compara las opciones integradas en ESP32 y diseña una estrategia de estados y reconexión.

## 1. Medio compartido y presupuesto de enlace

La potencia recibida se razona con un presupuesto:

$$
P_R=P_T+G_T+G_R-L_{trayecto}-L_{adicional}
$$

El margen de enlace es:

$$
M=P_R-S_{RX}
$$

donde $S_{RX}$ es la sensibilidad requerida para una tasa/modulación. Muros, orientación, cuerpo humano, interferencia y ubicación de antena aumentan pérdidas. RSSI no es distancia directa y debe interpretarse junto con pérdidas de paquetes y latencia.

La energía por periodo de operación se estima como:

$$
E=\sum_i V I_i t_i
$$

Un enlace de alto caudal puede consumir menos energía total si transmite durante poco tiempo, pero la asociación, escaneo y reconexión también cuestan energía.

## 2. Wi-Fi

En modo estación, el ESP32 se asocia a un punto de acceso y obtiene configuración IP; en SoftAP crea su propia red. Wi-Fi facilita integración IP, HTTP y MQTT, y ofrece mayor caudal, con consumo y complejidad de red superiores.

Estados mínimos: `OFF → STARTED → CONNECTING → GOT_IP → DEGRADED → RETRY`. “Conectado al AP” no implica que DNS, broker o servidor estén disponibles.

## 3. Bluetooth clásico y BLE

Bluetooth clásico resulta útil para flujos continuos o perfiles compatibles con el dispositivo objetivo. BLE estructura datos mediante:

- GAP: publicidad, descubrimiento y conexión;
- GATT: servicios y características;
- propiedades: lectura, escritura, notificación e indicación;
- UUID: identidad semántica de servicios y características.

Una notificación no es una variable global “enviada por radio”: requiere conexión, suscripción del cliente y manejo de desconexión. La seguridad y el emparejamiento deben corresponder al riesgo del proyecto.

## 4. Coexistencia y diseño físico

Wi-Fi y Bluetooth comparten la banda de 2,4 GHz y recursos de radio. Las pruebas deben incluir operación simultánea si el proyecto la requiere. La antena del módulo necesita la zona libre y ubicación recomendadas por Espressif; una caja, plano o cable cercano puede degradar el enlace aunque el firmware sea correcto.

## 5. Ejemplo guiado de selección

Un nodo envía 40 bytes cada 10 s a una Raspberry Pi situada a 15 m, a través de una pared, y debe permitir configuración desde un teléfono.

1. El caudal de aplicación es bajo: 4 bytes/s antes de overhead.
2. La Raspberry Pi y el ESP32 comparten red local: Wi-Fi + MQTT simplifica la ruta de datos.
3. BLE puede reservarse para configuración cercana si el alcance y el teléfono lo justifican.
4. La elección se prueba con RSSI, latencia, pérdida y tiempo de reconexión en tres ubicaciones.
5. El control local no depende del enlace; los datos se marcan o almacenan temporalmente durante la desconexión.

## 6. Procedimiento práctico

1. Definir payload, periodo y condición de alarma.
2. Medir corriente/tiempo en conexión, reposo y transmisión.
3. Probar Wi-Fi: arranque, IP, pérdida del AP y recuperación.
4. Probar Bluetooth/BLE: descubrimiento, intercambio, desconexión y nueva conexión.
5. Repetir con distancia y obstáculo controlados.
6. Registrar RSSI, latencia, pérdida y energía aproximada.
7. Elegir tecnología mediante matriz, no por una sola medición.

## 7. Diagnóstico

| Síntoma | Capa probable | Verificación |
|---|---|---|
| Asociado sin enviar datos | IP/DNS/aplicación | dirección, ping y socket |
| Reinicios durante radio | alimentación | mínimo de 3,3 V |
| BLE visible pero sin datos | GATT/suscripción | propiedades y CCCD |
| Reconecta en bucle | política sin backoff | registrar estados/tiempos |
| Alcance muy variable | antena/entorno | orientación, caja y RSSI |
| Wi-Fi degrada BLE | coexistencia | probar radios separadas/juntas |

## 8. Preguntas y trabajo independiente

1. ¿Qué evento demuestra conectividad útil, no solo enlace físico?
2. ¿Cuál es el costo energético de reconectar?
3. ¿Qué información se pierde durante desconexión?
4. ¿Qué credenciales o datos requieren protección?

Entregar matriz comparativa, máquina de estados, mediciones en tres escenarios y selección justificada para el ABP.

## 9. Referencias precisas

- Espressif Systems, *ESP32 Series Datasheet*, v5.3, “Wi-Fi” y “Bluetooth”, pp. 3–5; §§4.6–4.7, pp. 32–35; tablas RF §§5.6–5.8, pp. 53–58. [PDF oficial](https://www.espressif.com/documentation/esp32_datasheet_en.pdf).
- Espressif Systems, *ESP-IDF Programming Guide*, “Wi-Fi Driver”, secciones “ESP32 Wi-Fi Feature List”, “Wi-Fi Programming Model” y “Wi-Fi Event Description”. [Documentación oficial](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/wifi.html).
- Espressif Systems, *ESP-IDF Programming Guide*, “Bluetooth API” y ejemplos GATT/GAP del target ESP32. [Documentación oficial](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/bluetooth/).
- Espressif Systems, *ESP32 Hardware Design Guidelines*, §1.3.6 “RF”, pp. 11–13, y §1.4.8, p. 27. [PDF oficial](https://documentation.espressif.com/esp-hardware-design-guidelines/en/latest/esp32/esp-hardware-design-guidelines-en-master-esp32.pdf).

> Consulta: 5 de agosto de 2026. Los valores de alcance se miden en el contexto real del proyecto.
