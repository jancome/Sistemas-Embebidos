# Práctica integradora: sensor → ESP32 → Raspberry → SQLite → dashboard

Para sesiones de **3 horas** y cierre del curso antes del **27 de noviembre de 2026**. Complementa los laboratorios 10 y 11.

**Sensor de referencia recomendado:** DHT22 en módulo de tres pines, con resistencia pull-up integrada y operación confirmada a 3,3 V. Debe conseguirse y probarse antes de la clase. Las evidencias serán mediciones reales; no se completan lecturas faltantes con valores simulados.

## Resultado de la práctica

~~~text
Módulo DHT22 → ESP32-S3 → USB de datos → Raspberry Pi
                                      ├─ Python: recibir y validar
                                      ├─ SQLite: conservar registros
                                      └─ Flask: dashboard en el navegador
~~~

**SQL es el lenguaje; SQLite y MySQL son gestores distintos.** SQLite guarda la base en un archivo y no necesita administrar un servidor de base de datos separado. sqlite3 viene en la instalación habitual de Python de Raspberry Pi OS. Flask sirve la página y pySerial recibe por USB.

La página se abre en el navegador de la Raspberry, incluso si se ve su escritorio por Connect. No hay que configurar Wi-Fi en ESP32 ni abrir puertos del router.

## Organización hasta el cierre

| Sesión | Trabajo y evidencia |
|---|---|
| 11 de noviembre | Sensor, mensaje USB, recepción, SQLite y dashboard |
| 18 de noviembre | Adaptación al proyecto, tramas inválidas, desconexión/reconexión, servicio y logs |
| 25 de noviembre | Demostración, consulta de históricos y sustentación |
| Hasta el 27 de noviembre | Margen de cierre que indique el docente; no supone clases adicionales |

El repositorio sitúa la muestra final el 25. Esta propuesta no cambia esa fecha ni los pesos de evaluación.

## Preparación antes de clase

- Raspberry actualizada, Python 3 y acceso al escritorio.
- ESP32-S3 y cable USB **de datos**; identificar qué conector utiliza la placa.
- Módulo DHT22 de tres pines con pull-up integrado, probado con alimentación y señal de 3,3 V.
- Cables; montaje con alimentación desconectada.
- Arduino IDE con soporte de placa y bibliotecas **DHT sensor library by Adafruit** y **Adafruit Unified Sensor** instaladas.
- Carpeta de esta práctica descargada en Raspberry.

N16R8 identifica memoria del módulo, no el pinout completo. Verificar la placa concreta. Esta práctica no necesita utilizar PSRAM.

## Archivos

~~~text
integracion-usb-dashboard/
  app.py
  config.json
  requirements.txt
  generar_servicio.py
  templates/dashboard.html
  esp32_dht22/esp32_dht22.ino
  mediciones.sqlite3           # Lo crea la aplicación
~~~

Descargar el repositorio mediante **Code → Download ZIP**, descomprimir y abrir esta carpeta, o utilizar su copia local. Mantener templates/dashboard.html junto a app.py.

## Clase de tres horas

| Bloque | Actividad |
|---|---|
| 20 min | Explicar adquisición, mensaje, validación, persistencia y consulta |
| 25 min | Sensor y lectura del ESP32 |
| 20 min | Observar una trama JSON por línea |
| 30 min | Receptor y comprobación de SQLite |
| 30 min | Dashboard e histórico |
| 35 min | Pruebas de comunicación y recuperación |
| 20 min | Evidencia y adaptación al proyecto |

La base del dashboard se entrega preparada. No se dedica la clase a programar HTML desde cero. Cada integrante debe explicar cómo un dato llega desde el sensor hasta la consulta.

## 1. Montar el DHT22

Con alimentación desconectada, seguir **las etiquetas del módulo**, no una posición supuesta:

| Módulo DHT22 | ESP32-S3 |
|---|---|
| VCC / + | 3V3 |
| GND / − | GND |
| DATA / S | GPIO4, si está expuesto y libre en el pinout de la placa |

El sensor se conecta al ESP32, no a los GPIO de Raspberry. El sensor suelto de cuatro pines puede necesitar pull-up externo; el módulo elegido debe incluirlo y funcionar a 3,3 V. Si cambia GPIO, modificar PIN_DHT.

## 2. Programar y observar el ESP32

Abrir [esp32_dht22.ino](esp32_dht22/esp32_dht22.ino), seleccionar placa/puerto y cargar. Lee cada **3 segundos**. No consultar DHT22 más rápido que su intervalo admitido.

Con USB nativo puede ser necesario **USB CDC On Boot → Enabled** para que Serial salga por ese conector. Con puente USB-UART, Serial y la selección CDC deben corresponder al puente. Usar el mismo conector funcional al pasar a Raspberry; consultar el manual de la placa.

Monitor serial a **115200 baudios**. Ejemplo ilustrativo:

~~~json
{"nodo":"esp32-01","variable":"temperatura","valor":25.4,"unidad":"C","secuencia":1,"estado":"OK","humedad_pct":61.2}
~~~

Cerrar el monitor antes de abrir el receptor: un puerto no debe ser usado por dos aplicaciones.

**Explicación:** JSON organiza campos, USB transporta. valor es numérico; unidad le da significado; secuencia ayuda a observar continuidad/reinicios. Raspberry agrega la hora de recepción. Si el sensor falla, ESP32 envía ERROR con valor null, no una temperatura ficticia de cero.

## 3. Preparar Python y el puerto

Conectar ESP32 por USB a Raspberry. No conectarlo simultáneamente a dos computadores. En una terminal **de la Raspberry**, entrar a la carpeta que contiene app.py y ejecutar cada línea:

~~~bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m serial.tools.list_ports -v
~~~

Si falta venv, instalar python3-venv antes de clase. Si hay Permission denied, consultar:

~~~bash
groups
~~~

Si falta dialout, agregar al usuario propio y cerrar sesión o reiniciar cuando no haya actualización activa:

~~~bash
sudo usermod -aG dialout "$USER"
~~~

No ejecutar toda la aplicación con sudo ni cambiar permisos globales de /dev.

## 4. Revisar config.json

~~~json
{
  "puerto": "auto",
  "baudrate": 115200,
  "variable": "temperatura",
  "unidad": "C",
  "minimo": -40,
  "maximo": 80,
  "umbral": null,
  "sin_datos_s": 10
}
~~~

- auto acepta un único puerto USB detectado. Con varios dispositivos o sin metadatos USB, escribir la ruta identificada con list_ports, por ejemplo /dev/ttyACM0 o /dev/ttyUSB0.
- Puede usarse /dev/serial/by-id/… si existe esa identificación persistente.
- min/max corresponden a la variable/sensor. No son un umbral de peligro.
- umbral null desactiva la alerta. Para ensayarla, elegir un valor próximo a una lectura observada; no forzar calor. La regla es valor >= umbral.
- sin_datos_s debe superar al intervalo de envío: 10 s para envíos cada 3 s.
- Detener/iniciar la aplicación después de editar configuración.

## 5. Ejecutar y ver el dashboard

Desde esa carpeta y con .venv activo:

~~~bash
python app.py
~~~

En el navegador **dentro del escritorio de Raspberry**:

~~~text
http://127.0.0.1:5000
~~~

Esa dirección escrita en el navegador del Mac consultaría al Mac. El servidor escucha localmente; no se necesita publicarlo en Internet.

Muestra temperatura, humedad, hora, estado, gráfica, últimos registros, contador y descarga CSV. La página consulta cada dos segundos; la adquisición sigue el intervalo del ESP32.

**Comprobar:** la secuencia y el número de filas aumentan. Observar cambios ambientales suaves y esperar la respuesta del sensor. Si falta el sensor pueden preparar software, pero no presentar simulaciones como adquisición física.

## 6. Consultar SQLite

app.py crea mediciones.sqlite3 junto al programa. Abrir otra terminal en la misma carpeta:

~~~bash
python3
~~~

En ese intérprete, una instrucción a la vez:

~~~python
import sqlite3
db = sqlite3.connect("mediciones.sqlite3")
filas = db.execute("SELECT fecha_hora, valor, unidad, estado FROM mediciones ORDER BY id DESC LIMIT 5").fetchall()
print(filas)
cantidad = db.execute("SELECT COUNT(*) FROM mediciones").fetchone()[0]
print("Mediciones guardadas:", cantidad)
db.close()
exit()
~~~

SELECT consulta, ORDER BY id DESC empieza por las últimas filas y LIMIT 5 acota el resultado. Comparar una fila con el dashboard. La hora guardada es recepción en UTC; el navegador muestra la zona local.

Una trama inválida o un fallo del sensor no insertan una medición ficticia. Los detalles quedan en la tabla eventos y los logs.

## 7. Pruebas

| Prueba | Acción | Evidencia |
|---|---|---|
| Adquisición | Sensor conectado y mensajes válidos | Lecturas reales y secuencia |
| Persistencia | Consultar SQLite y recargar página | Filas anteriores conservadas |
| Trama inválida | Activar PROBAR_TRAMA_INVALIDA en el sketch y volver a cargar | Segunda trama rechazada; contador/evento; luego recepción válida |
| Pérdida USB | Desconectar USB ESP32–Raspberry | Último dato marcado como histórico; cambia estado; sin ceros inventados |
| Reconexión | Volver a conectar USB de datos | Reintenta y guarda nuevas lecturas |
| Arranque | Configurar servicio y reiniciar ordenadamente | Receptor iniciado y dashboard disponible |

Para cargar firmware detener receptor y cerrar monitores. Identificar la prueba inducida y volver PROBAR_TRAMA_INVALIDA a false al terminar.

Los datos nunca recibidos no se recuperan automáticamente. La versión no implementa buffer/reenvío, deduplicación, autenticación de nodos ni control de actuadores. Abrir el puerto puede reiniciar ESP32 y su secuencia; el histórico de Raspberry permanece.

## 8. Servicio y logs — segunda sesión

Comprobar primero el funcionamiento manual. Detener app.py con Ctrl+C y ejecutar desde la carpeta:

~~~bash
python generar_servicio.py
sudo cp monitor-esp32.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now monitor-esp32
systemctl status monitor-esp32 --no-pager
~~~

El generador usa el usuario y rutas reales, sin asumir jancome. Ejecutarlo sin sudo; solo la instalación requiere sudo.

~~~bash
journalctl -u monitor-esp32 -n 30 --no-pager
sudo systemctl restart monitor-esp32
~~~

No ejecutar simultáneamente el servicio y otra copia manual. Reiniciar el servicio tras editar configuración. Reiniciar Raspberry ordenadamente cuando no haya actualización activa.

El servicio arranca el receptor, pero no recupera lecturas perdidas durante un apagado. Flask se utiliza para una práctica local, no como despliegue industrial o servicio público.

## Entrega mínima de la muestra

Sensor real, contrato de mensaje, conexiones, código ESP32/Python, SQLite con datos, consulta explicada, dashboard, trama inválida rechazada, pérdida/reconexión, servicio, logs, informe y demostración individual.

Se mantienen los otros requisitos del proyecto final —placa base, modularidad/FreeRTOS y actuador/indicador— según el alcance acordado; esta práctica no los reemplaza.

## Adaptar al proyecto

Cambiar variable, unidad y valor en ESP32, y los mismos campos/rangos en config.json. Conservar mensaje, validación y persistencia. Humedad es un campo complementario opcional.

El YF-S201 requiere adaptar su señal antes del ESP32-S3; no conectarlo directamente como sustituto del DHT22. Su factor de caudal es nominal y necesita verificación/calibración.

## Diagnóstico

| Síntoma | Revisar |
|---|---|
| No hay puerto | Cable de datos, conector, CDC/puente USB-UART y list_ports |
| Permission denied | Grupo dialout y sesión actualizada |
| Sin lecturas válidas | DHT, 3,3 V, pull-up, pin y JSON |
| Tramas rechazadas | Campos, variable/unidad, números y rango |
| Página no abre | app.py activo, navegador de Raspberry, puerto 5000 libre |
| Página sin cambios | Conexión, edad del dato y eventos |
| No guarda | Logs, permisos y espacio disponible |

## Fuentes

- [Lab 10](../README.md), [Lab 11](../../lab-11-sqlite-dashboard-servicio/README.md).
- [Cronograma](../../../CRONOGRAMA_2026_2.md), [proyecto final](../../../PROYECTO_FINAL.md).
- [Python sqlite3](https://docs.python.org/3/library/sqlite3.html).
- [pySerial](https://pyserial.readthedocs.io/en/latest/shortintro.html).
- [Flask](https://flask.palletsprojects.com/en/stable/installation/).
- [DHT22](https://learn.adafruit.com/dht/overview), [conexión y pull-up](https://learn.adafruit.com/dht/connecting-to-a-dhtxx-sensor).
- [ESP32 GPIO](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/gpio.html), [USB CDC](https://docs.espressif.com/projects/arduino-esp32/en/latest/tutorials/cdc_dfu_flash.html).
