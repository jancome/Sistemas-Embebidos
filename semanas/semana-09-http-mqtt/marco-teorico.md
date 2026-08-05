# Marco teórico – Semana 09

## HTTP, MQTT, payloads y recuperación de comunicaciones

### Propósito formativo

La red transporta bytes; el protocolo organiza intercambios; el formato representa datos; y la aplicación decide qué significan. Separar estas capas permite diagnosticar si una falla está en conectividad, sesión, mensaje, contenido o lógica.

## 1. HTTP: solicitud y respuesta

HTTP modela recursos. Una solicitud incluye método, URI, campos de cabecera y contenido opcional. La respuesta entrega estado, cabeceras y contenido. `GET` recupera una representación; `POST` procesa el contenido según el recurso. El código de estado es parte de la evidencia:

- `2xx`: solicitud procesada;
- `4xx`: problema atribuible a la solicitud o autorización;
- `5xx`: servidor no pudo completar una solicitud válida.

Una respuesta TCP recibida no equivale a éxito HTTP; y `200` no garantiza que el JSON tenga el campo esperado.

## 2. MQTT: publicación y suscripción

MQTT desacopla productores y consumidores mediante un broker y tópicos. Conceptos centrales:

- cliente, broker, tópico y filtro de suscripción;
- QoS 0: como máximo una vez;
- QoS 1: al menos una vez, por tanto puede duplicar;
- QoS 2: exactamente una vez en el flujo MQTT, con mayor intercambio;
- mensaje retenido, sesión y voluntad (`Will`) según necesidad.

QoS no reemplaza la semántica de aplicación. Con QoS 1, el receptor debe tolerar duplicados mediante identificador de muestra o secuencia.

## 3. Diseño del payload

Un mensaje útil incluye identidad, tiempo, secuencia, valor, unidad y calidad. Ejemplo conceptual:

```json
{"device":"nodo-03","seq":1842,"ts":"2026-09-30T15:40:20Z","temp_c":31.4,"quality":"ok"}
```

El tamaño útil y el overhead se separan:

$$
\eta_{payload}=\frac{B_{utiles}}{B_{totales}}
$$

Para un intervalo $T$, el caudal medio aproximado es $B_{totales}/T$, pero se debe medir también pico, latencia y memoria.

## 4. Timeout, reintento e idempotencia

Un timeout debe derivarse de la operación esperada y no ser infinito. El reintento inmediato sincronizado agrava una caída. El backoff exponencial acotado puede expresarse:

$$
t_n=\min(t_{max},t_0 2^n)+J
$$

donde $J$ es una variación aleatoria. Las operaciones repetibles deben diseñarse como idempotentes o incluir un identificador que permita detectar duplicados.

Las credenciales no se publican en el repositorio. Se inyectan por configuración local o almacenamiento seguro y se limita su alcance.

## 5. Ejemplo guiado comparativo

**Caso:** temperatura cada 10 s y alarma inmediata.

- HTTP: el ESP32 puede hacer `POST /measurements`; obtiene confirmación directa, pero inicia cada intercambio y debe conocer el servidor.
- MQTT: publica `curso/nodo03/telemetry`; múltiples consumidores pueden suscribirse y el broker desacopla extremos.
- Para QoS 1, `seq` hace detectables los duplicados.
- La alarma usa tópico separado y prioridad lógica; el control local nunca espera al broker.
- Se desconecta el servicio durante 60 s y se mide recuperación, mensajes perdidos/repetidos y memoria usada.

## 6. Procedimiento de laboratorio

1. Documentar endpoint o árbol de tópicos.
2. Definir esquema de payload, tipos, unidades y límites.
3. Enviar un mensaje válido y capturar solicitud/publicación y recepción.
4. Medir latencia extremo a extremo y tamaño.
5. Probar DNS/servidor/broker ausente, timeout, JSON inválido y respuesta 4xx/5xx.
6. Implementar reconexión con backoff y contador de fallas.
7. Verificar que adquisición y control continúan sin red.

## 7. Diagnóstico por capas

| Evidencia | Capa | Diagnóstico siguiente |
|---|---|---|
| Sin IP | enlace/red | AP, DHCP, dirección |
| IP pero nombre no resuelve | DNS | servidor configurado |
| TCP rechazada | transporte/servicio | puerto y proceso |
| HTTP 401/403 | autenticación | credencial y permisos |
| MQTT conecta pero no llega | tópico/QoS/suscripción | filtros y ACL |
| JSON recibido pero rechazado | esquema | tipo, unidad y campo |
| Datos duplicados | QoS/reintento | secuencia e idempotencia |

## 8. Preguntas y trabajo independiente

1. ¿Qué confirma realmente que una muestra fue persistida?
2. ¿Qué ocurre si el mismo mensaje llega dos veces?
3. ¿Cómo distingue el receptor dato atrasado, inválido y ausente?
4. ¿Qué estado conserva el nodo durante una caída?

Entregar diagrama, contrato de payload, mediciones, captura de una falla y justificación HTTP/MQTT.

## 9. Referencias precisas

- IETF, RFC 9110, *HTTP Semantics*, §§6–9 (mensajes y métodos) y §15 (códigos de estado). [Estándar oficial](https://www.rfc-editor.org/rfc/rfc9110).
- OASIS, *MQTT Version 5.0*, OASIS Standard, 2019, §1.2, pp. 16–18; §3.3 `PUBLISH`, pp. 53–62; §4.3 “QoS levels and protocol flows”, pp. 93–97; §4.7 “Topic Names and Topic Filters”, pp. 101–104. [PDF oficial](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.pdf).
- IETF, RFC 8259, *The JavaScript Object Notation (JSON) Data Interchange Format*, §§1–8. [Estándar oficial](https://www.rfc-editor.org/rfc/rfc8259).
- Espressif Systems, *ESP-IDF Programming Guide*, “ESP HTTP Client” y “ESP-MQTT”, secciones de configuración, eventos y ejemplos. [Documentación estable](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/protocols/).

> Consulta: 5 de agosto de 2026. En el curso puede usarse MQTT 3.1.1 o 5 según la biblioteca; la versión se documenta.
