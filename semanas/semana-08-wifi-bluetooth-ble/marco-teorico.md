# Marco teórico – Semana 08

# Wi-Fi, Bluetooth Clásico y Bluetooth Low Energy en ESP32

## 1. Propósito

Comparar tecnologías inalámbricas disponibles en ESP32 y utilizarlas con criterios de alcance, consumo, latencia, topología, seguridad y tipo de dato. El estudiante debe conocer las tres alternativas básicas del syllabus antes de seleccionar la más adecuada para su proyecto.

## 2. Resultados de aprendizaje

Al finalizar la semana, el estudiante estará en capacidad de:

- Diferenciar Wi-Fi, Bluetooth Clásico y BLE.
- Configurar el ESP32 como estación y reconocer el modo punto de acceso.
- Comprender conexión, desconexión y reconexión como estados.
- Identificar servicios y características en BLE.
- Reconocer el modelo de puerto serie en Bluetooth Clásico.
- Comparar consumo, alcance y ancho de banda.
- Diseñar una estrategia que mantenga la operación local durante fallas de red.

## 3. La comunicación inalámbrica como subsistema

La radio no debe mezclarse con la lógica principal. La arquitectura recomendada es:

```text
Adquisición local
      ↓
Validación
      ↓
Cola o buffer
      ↓
Gestor de comunicación
      ↓
Wi-Fi / Bluetooth / BLE
```

El nodo debe continuar midiendo y controlando aunque el enlace esté temporalmente caído.

## 4. Wi-Fi

Wi-Fi permite integrar el ESP32 a una red IP.

### Modo estación —STA—

El ESP32 se conecta a un punto de acceso existente.

Aplicaciones:

- acceso a servidor;
- publicación HTTP o MQTT;
- conexión con Raspberry Pi;
- sincronización de tiempo;
- configuración remota.

### Modo punto de acceso —AP—

El ESP32 crea una red a la cual se conectan otros dispositivos. Puede servir para configuración inicial o redes aisladas.

### Modo combinado

Algunas aplicaciones utilizan AP y STA de forma simultánea, aunque esto aumenta complejidad y consumo.

## 5. Estados de conexión Wi-Fi

Una máquina de estados evita llamadas bloqueantes:

```text
INICIAL
  ↓
CONFIGURANDO
  ↓
CONECTANDO
  ├── éxito → CONECTADO
  └── timeout → ESPERA_REINTENTO

CONECTADO
  └── pérdida → DESCONECTADO → ESPERA_REINTENTO
```

Cada estado debe tener un límite temporal. Reintentar sin pausa puede consumir energía y saturar registros.

## 6. Dirección IP y red

Para comunicarse con Raspberry Pi se deben comprender:

- dirección IP;
- máscara de red;
- puerta de enlace;
- DNS;
- nombre de host;
- puerto de aplicación.

Una conexión Wi-Fi exitosa no garantiza que el servidor sea alcanzable. La falla puede estar en la red, el DNS, el puerto o la aplicación.

## 7. Bluetooth Clásico

Bluetooth Clásico puede ofrecer perfiles como puerto serie. Es útil para:

- comunicación simple con teléfono o computador;
- consola de configuración;
- transmisión continua moderada;
- reemplazo de cable serial en demostraciones.

No todos los miembros de la familia ESP32 soportan las mismas funciones. Debe verificarse el SoC y el framework utilizados.

## 8. Bluetooth Low Energy —BLE—

BLE está orientado a intercambio de pequeñas cantidades de datos con bajo consumo.

Conceptos principales:

- dispositivo central;
- periférico;
- publicidad —advertising—;
- servicio;
- característica;
- descriptor;
- lectura;
- escritura;
- notificación.

### Modelo GATT

Un periférico organiza información en servicios. Cada servicio contiene características.

Ejemplo:

```text
Servicio: monitoreo ambiental
  ├── característica temperatura
  ├── característica humedad
  └── característica estado de batería
```

## 9. Comparación

| Criterio | Wi-Fi | Bluetooth Clásico | BLE |
|---|---|---|---|
| Integración IP | directa | no necesariamente | no necesariamente |
| Ancho de banda | alto | medio | bajo a medio |
| Consumo | mayor | medio | bajo |
| Alcance | depende de red | corto/medio | corto/medio |
| Modelo | red y sockets | perfiles | servicios y características |
| Uso típico | nube, servidor, Raspberry Pi | enlace serial | sensores y configuración |

La elección depende del requisito. No existe una tecnología universalmente mejor.

## 10. Consumo y tiempo de radio

La radio puede ser uno de los bloques de mayor consumo. Para reducir energía se puede:

- transmitir por lotes;
- aumentar intervalo de publicación;
- desconectar cuando no sea necesario;
- usar modos de ahorro;
- reducir tamaño de mensajes;
- evitar reintentos continuos.

El diseño debe equilibrar consumo y disponibilidad.

## 11. Coexistencia

Wi-Fi y Bluetooth comparten recursos de radio en muchas variantes de ESP32. Su uso simultáneo puede afectar latencia y rendimiento. Se debe probar la coexistencia real del proyecto y no asumir que dos ejemplos separados funcionarán juntos sin ajustes.

## 12. Seguridad básica

- no publicar credenciales en GitHub;
- evitar contraseñas triviales;
- limitar servicios expuestos;
- usar emparejamiento o autenticación cuando corresponda;
- no transmitir datos sensibles en texto plano sin evaluar el riesgo;
- separar configuración de código fuente.

## 13. Ejemplo guiado

### Requisito

Un nodo registra temperatura y debe enviar datos a Raspberry Pi cada 30 segundos, pero la alarma local no puede detenerse si se pierde la red.

### Solución propuesta

```text
Tarea de sensor → cola local → tarea Wi-Fi
                    ↓
              control de alarma
```

La tarea Wi-Fi intenta publicar. Si falla:

- conserva la última medición;
- incrementa contador de fallas;
- espera antes de reintentar;
- no bloquea la adquisición;
- informa el estado cuando la red vuelve.

### Experiencia BLE complementaria

Crear un servicio con una característica de temperatura y enviar notificación a una aplicación móvil. Así se compara el modelo GATT con el modelo IP.

## 14. Actividad práctica

Cada grupo debe realizar dos experiencias:

### Experiencia A — Wi-Fi

1. conectar como estación;
2. mostrar IP;
3. registrar eventos;
4. enviar una medición;
5. apagar el punto de acceso;
6. comprobar operación local;
7. restaurar red y reconectar.

### Experiencia B — Bluetooth o BLE

1. configurar nombre;
2. exponer un dato;
3. recibir o enviar una instrucción;
4. medir tiempo de actualización;
5. comparar con Wi-Fi.

## 15. Conexión con el ABP

Cada grupo debe justificar:

- qué tecnología usará en el proyecto;
- por qué;
- qué información transmitirá;
- con qué frecuencia;
- qué ocurre si el enlace falla;
- cómo se recupera;
- cómo protege credenciales.

## 16. Diagnóstico de fallas

### Wi-Fi

1. verificar alimentación;
2. confirmar SSID y contraseña;
3. revisar eventos de conexión;
4. comprobar IP;
5. probar `ping` desde la misma red;
6. revisar puerto y servidor;
7. validar firewall;
8. comprobar timeout y reconexión.

### BLE

1. verificar publicidad;
2. confirmar UUID;
3. revisar servicio y característica;
4. comprobar permisos de lectura/escritura;
5. activar notificaciones;
6. revisar longitud y formato del dato;
7. confirmar que el central no mantenga una conexión anterior.

## 17. Errores comunes

- Detener todo el sistema mientras conecta.
- Reiniciar el ESP32 ante cualquier desconexión.
- Guardar credenciales dentro del repositorio.
- Confundir conexión Wi-Fi con acceso al servidor.
- Seleccionar BLE sin comprender servicios y características.
- Probar solo en condiciones ideales.
- No registrar causa de desconexión.
- Enviar datos con demasiada frecuencia.
- No verificar la variante exacta de ESP32.

## 18. Trabajo independiente

- Completar comparación de tecnologías.
- Implementar máquina de estados de conexión.
- Añadir contador de fallas y tiempo desde última conexión.
- Documentar payload y frecuencia.
- Preparar el protocolo de aplicación de la Semana 09.

## 19. Referencias de apoyo

- Documentación oficial Arduino-ESP32: API Wi-Fi y bibliotecas Bluetooth/BLE.
- Documentación oficial ESP-IDF sobre BLE y coexistencia.
- `SYLLABUS.md` y `guias-laboratorio/lab-06-wifi-bluetooth/README.md`.
