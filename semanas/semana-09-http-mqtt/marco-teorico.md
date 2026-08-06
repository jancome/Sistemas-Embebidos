# Marco teórico – Semana 09

# Protocolos de aplicación: HTTP y MQTT

## 1. Propósito

Comprender cómo el ESP32 intercambia información con otros sistemas usando protocolos de aplicación. El estudiante debe diferenciar transporte, protocolo, formato de datos y lógica del proyecto. Una conexión Wi-Fi activa no define por sí sola cómo se publican o reciben mediciones.

## 2. Resultados de aprendizaje

Al finalizar la semana, el estudiante estará en capacidad de:

- Diferenciar HTTP y MQTT.
- Formular solicitudes GET y POST.
- Interpretar códigos de respuesta.
- Definir tópicos y payloads MQTT.
- Seleccionar un protocolo según el requisito.
- Diseñar mensajes versionados y validables.
- Implementar timeout, reintento y recuperación.
- Separar credenciales y configuración del código público.

## 3. Capas de comunicación

La arquitectura debe distinguir:

```text
Aplicación: HTTP o MQTT
Transporte: TCP
Red: IP
Enlace: Wi-Fi
Medio: radio
```

Una falla puede ocurrir en cualquiera de estas capas. Por eso, el diagnóstico debe comprobar desde la conexión física y de red hasta la respuesta de la aplicación.

## 4. HTTP

HTTP sigue principalmente un modelo solicitud–respuesta.

### Métodos comunes

- `GET`: consultar un recurso.
- `POST`: enviar datos para crear o procesar información.
- `PUT`: actualizar o reemplazar un recurso.
- `DELETE`: solicitar eliminación.

En este curso se priorizarán GET y POST.

### Estructura conceptual

```text
Método + ruta + versión
Cabeceras
Línea vacía
Cuerpo opcional
```

Ejemplo conceptual:

```text
POST /api/mediciones
Content-Type: application/json

{"nodo":"esp32-01","temperatura":31.4}
```

## 5. Códigos de respuesta

Los códigos ayudan a interpretar el resultado:

- `2xx`: operación aceptada o exitosa.
- `4xx`: problema en la solicitud o autorización.
- `5xx`: problema del servidor.

No debe considerarse éxito únicamente porque la conexión TCP se abrió. El firmware debe comprobar el código y, cuando aplique, validar el contenido de la respuesta.

## 6. Payload JSON

JSON es legible y ampliamente utilizado.

Un mensaje útil puede incluir:

```json
{
  "schema": 1,
  "node_id": "esp32-01",
  "sequence": 145,
  "timestamp_ms": 523100,
  "temperature_c": 31.4,
  "status": "ok"
}
```

Campos recomendados:

- versión o esquema;
- identificador del nodo;
- número de secuencia;
- marca temporal;
- variable y unidad;
- estado de calidad;
- información de falla.

## 7. MQTT

MQTT utiliza un modelo publicación–suscripción mediante un broker.

```text
Publicador → broker → suscriptores
```

El publicador no necesita conocer directamente a cada receptor. Publica en un tópico.

Ejemplo:

```text
laboratorio/nodo01/telemetria
laboratorio/nodo01/estado
laboratorio/nodo01/comandos
```

## 8. Tópicos

Los tópicos deben tener una jerarquía clara. Se recomienda evitar nombres ambiguos.

Una convención posible:

```text
curso/grupo/dispositivo/categoria
```

Ejemplo:

```text
sistemas-embebidos/g03/esp32-01/temperatura
```

No se deben incluir contraseñas o datos privados en el tópico.

## 9. Calidad de servicio —QoS—

MQTT define niveles de entrega:

- QoS 0: como máximo una vez.
- QoS 1: al menos una vez.
- QoS 2: exactamente una vez en términos del protocolo.

Mayor QoS implica más intercambio y complejidad. La selección debe relacionarse con el impacto de perder o duplicar datos.

## 10. Mensajes retenidos y última voluntad

### Retained message

El broker conserva el último mensaje retenido de un tópico y lo entrega a nuevos suscriptores.

### Last Will and Testament

Permite publicar un estado cuando un cliente se desconecta de forma inesperada.

Estas funciones son útiles para dashboards y diagnóstico, pero deben diseñarse conscientemente para no mostrar datos antiguos como actuales.

## 11. HTTP frente a MQTT

| Criterio | HTTP | MQTT |
|---|---|---|
| Modelo | solicitud–respuesta | publicación–suscripción |
| Intermediario | servidor web/API | broker |
| Acoplamiento | cliente conoce endpoint | cliente conoce broker y tópico |
| Sobrecarga | mayor | generalmente menor |
| Uso típico | consulta y envío puntual | telemetría continua y eventos |
| Recepción de comandos | polling o servidor propio | suscripción directa |

## 12. Timeout y reintento

Un sistema robusto debe evitar esperas indefinidas.

```text
intento
  ├── éxito → confirmar y continuar
  └── falla → registrar → esperar → reintentar
```

La espera puede incrementarse gradualmente —backoff— para evitar saturar la red.

Los datos pueden almacenarse temporalmente en una cola si el enlace no está disponible.

## 13. Idempotencia y duplicados

Con reintentos, un mismo mensaje puede llegar más de una vez. Incluir un número de secuencia o identificador permite reconocer duplicados.

Ejemplo:

```text
node_id + sequence = identificador lógico del registro
```

## 14. Seguridad básica

- no almacenar tokens en archivos públicos;
- usar canales cifrados cuando el entorno lo requiera;
- autenticar clientes;
- limitar tópicos y permisos;
- validar tamaños y tipos de datos;
- no ejecutar comandos recibidos sin comprobación;
- registrar intentos fallidos.

## 15. Ejemplo guiado

### Caso HTTP

El ESP32 mide humedad cada minuto y envía un POST a una API en Raspberry Pi.

Pasos:

1. verificar Wi-Fi;
2. construir JSON;
3. abrir conexión;
4. enviar solicitud;
5. leer código;
6. confirmar recepción;
7. registrar tiempo y resultado;
8. guardar la medición si falla.

### Caso MQTT

El ESP32 publica telemetría en:

```text
curso/g02/nodo01/telemetria
```

La Raspberry Pi se suscribe, valida el esquema y almacena los datos. El ESP32 también se suscribe a:

```text
curso/g02/nodo01/comandos
```

Los comandos deben contener versión, acción permitida y parámetros válidos.

## 16. Actividad práctica

Cada grupo debe elegir HTTP o MQTT para una implementación principal y demostrar:

1. conexión;
2. payload documentado;
3. envío válido;
4. respuesta o confirmación;
5. medición del tiempo de comunicación;
6. pérdida del servidor o broker;
7. timeout;
8. reintento controlado;
9. recuperación;
10. registro de fallas.

Además, debe explicar cómo se implementaría el mismo caso con el otro protocolo.

## 17. Conexión con el ABP

El protocolo debe permitir la integración posterior con Raspberry Pi. Se debe definir:

- endpoint o tópico;
- formato de mensaje;
- frecuencia;
- unidad;
- calidad del dato;
- autenticación;
- comportamiento sin red;
- estrategia de reenvío;
- detección de duplicados.

## 18. Diagnóstico de fallas

### HTTP

1. comprobar IP y puerto;
2. probar endpoint desde otro cliente;
3. revisar método y ruta;
4. confirmar cabeceras;
5. validar JSON;
6. leer código de respuesta;
7. revisar timeout;
8. comprobar servidor y firewall.

### MQTT

1. verificar broker;
2. comprobar puerto;
3. revisar credenciales;
4. confirmar client ID;
5. revisar tópico exacto;
6. comprobar suscripción;
7. validar QoS;
8. observar mensajes con un cliente de prueba;
9. revisar reconexión.

## 19. Errores comunes

- Confundir Wi-Fi con HTTP.
- Publicar sin verificar respuesta.
- Enviar valores sin unidad o identificador.
- No versionar el esquema.
- Reintentar en un ciclo rápido.
- Usar tópicos inconsistentes.
- Ignorar mensajes duplicados.
- Guardar credenciales en GitHub.
- Suponer que el broker siempre está disponible.
- Aceptar comandos sin validación.

## 20. Trabajo independiente

- Documentar el contrato de mensajes.
- Implementar timeout y reintento.
- Añadir número de secuencia.
- Probar un dato inválido.
- Registrar tamaño del payload y tiempo de comunicación.
- Preparar la arquitectura concurrente de la Semana 11.

## 21. Referencias de apoyo

- Documentación oficial de MQTT.
- Documentación oficial Arduino-ESP32 para clientes de red.
- Documentación de la API o broker seleccionado.
- `SYLLABUS.md` y `guias-laboratorio/lab-07-http-mqtt/README.md`.
