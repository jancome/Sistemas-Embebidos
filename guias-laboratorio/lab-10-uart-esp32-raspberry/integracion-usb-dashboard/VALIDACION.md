# Verificación del material

## Comprobado en el entorno de preparación

- Python: sintaxis e importaciones de receptor y generador de servicio.
- Cinco pruebas automáticas: validación y persistencia, estados/frescura, tramas parciales/excesivas, API/CSV y desconexión/reconexión mediante pseudo-terminal.
- Tramas numéricas válidas, texto/booleanos/NaN/inf, campos ausentes, humedad inválida y valores fuera de rango.
- SQLite conserva registros al reabrir la base y no inserta mediciones ficticias ante error del sensor.
- Dashboard probado con Chromium en tamaño escritorio y móvil, gráfica y consultas sin errores JavaScript.
- Consulta de una fila por --id: identificador existente, ausente, inválido y base inexistente, comprobando que no se modifica la base.
- Columna ID del dashboard contrastada con la secuencia recibida y con el registro SQLite.
- Ejemplos SQL contrastados con un conjunto de datos ilustrativos y resultados esperados.
- Enlaces locales, anclas del glosario y referencias a las imágenes revisados.

Estas pruebas usaron datos identificados como prueba y bases temporales; no son mediciones del DHT22 ni evidencia de funcionamiento de una placa física.

Los diagramas de conexiones representan señales, no la ubicación física de los pines. La imagen del dashboard está identificada como captura con datos de ejemplo.

## Pendiente antes de clase

- Identificar la placa ESP32-S3 concreta, su conector USB y pinout.
- Conseguir y comprobar módulo DHT22 con pull-up y compatibilidad a 3,3 V.
- Compilar/cargar el sketch en Arduino IDE con las bibliotecas y opciones de placa correctas.
- Probar lectura real, USB, permisos y servicio en la Raspberry del docente.
- Documentar prueba física de pérdida/reconexión y reinicio.

No se compiló aquí el firmware con el toolchain de ESP32 ni se instaló el servicio en la Raspberry del docente. Son pasos de ensayo físico pendientes.

## Repetir la comprobación de software

En la carpeta con entorno activo:

~~~bash
python verificar_software.py
~~~

Usa una carpeta temporal y un puerto simulado; no reemplaza el ensayo con sensor real.

