# Fundamentos de adquisición, SQLite y dashboard

Los términos enlazados, como [JSON](glosario.md#json) o [transacción](glosario.md#transaccion), abren una explicación con ejemplos. La [lectura ampliada de bases de datos](bases-de-datos.md) desarrolla los argumentos de elección y las consultas SQL.

## Del sensor a la información

Un sensor produce una lectura de una magnitud física. Por ejemplo, un DHT22 mide temperatura ambiente y humedad relativa. El ESP32 consulta esa lectura y la transmite. La Raspberry recibe el mensaje, comprueba sus datos, los guarda y permite consultarlos.

Cada parte responde una pregunta:

| Parte | Pregunta que resuelve |
|---|---|
| Sensor | ¿Qué valor tiene la magnitud física? |
| ESP32 | ¿Cómo obtengo la lectura y la envío? |
| Receptor Python | ¿El mensaje llegó y puede utilizarse? |
| [Base de datos](glosario.md#base-de-datos) | ¿Cómo conservo y consulto las lecturas? |
| [Dashboard](glosario.md#dashboard) | ¿Cómo interpreto lo que ocurre y lo que ocurrió? |

Ver un número en pantalla no demuestra que se haya guardado. Tener un archivo de datos tampoco significa que exista una interfaz para interpretarlo. La integración conecta esas funciones.

## Por qué reunir estas funciones en Raspberry

Un PC también puede recibir datos, utilizar SQLite y mostrar una página. La Raspberry permite dejar un computador dedicado junto al proyecto, con sus programas y registros, mientras el portátil se utiliza para otras tareas. Su tamaño y sus conexiones USB y de red facilitan integrarla en el montaje.

No basta con conectar la alimentación: necesita sistema operativo, almacenamiento, fuente adecuada y configuración. Para operar sin abrir una terminal se prepara un servicio. La elección se justifica cuando el proyecto necesita funcionar de manera independiente del portátil; si solo se hace una prueba ocasional, el PC puede ser suficiente.

ESP32 conserva la adquisición del sensor. Raspberry reúne recepción, histórico e interfaz. Distribuir responsabilidades facilita comprobar dónde ocurrió un fallo.

## Lectura, mensaje y registro

Son etapas relacionadas, pero diferentes:

- **Lectura:** resultado de consultar el sensor.
- **Mensaje:** representación que envía el ESP32.
- **Registro:** información que se conserva al recibir y validar el mensaje.

Un mensaje de ejemplo:

~~~json
{
  "nodo": "esp32-01",
  "variable": "temperatura",
  "valor": 25.4,
  "unidad": "C",
  "secuencia": 1,
  "estado": "OK",
  "humedad_pct": 61.2
}
~~~

Estos valores son ilustrativos. [JSON](glosario.md#json) organiza pares de nombre y valor: valor es numérico, unidad indica cómo interpretarlo y [nodo](glosario.md#nodo) identifica el origen. USB es el medio de transporte. Un salto de línea separa cada [trama](glosario.md#puerto-serial).

Raspberry añade una [marca de tiempo en UTC](glosario.md#fecha-utc) al recibir. No equivale necesariamente a la hora exacta en que el sensor midió. La secuencia cuenta intentos desde el arranque del [firmware](glosario.md#firmware); puede volver a comenzar si se reinicia el ESP32.

Por ejemplo, "valor": 25.4 comunica un número, mientras que "valor": "25.4" comunica texto. Ambos pueden formar parte de un JSON correcto, pero el segundo incumple el formato de medición que espera el receptor. Entender el formato y [validar el significado](glosario.md#validacion) son comprobaciones distintas.

## Qué es una base de datos

Es una forma organizada de conservar información y recuperarla mediante consultas. En una base relacional los datos se distribuyen en tablas.

La necesitamos porque la lectura visible ahora no cuenta por sí sola lo que pasó antes. Si el dashboard muestra 25 °C, todavía no sabemos si hace un minuto hubo 30 °C, qué nodo lo midió o si dejó de transmitir. Guardar cada lectura con su origen, unidad y hora permite investigar esas preguntas.

Una base aporta tres capacidades al proyecto:

| Necesidad | Qué se conserva o consulta | Qué permite justificar |
|---|---|---|
| Revisar un comportamiento | Varias lecturas con fecha y origen | Cómo cambió una variable en el periodo observado |
| Comprobar una regla | Valor, estado y umbral aplicado | Qué lecturas se clasificaron como ALERTA |
| Investigar un fallo | Última lectura y eventos de comunicación | Qué se recibió antes de la interrupción y cuándo se reanudó |

Estos argumentos explican por qué el proyecto incluye almacenamiento: una captura de pantalla conserva una vista; una base permite volver a consultar los registros.

Para imaginar una tabla, puede pensarse en una hoja con filas y columnas:

| id | fecha_hora | nodo | valor | unidad |
|---:|---|---|---:|---|
| 1 | 2026-11-11T15:00:00+00:00 | esp32-01 | 25.4 | C |
| 2 | 2026-11-11T15:00:03+00:00 | esp32-01 | 25.6 | C |

Ejemplo ilustrativo:

- **[Tabla](glosario.md#tabla):** conjunto de registros sobre un tema; aquí, mediciones.
- **Fila o registro:** una medición recibida.
- **Columna o campo:** una característica de esa fila, como valor o unidad.
- **[Clave primaria](glosario.md#clave-primaria):** identificador de una fila; aquí, id.
- **[Tipo de dato](glosario.md#tipos):** indica la clase de información, por ejemplo entero, real o texto.

El id de la base no es la secuencia del ESP32. La Raspberry puede seguir asignando nuevos id aunque se reinicie la secuencia del emisor.

## Qué es SQLite

[SQLite](glosario.md#sqlite) es un motor de base de datos que la aplicación utiliza directamente. En esta práctica guarda las tablas en el archivo **mediciones.sqlite3**, dentro de la carpeta del programa.

No hace falta instalar un servidor de base de datos ni crear un usuario de MySQL. Python accede mediante sqlite3, incluido habitualmente en Raspberry Pi OS.

El archivo no es un CSV ni un documento para abrir y editar como texto. Se consulta con SQLite a través de Python o de una herramienta compatible. Cambiar la extensión de un archivo no lo convierte en una base de datos.

### SQL, SQLite, sqlite3 y MySQL

| Nombre | Significado en esta práctica |
|---|---|
| [SQL](glosario.md#sql) | Lenguaje para definir, guardar y consultar datos |
| [SQLite](glosario.md#sqlite) | Motor que administra la base local |
| sqlite3 | Módulo con el que Python utiliza SQLite |
| [MySQL](glosario.md#mysql) | Otro motor, normalmente con servidor y administración propios |

SQL no es un programa que debamos abrir. Es el lenguaje de las instrucciones que enviamos a la base. SQLite y MySQL utilizan SQL con diferencias entre sus funciones y dialectos.

### Por qué lo utilizamos aquí

La elección parte de los requisitos: el receptor y la página se ejecutan en una Raspberry, existe un proceso principal de adquisición y necesitamos consultar su histórico. SQLite resuelve ese almacenamiento sin añadir la instalación y administración de otro servidor.

| Característica | Ventaja concreta en el montaje |
|---|---|
| Acceso mediante sqlite3 | Python puede guardar y consultar desde la misma aplicación |
| Archivo local | El histórico queda junto al programa y se identifica su ubicación |
| Tablas y SQL | Se pueden filtrar nodos, ordenar lecturas y calcular resúmenes |
| Transacciones | Cada escritura puede confirmarse como una operación coherente |
| Lectura durante la operación | La página puede consultar mientras el receptor sigue adquiriendo |

Un archivo local también requiere espacio, permisos y copias de respaldo. SQLite coordina una escritura a la vez; si el sistema exige muchas escrituras simultáneas o administración centralizada entre equipos, conviene evaluar otra arquitectura. [Criterios oficiales de uso de SQLite](https://www.sqlite.org/whentouse.html).

### Qué cambiaría con MySQL

MySQL normalmente añade un servicio de base de datos al que se conecta la aplicación. Ese servicio puede estar en Raspberry o en otro equipo. La página sigue necesitando una aplicación que reciba las peticiones y consulte los datos.

| Aspecto | SQLite en esta práctica | MySQL en una arquitectura con servidor |
|---|---|---|
| Acceso | Python abre la base local | Python se conecta al servicio de base de datos |
| Configuración | Archivo y permisos del sistema | Servicio, dirección, usuario, contraseña y permisos de base |
| Uso desde varios equipos | Habitualmente a través de la aplicación web | Puede centralizar conexiones de aplicaciones autorizadas |
| Escrituras concurrentes | Un escritor a la vez | Puede atender escrituras concurrentes según el motor y los bloqueos |
| Lenguaje | SQL con funciones de SQLite | SQL con funciones y diferencias propias de MySQL |

Tener varios navegadores abiertos no obliga por sí solo a cambiar a MySQL: esos navegadores consultan Flask y Flask consulta SQLite. Tampoco es necesario tener internet para utilizar MySQL en una red local. La decisión depende de dónde están los datos, quién escribe y cómo se administran los accesos.

Por ejemplo, un monitor local instalado junto a una máquina puede usar SQLite. Si varias estaciones independientes deben escribir en un repositorio compartido con permisos por aplicación, MySQL puede ser una alternativa a evaluar. [Comparación desarrollada con esquemas y ejemplos](bases-de-datos.md#sqlite-y-mysql).

## Qué ocurre al guardar una medición

1. El receptor interpreta el JSON.
2. Comprueba campos, unidad y valor.
3. Decide si corresponde NORMAL o ALERTA, cuando hay umbral.
4. Ejecuta una instrucción INSERT con los valores.
5. Confirma la transacción.
6. El registro queda disponible para una consulta.

Una [transacción](glosario.md#transaccion) agrupa cambios que deben confirmarse o revertirse. Confirmar se conoce como commit. Esto permite distinguir «intenté guardar» de «la escritura se confirmó». SQLite ayuda a mantener la consistencia de la base; no recupera mensajes que nunca llegaron ni elimina la necesidad de cuidar el almacenamiento.

En Python:

~~~python
db.execute(
    "INSERT INTO ejemplo (valor, unidad) VALUES (?, ?)",
    (25.4, "C")
)
db.commit()
~~~

Este fragmento supone que existen la conexión db y la tabla ejemplo. Los signos ? son posiciones para [parámetros](glosario.md#parametros): se entrega el valor aparte de la instrucción SQL. Son importantes al utilizar datos que llegan de un dispositivo o de una entrada del usuario.

## Cómo aprendemos las instrucciones básicas

| Instrucción | Función | Uso concreto |
|---|---|---|
| CREATE TABLE | Define una tabla | Crear el lugar donde irán las mediciones |
| INSERT INTO | Agrega una fila | Guardar una lectura validada |
| SELECT | Recupera información | Mostrar últimas lecturas o contar registros |
| WHERE | Selecciona filas que cumplen una condición | Consultar solo temperatura |
| ORDER BY | Ordena resultados | Mostrar primero las últimas filas |
| LIMIT | Limita la cantidad devuelta | Consultar cinco filas |

~~~sql
SELECT fecha_hora, valor, unidad
FROM mediciones
WHERE variable = 'temperatura'
ORDER BY id DESC
LIMIT 5;
~~~

Se lee: “mostrar fecha, valor y unidad de las mediciones de temperatura, empezando por los id mayores y devolviendo como máximo cinco filas”.

~~~sql
SELECT COUNT(*) FROM mediciones;
~~~

COUNT(*) cuenta filas; no suma temperaturas.

### Ejemplos: pasar de una pregunta a una consulta

Estas instrucciones se ejecutan desde Python o una herramienta SQLite, no directamente como comandos de la terminal Linux. El [capítulo de bases de datos](bases-de-datos.md) explica cómo probarlas y seguir cada resultado.

**¿Cuántas lecturas de temperatura en Celsius se guardaron?**

~~~sql
SELECT COUNT(*) AS cantidad
FROM mediciones
WHERE variable = 'temperatura' AND unidad = 'C';
~~~

WHERE selecciona la magnitud y la unidad. COUNT(*) cuenta las filas seleccionadas. AS da un nombre al resultado. Si solo existieran las dos filas de la tabla ilustrativa anterior, cantidad sería 2.

**¿Cuál fue el promedio y cuáles fueron los extremos?**

~~~sql
SELECT MIN(valor) AS minimo,
       ROUND(AVG(valor), 2) AS promedio,
       MAX(valor) AS maximo
FROM mediciones
WHERE variable = 'temperatura' AND unidad = 'C';
~~~

Con 25.4 y 25.6, el mínimo sería 25.4, el promedio 25.5 y el máximo 25.6. ROUND muestra el promedio con hasta dos decimales. Estas operaciones resumen los registros seleccionados; no certifican la precisión del sensor ni describen los periodos sin datos. [Agregaciones y agrupación](glosario.md#agregacion).

**¿Qué lecturas quedaron clasificadas como ALERTA?**

~~~sql
SELECT fecha_hora, nodo, valor, unidad, umbral
FROM mediciones
WHERE estado = 'ALERTA'
ORDER BY id DESC
LIMIT 5;
~~~

La consulta recupera la clasificación guardada en su momento. Si todas se recibieron con umbral null, puede no haber alertas. Eso no significa que la consulta esté fallando.

El [capítulo ampliado](bases-de-datos.md) añade ejemplos por nodo, periodos de tiempo, parámetros, NULL y relación con los elementos del dashboard.

## Un ejemplo que se puede ejecutar sin sensor

El archivo [ejemplo_sqlite.py](ejemplo_sqlite.py) crea **ejemplo.sqlite3**, inserta una fila ilustrativa y la consulta. Sirve para estudiar CREATE, INSERT, commit y SELECT antes de integrar el sensor.

Ese archivo está separado de mediciones.sqlite3 para no confundir los ejemplos con los registros reales. Cada ejecución añade una fila de ejemplo; una nueva ejecución no representa una nueva lectura física.

## La base de esta aplicación

### Tabla mediciones

Sus campos principales son:

| Campo | Qué conserva |
|---|---|
| id | Identificador asignado por SQLite |
| fecha_hora | Hora de recepción en UTC |
| nodo | Nombre enviado por el emisor |
| variable, valor y unidad | Qué se midió, cuánto y en qué unidad |
| secuencia | Contador enviado por ESP32 |
| estado | NORMAL o ALERTA según la regla configurada |
| umbral | Regla aplicada a esa lectura; puede no existir |
| humedad_pct | Lectura complementaria del ejemplo DHT22 |

El receptor admite campos adicionales para otros sensores. No son necesarios para explicar el ejemplo de temperatura.

### Tabla eventos

Guarda situaciones de operación, como una trama rechazada o un error reportado por el sensor. Un mensaje inválido no se transforma en una medición de cero.

**[NULL](glosario.md#null)** representa ausencia de un valor. No significa cero ni una cadena vacía. Si no hay umbral, la base puede conservar NULL en ese campo.

## Del CSV a SQLite

[CSV](glosario.md#csv) es un archivo de texto tabular útil para intercambio y análisis sencillo. SQLite permite mantener tablas y realizar consultas sin reescribir el archivo completo desde nuestro programa.

En la práctica anterior el programa producía un CSV. Ahora guarda en SQLite y ofrece una descarga CSV del histórico cuando se necesita. El archivo exportado es una copia para consultar o entregar; no reemplaza la base activa.

## Qué es un dashboard

Es un panel que reúne datos para que el usuario pueda interpretar el estado del sistema. Puede incluir valores, indicadores, gráficas y tablas.

En este proyecto responde:

| Elemento | Pregunta |
|---|---|
| Temperatura y humedad | ¿Cuál fue la última lectura? |
| Fecha y hora | ¿Cuándo llegó? |
| Estado | ¿Hay datos recientes o una condición que atender? |
| Gráfica | ¿Cómo cambió la variable? |
| Tabla | ¿Cuáles fueron los últimos registros? |
| Descarga | ¿Cómo reviso los datos fuera de la página? |

El dashboard no mide por sí mismo. Presenta información que el sistema ya recibió y guardó. Una gráfica visible no prueba que el sensor siga conectado.

## Cómo se construye el dashboard de la práctica

Hay tres partes:

1. **[Flask](glosario.md#flask):** herramienta Python que atiende peticiones del navegador.
2. **[HTML y JavaScript](glosario.md#html-javascript):** página que organiza los elementos y solicita actualizaciones.
3. **Consulta a SQLite:** recupera el histórico que será presentado.

Flask no es la base de datos. El navegador no abre directamente mediciones.sqlite3.

## Qué contiene cada archivo

| Archivo | Qué hace | Qué revisar primero |
|---|---|---|
| esp32_dht22.ino | Lee el sensor y envía JSON | GPIO, intervalo, nombre del nodo y formato del mensaje |
| config.json | Define la comunicación y las reglas del receptor | Puerto, velocidad, variable, unidad, rango y umbral |
| app.py | Recibe, valida, guarda y atiende la web | Recorrido de un mensaje por sus funciones |
| templates/dashboard.html | Organiza la página y actualiza sus elementos | Qué dato representa cada tarjeta y cómo se solicita el estado |
| requirements.txt | Lista las bibliotecas Python necesarias | Flask y pySerial |
| ejemplo_sqlite.py | Enseña a crear, insertar y consultar con datos ilustrativos | Archivo separado ejemplo.sqlite3 |
| consultar_datos.py | Consulta las mediciones y eventos reales | Filas coincidentes con el panel |
| generar_servicio.py | Prepara la definición para iniciar con Linux | Usuario y rutas de Raspberry |

En app.py, una función agrupa instrucciones para una tarea. Una clase reúne datos y operaciones relacionadas. No es necesario escribir la aplicación completa desde cero para reconocer este recorrido:

| Parte de app.py | Responsabilidad |
|---|---|
| load_config | Lee y comprueba config.json |
| LineFramer | Reúne los bytes recibidos hasta completar una línea |
| validate_message | Comprueba formato, campos y valores del mensaje |
| Database | Crea tablas, inserta registros y consulta el histórico |
| Runtime | Coordina la recepción, los estados y los reintentos USB |
| create_app | Define qué responde cada dirección web |

USB no garantiza que cada lectura de Python contenga un mensaje completo: puede llegar solo una parte o varias líneas juntas. Por eso LineFramer conserva lo parcial hasta encontrar el salto de línea. Después se interpreta el JSON y se valida antes de guardar.

El programa atiende la recepción y las consultas web mediante tareas de ejecución separadas dentro de la misma aplicación. Esto permite que la página siga respondiendo mientras espera datos. No significa que las lecturas se generen en el navegador.

Para la primera adaptación se modifican parámetros de configuración y los identificadores del firmware. Cambiar de sensor exige revisar también la unidad, el rango, el intervalo y los campos; no basta con cambiar un título de la página.

## Del navegador a la consulta

~~~text
Navegador pide información
          ↓
Flask recibe la petición
          ↓
Python consulta SQLite
          ↓
Flask devuelve un resumen JSON
          ↓
La página actualiza indicadores, gráfica y tabla
~~~

La dirección **/api/estado** es una [ruta de la API](glosario.md#api) que devuelve ese resumen. Una API es una forma definida de solicitar e intercambiar datos entre programas. En esta práctica puede verse como la “ventanilla” a la que la página pide información.

Una tarjeta con la última lectura, una gráfica y una tabla pueden utilizar distintas consultas sobre la misma base. El panel no necesita guardar tres copias de la medición: cambia la selección, el orden o el resumen que solicita. [Ejemplos de consultas para el dashboard](bases-de-datos.md#base-y-dashboard).

## Dónde corre cada parte

- El firmware se ejecuta en ESP32.
- app.py, Flask y SQLite funcionan en Raspberry.
- El navegador de Raspberry muestra la página.
- El Mac o PC puede controlar ese escritorio mediante Connect.

**[127.0.0.1 y el puerto web](glosario.md#localhost):** la dirección significa “este mismo computador” y 5000 identifica la aplicación web. Por eso se abre http://127.0.0.1:5000 en el navegador de Raspberry. Escribirlo en el Mac consulta al Mac.

Connect permite acceder al escritorio, pero no sustituye al receptor ni a la base de datos.

## Frecuencia de lectura y frecuencia de pantalla

El [intervalo de muestreo](glosario.md#muestreo) del ESP32 es de tres segundos. La página consulta el estado cada dos. Son tareas distintas: actualizar la página no obliga al sensor a producir otra lectura.

No se espera que cada actualización de pantalla agregue una fila. La cantidad de filas crece cuando se recibe una medición válida. El DHT22 no responde instantáneamente a cambios ambientales.

## Cómo interpretar los estados

- **OK en el mensaje:** ESP32 declara que pudo leer el sensor; Raspberry todavía debe validar.
- **NORMAL en la medición:** dato válido que no cumple la condición de alerta, o sin umbral configurado.
- **ALERTA:** dato válido que alcanza o supera el umbral elegido.
- **ERROR:** el sistema informa un fallo, como una lectura fallida del sensor.
- **SIN DATOS RECIENTES:** no se reciben lecturas válidas dentro del plazo configurado.

El dato anterior puede conservarse como histórico. Debe mostrarse como antiguo, no como una nueva lectura ni como cero. Un umbral didáctico no es una declaración de peligro físico.

## Qué cambia al cerrar o desconectar

| Situación | Efecto esperado |
|---|---|
| Cerrar la página | El receptor puede continuar si app.py sigue ejecutándose |
| Desconectar ESP32 | No llegan lecturas; se conservan registros previos |
| Reconectar USB | El receptor reintenta y vuelve a guardar datos válidos |
| Detener app.py | Se detienen recepción y servidor web |
| Reiniciar Raspberry | Se interrumpen procesos; el servicio debe volver a iniciarlos |

No se reconstruyen automáticamente las lecturas perdidas durante una desconexión. Abrir algunos puertos puede reiniciar ESP32. La secuencia podría empezar otra vez, sin borrar el histórico de la Raspberry.

## Servicio y logs

Un **[servicio](glosario.md#servicio-logs)** es una aplicación administrada por el sistema para poder iniciarla y supervisarla. systemd permite configurarlo en Linux. Guardar app.py no hace que arranque automáticamente.

Los **logs** son mensajes sobre la operación del programa: conexión, rechazo o error. El histórico de mediciones registra la variable física. Cumplen funciones distintas, aunque ambos ayudan a explicar lo ocurrido.

## Cómo justificar una conclusión

Relacionar una acción con su evidencia:

> Enviamos lecturas reales del sensor y el contador aumentó. La consulta SELECT mostró los mismos valores y horas del dashboard. Después de cerrar y abrir la página, los registros permanecieron. Esto comprueba recepción, persistencia y consulta; no demuestra que se hayan recuperado datos perdidos durante una desconexión.

Los valores concretos del informe deben venir de los archivos y pruebas del grupo.

## Referencias

- [Bases de datos: argumentos y consultas explicadas](bases-de-datos.md).
- [Glosario de términos](glosario.md).
- [SQLite: usos apropiados](https://www.sqlite.org/whentouse.html).
- [Python sqlite3](https://docs.python.org/3/library/sqlite3.html).
- [MySQL: qué es y cómo funciona](https://dev.mysql.com/doc/refman/8.4/en/what-is-mysql.html).
- [Flask: aplicación y rutas](https://flask.palletsprojects.com/en/stable/quickstart/).
- [DHT22](https://learn.adafruit.com/dht/overview).
- [Guía de la práctica](README.md).

