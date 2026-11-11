# Glosario de la práctica

Cada término enlazado en el [marco teórico](marco-teorico.md) lleva a su explicación en esta página. Los ejemplos de valores son ilustrativos.

## Comunicación y mediciones

<a name="json"></a>
### JSON

Significa JavaScript Object Notation. Es un formato de texto que permite intercambiar datos con una estructura reconocible. Se utiliza también desde Python y C++; no exige programar en JavaScript.

En un objeto JSON hay pares de nombre y valor:

~~~json
{"nodo":"esp32-01","valor":25.4,"unidad":"C"}
~~~

- Las llaves delimitan el objeto.
- "nodo", "valor" y "unidad" son nombres de campos.
- Los dos puntos separan un nombre de su valor.
- Las comas separan los campos.
- "esp32-01" y "C" son texto; 25.4 es un número.

El número decimal se escribe con punto. JSON usa comillas dobles y no admite comentarios ni una coma después del último campo. 25.4 y "25.4" son distintos: el segundo es texto y el receptor de la práctica lo rechaza como medición.

En nuestro enlace serial se envía un objeto completo por línea. Esta forma de separar objetos se conoce como JSON delimitado por saltos de línea. El formato organiza el contenido; USB transporta los bytes. JSON no guarda por sí solo el histórico.

[Volver a lectura, mensaje y registro](marco-teorico.md#lectura-mensaje-y-registro).

<a name="nodo"></a>
### Nodo

Equipo identificado dentro del sistema. esp32-01 puede ser el nodo que mide en un punto y esp32-02 el que mide en otro. El nombre permite atribuir cada registro a su origen; no es necesariamente la dirección de red.

<a name="firmware"></a>
### Firmware

Programa que se carga en el ESP32 y se ejecuta allí. En la práctica consulta el DHT22 y envía mensajes. El archivo Python de Raspberry es otro programa, ejecutado en otro equipo.

<a name="puerto-serial"></a>
### Puerto serial, trama y baudios

El puerto serial es la interfaz que el programa abre para intercambiar datos con la placa. Linux puede identificarlo como /dev/ttyACM0 o /dev/ttyUSB0.

Una trama es una unidad de mensaje acordada. Aquí, una línea JSON constituye una trama. Recibir bytes no asegura haber recibido ya una línea completa.

Los baudios expresan una velocidad de señalización. En un enlace UART las configuraciones de ambos extremos deben coincidir; aquí se usa 115200. Cuando la placa utiliza USB CDC nativo, el transporte USB y la interpretación de esa configuración dependen de su implementación.

<a name="muestreo"></a>
### Muestreo e intervalo

Muestrear es obtener lecturas en instantes definidos. Un intervalo de tres segundos significa intentar una lectura cada tres segundos. La frecuencia correspondiente es aproximadamente una tercera parte de una lectura por segundo.

El intervalo depende del sensor y del fenómeno. Reducirlo no aumenta automáticamente la precisión y puede incumplir el tiempo de respuesta del sensor.

<a name="gpio-pullup"></a>
### GPIO y resistencia pull-up

GPIO identifica una entrada o salida configurable del microcontrolador. GPIO4 se refiere a una señal concreta del ESP32, no al cuarto pin físico de cualquier placa.

Una resistencia pull-up mantiene una línea en un nivel lógico alto cuando ningún dispositivo la lleva al nivel bajo. En un módulo DHT22 puede venir integrada. Su presencia y la compatibilidad con 3,3 V se revisan antes de conectar el sensor al ESP32.

<a name="fecha-utc"></a>
### Marca de tiempo, ISO 8601 y UTC

Una marca de tiempo asocia un hecho con una fecha y hora. En esta aplicación se registra cuándo Raspberry recibió y guardó la lectura.

2026-11-11T15:00:00+00:00 es un ejemplo en formato ISO 8601. La T separa fecha y hora; +00:00 indica UTC. Ese instante corresponde a las 10:00 en Colombia, cuya zona es UTC−05:00.

Comparar horas exige considerar la zona. El dashboard puede convertir UTC a la zona del navegador. La hora de recepción puede diferir de la hora de adquisición.

<a name="umbral"></a>
### Umbral

Valor elegido para aplicar una regla. Con umbral 26, una temperatura válida de 26,2 °C satisface valor >= umbral y se clasifica ALERTA.

En esta práctica es una regla didáctica. No certifica una condición de peligro ni debe provocarse calentando la placa. null en la configuración significa que no se aplica esta regla.

<a name="validacion"></a>
### Validación e integridad

Validar es comprobar que un dato cumple las reglas: campos necesarios, número válido, unidad esperada y rango aceptado.

La integridad se refiere a conservar datos coherentes con el modelo. Algunas reglas se comprueban en Python y otras pueden imponerse en la base. Que un mensaje sea JSON correcto no demuestra que describa una medición válida.

## Bases de datos

<a name="base-de-datos"></a>
### Base de datos y motor

La base de datos es el conjunto organizado de información. El motor es el software que permite definir su estructura, guardar cambios y consultar registros. En la práctica el motor es SQLite y la base se conserva en mediciones.sqlite3.

<a name="sql"></a>
### SQL

Significa Structured Query Language: lenguaje de consulta estructurada. Permite dar instrucciones como crear una tabla, insertar una fila o recuperar registros.

~~~sql
SELECT valor FROM mediciones;
~~~

Se lee: «obtener la columna valor de la tabla mediciones». SQLite y MySQL utilizan SQL, con diferencias de sintaxis y funciones.

<a name="sqlite"></a>
### SQLite y sqlite3

SQLite es un motor que la aplicación utiliza directamente, sin un servidor de base de datos separado. Puede conservar las tablas en un archivo local.

sqlite3 es el módulo con el que Python accede al motor. La instrucción import sqlite3 carga ese módulo; no abre todavía la base.

<a name="mysql"></a>
### MySQL y modelo cliente/servidor

MySQL es un sistema de gestión de bases de datos que normalmente funciona mediante un servidor. Una aplicación cliente se conecta a ese servicio y solicita operaciones. Cliente y servidor pueden estar en el mismo equipo o en equipos diferentes.

El servidor administra conexiones y permisos de base de datos. Requiere instalación y configuración propias. En este laboratorio se utiliza SQLite; la comparación con MySQL sirve para entender la decisión.

[Ver comparación y ejemplos](bases-de-datos.md#sqlite-y-mysql).

<a name="tabla"></a>
### Tabla, fila, columna y esquema

Una tabla reúne registros sobre un tema. Una fila contiene un caso, por ejemplo una medición. Una columna describe un atributo, como nodo o valor.

El esquema define la estructura: nombres de tablas, columnas y reglas. Cambiar un encabezado de la página no modifica el esquema de la base.

<a name="clave-primaria"></a>
### Clave primaria e identificador

Campo, o conjunto de campos, que identifica de manera única una fila. En mediciones es id.

La secuencia del ESP32 puede reiniciarse; el id pertenece al histórico de Raspberry. Una clave primaria evita identificadores duplicados, pero no garantiza por sí sola que no se inserte dos veces la misma medición física.

<a name="tipos"></a>
### INTEGER, REAL, TEXT y NOT NULL

- INTEGER representa enteros: 1, 2, 3.
- REAL representa números con decimales: 25.4.
- TEXT representa texto: esp32-01.
- NOT NULL exige que exista un valor en esa columna.

SQLite permite tipos de forma flexible en sus tablas habituales. Declarar REAL no reemplaza la validación de una medición en Python. Existen tablas STRICT para imponer controles de tipos adicionales, pero la aplicación de esta práctica no las utiliza.

<a name="null"></a>
### NULL, null y None

Expresan ausencia de un valor en contextos distintos: NULL en SQL, null en JSON y None en Python.

No equivalen al número cero ni al texto vacío. Un umbral ausente puede ser NULL; una temperatura de 0 °C puede ser una lectura real.

En SQL se consulta con IS NULL o IS NOT NULL, no con = NULL. En esta aplicación los fallos del sensor se guardan como eventos; no se insertan como mediciones de cero.

<a name="consulta"></a>
### Consulta o query, filtro, orden y límite

Una consulta pide información a la base:

~~~sql
SELECT id, valor
FROM mediciones
WHERE nodo = 'esp32-01'
ORDER BY id DESC
LIMIT 5;
~~~

SELECT elige columnas; FROM indica la tabla; WHERE filtra filas; ORDER BY ordena; DESC significa descendente; LIMIT restringe cuántas filas devuelve. Sin ORDER BY no debe asumirse un orden de resultados.

<a name="cursor"></a>
### Conexión, cursor, fetchone y fetchall

La conexión es el acceso abierto entre Python y una base concreta. db.execute envía una instrucción a través de esa conexión y devuelve un cursor, que permite recorrer su resultado.

fetchone obtiene la siguiente fila, o None si no queda ninguna. fetchall obtiene las filas restantes como una lista, que puede estar vacía. La consulta no se convierte en una nueva tabla permanente por utilizar estos métodos.

En el programa, sqlite3.Row permite identificar valores por nombre de columna. dict(fila) convierte una fila en un diccionario que resulta más fácil de leer al imprimir.

<a name="agregacion"></a>
### COUNT, AVG, MIN, MAX, GROUP BY y AS

Son herramientas para resumir datos. COUNT(*) cuenta filas; AVG calcula la media de valores; MIN y MAX obtienen los extremos. GROUP BY calcula un resultado por grupo, por ejemplo por nodo.

AS asigna un nombre al resultado de una expresión: AVG(valor) AS promedio. No renombra la columna de la tabla.

Una media solo tiene sentido si se sabe qué magnitud, unidad, nodos y periodo incluye. AVG ignora los valores NULL y promedia registros; no compensa por sí mismo los periodos sin datos.

<a name="parametros"></a>
### Parámetros de una consulta

Valores entregados por separado del texto SQL. En Python con sqlite3 se utilizan signos ? como posiciones para esos valores:

~~~python
db.execute(
    "SELECT valor FROM mediciones WHERE nodo = ?",
    ("esp32-01",)
)
~~~

La coma del segundo argumento crea una tupla de un elemento. Se evita construir la instrucción pegando texto introducido por el usuario. Los parámetros representan valores, no nombres de columnas.

<a name="transaccion"></a>
### Transacción, commit y rollback

Una transacción agrupa cambios que se confirman o se revierten. commit confirma la operación; rollback descarta los cambios pendientes de esa transacción.

Si se guarda una medición y ocurre un error antes de confirmar, no se debe anunciar que quedó conservada. Después de commit, rollback no funciona como un botón para deshacer permanentemente lo ya confirmado.

<a name="persistencia"></a>
### Persistencia y copia de respaldo

Persistencia significa conservar información después de terminar el proceso, por ejemplo en un archivo SQLite. No significa inmunidad frente a daños del almacenamiento ni recuperación de mensajes que nunca llegaron.

Una copia de respaldo es otra copia consistente para recuperar información si la original se pierde. Si SQLite está en uso, se utiliza un mecanismo de backup compatible o se detiene ordenadamente la aplicación antes de copiar. Exportar CSV conserva datos tabulares, pero no toda la estructura de la base.

<a name="concurrencia"></a>
### Concurrencia

Situación en la que varias tareas necesitan utilizar la base durante periodos que se superponen. Por ejemplo, un receptor inserta mientras el servidor consulta para la página.

SQLite permite múltiples lectores, pero coordina las escrituras para que haya un escritor a la vez. La necesidad de atender muchas escrituras concurrentes es uno de los criterios para considerar un servidor como MySQL.

<a name="indice"></a>
### Índice

Estructura que ayuda al motor a localizar registros, como un índice que orienta la búsqueda en un libro. Puede mejorar ciertas consultas, con un coste adicional de almacenamiento y mantenimiento al escribir.

No se añade automáticamente un índice por cada nueva gráfica. Se decide a partir de las consultas y su rendimiento. No hace falta crear uno adicional para comenzar esta práctica.

<a name="wal"></a>
### WAL y SHM

WAL es un modo de operación de SQLite que registra cambios en un archivo auxiliar antes de incorporarlos al archivo principal. Puede facilitar la lectura mientras otra conexión escribe. La aplicación de esta práctica utiliza ese modo.

El sufijo -wal identifica ese registro; -shm se usa para coordinar su acceso entre conexiones. Una base activa no siempre queda representada solo por el archivo principal, por eso sus auxiliares no deben borrarse ni ignorarse al realizar una copia de respaldo.

<a name="csv"></a>
### CSV

Formato de texto tabular con valores separados por un delimitador. Facilita intercambio con hojas de cálculo y otros programas.

La descarga CSV es una exportación del histórico. SQLite sigue siendo la base activa de la aplicación.

## Página y operación

<a name="terminal"></a>
### Terminal, prompt y comando

La terminal es una ventana para dar instrucciones al sistema. El prompt indica que está esperando una orden; puede verse como estudiante@raspberry:~ $.

Ese texto inicial no se copia. Si la instrucción es python app.py, solo se escribe esa parte y se pulsa Enter.

La consola Python de Thonny suele mostrar >>> y espera código Python. Los comandos cd o source de esta guía van en la terminal Linux, no en esa consola.

<a name="entorno-virtual"></a>
### Biblioteca y entorno virtual

Una biblioteca reúne funciones ya preparadas. La biblioteca DHT ayuda al firmware a leer el sensor; Flask y pySerial se utilizan desde Python para otras tareas.

El entorno virtual .venv guarda las bibliotecas Python de este proyecto. Se parece a una caja de herramientas que seleccionamos para trabajar: source .venv/bin/activate hace que esa terminal utilice la caja elegida.

Abrir otra terminal no activa automáticamente el mismo entorno. El entorno de Thonny también puede ser distinto.

<a name="compilar"></a>
### Compilar y cargar

Compilar es transformar el código del firmware en un programa que pueda ejecutar la placa. Cargar es transferir ese programa al ESP32.

El botón de verificar de Arduino IDE permite detectar errores de compilación. El de cargar añade la transferencia. Si se compila bien pero no se identifica el puerto o falla la conexión, la carga todavía puede fallar.

El archivo .ino contiene el código del firmware. Los fragmentos de explicación no se añaden como si fueran otro programa completo.

<a name="ssh"></a>
### SSH

Permite abrir una sesión de terminal en otro equipo a través de la red. En ssh estudiante@raspberry-g01.local, estudiante es el usuario de Raspberry y raspberry-g01.local es el nombre que se intenta localizar.

SSH no muestra por sí mismo el escritorio. En esta práctica sirve como posible primer acceso para activar Connect; después puede utilizarse la pantalla compartida.

<a name="dashboard"></a>
### Dashboard

Panel que reúne datos para interpretar un sistema: últimas lecturas, estados, gráfica y tabla. El significado de una tarjeta depende también de la unidad, la hora y la antigüedad de la lectura.

<a name="flask"></a>
### Flask y servidor web

Flask es una herramienta Python para crear aplicaciones web. En este montaje atiende las solicitudes del navegador, consulta la información y devuelve la página o los datos.

El servidor web atiende esas solicitudes. SQLite administra la base de datos. Aunque funcionan en Raspberry, cumplen responsabilidades distintas.

<a name="api"></a>
### API, HTTP y ruta

Una API define una forma de interacción entre programas. HTTP es el protocolo que utiliza el navegador para hacer solicitudes al servidor web. Una ruta identifica qué recurso se solicita.

Aquí / entrega la página; /api/estado devuelve un resumen JSON; /descargar.csv permite exportar registros. Estas rutas son de nuestra aplicación, no de Raspberry Pi Connect.

<a name="html-javascript"></a>
### HTML y JavaScript

HTML organiza los elementos de la página. JavaScript puede solicitar datos y actualizar lo que se ve. En nuestro dashboard se ejecuta en el navegador; Python se ejecuta en Raspberry.

<a name="localhost"></a>
### 127.0.0.1, localhost y puerto web

127.0.0.1 es una dirección que apunta al mismo equipo desde el que se utiliza. localhost es un nombre que habitualmente se resuelve a una dirección local.

En http://127.0.0.1:5000, 5000 es el puerto de la aplicación web. Es distinto del puerto serial /dev/ttyACM0. La dirección se abre en el navegador de Raspberry.

<a name="servicio-logs"></a>
### Servicio y logs

Un servicio es un programa administrado por el sistema para iniciarlo y supervisarlo. systemd permite configurar el receptor como servicio en Raspberry.

Los logs son mensajes sobre la operación: conexión, fallo y reintento. El histórico guarda mediciones. Consultar ambos ayuda a explicar una interrupción.

## Referencias

- [JSON: estructura y uso](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/JSON).
- [SQLite: tipos](https://www.sqlite.org/datatype3.html), [transacciones](https://www.sqlite.org/lang_transaction.html) y [agregaciones](https://www.sqlite.org/lang_aggfunc.html).
- [Python sqlite3](https://docs.python.org/3/library/sqlite3.html).
- [MySQL: qué es y cómo se organiza](https://dev.mysql.com/doc/refman/8.4/en/what-is-mysql.html).
- [Volver al marco teórico](marco-teorico.md).
