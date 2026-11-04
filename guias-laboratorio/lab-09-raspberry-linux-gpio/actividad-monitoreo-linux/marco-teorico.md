# Marco teórico — Raspberry Pi como computador de borde e integrador del proyecto

Complemento del [laboratorio de monitoreo Linux](README.md).  
**Alcance:** fundamentos de SBC, Linux, adquisición, validación y persistencia; demostración de temperatura CPU y reto de RAM. El curso toma Raspberry Pi 4 como referencia y la demostración utiliza Pi 5. Las capacidades concretas dependen del modelo, sistema y accesorios.

## 1. Pregunta orientadora

**¿Por qué podría convenir integrar el proyecto en una Raspberry Pi en vez de mantenerlo conectado a un PC?**

Porque permite dedicar un computador compacto al funcionamiento del proyecto, instalarlo cerca de los sensores y mantener recepción, procesamiento y almacenamiento sin depender del computador personal del estudiante. El PC puede quedar como herramienta de desarrollo y como cliente para consultar resultados.

Esto es una **decisión de arquitectura**, no una ventaja absoluta. Un PC también puede recibir datos del ESP32, guardar CSV/SQLite, ejecutar servicios y mostrar dashboards. La Raspberry no vuelve posibles esas funciones por primera vez: cambia cómo se despliega el sistema. Conviene comparar necesidades, recursos y costo total antes de elegir.

## 2. Conceptos que no debemos confundir

### Sistema embebido
Sistema de cómputo incorporado a un dispositivo o proceso para cumplir funciones definidas: medir, controlar, comunicar o supervisar. Lo que lo caracteriza es su función e integración; no necesariamente un tamaño específico ni la ausencia de sistema operativo.

### Microcontrolador
Integra procesamiento, memoria y periféricos orientados al control. En este curso el ESP32 se ocupa de adquisición y control local mediante firmware o un RTOS. Contar con un RTOS no garantiza por sí solo cumplir plazos: hay que diseñar y comprobar tiempos, prioridades y fallas.

### SBC
Un *single-board computer* reúne las funciones principales de un computador en una placa. Raspberry Pi 4/5 ejecuta un sistema operativo completo, aplicaciones y servicios. Raspberry Pi Pico es una familia de microcontroladores distinta: no se deben trasladar sus características a Pi 4/5.

### Computador de borde
Procesa información cerca de su origen. La ubicación y el papel en la arquitectura importan más que la marca: una Raspberry, un PC o un equipo industrial pueden desempeñar esa función.

## 3. Componentes y su significado para el proyecto

| Componente | Función | Relación con el laboratorio |
|---|---|---|
| CPU | Ejecuta instrucciones | Lee, valida, clasifica y escribe registros |
| RAM | Espacio temporal de programas/datos | Es la magnitud que estudia el reto de estudiantes |
| Almacenamiento | Conserva sistema, código e históricos | Guarda CSV; RAM no sustituye persistencia |
| USB | Conexión de periféricos | Próxima comunicación serial con una placa ESP32 |
| Red | Comunicación entre equipos | Administración y consulta remotas |
| GPIO e interfaces | Conexión electrónica | Requieren niveles y bibliotecas correctos; no se usan en esta práctica |
| Alimentación/refrigeración | Sostienen operación estable | Influyen en estabilidad y rendimiento |

Como ejemplo documentado, **Pi 5** utiliza un procesador Arm Cortex-A76 de cuatro núcleos a 2,4 GHz, incorpora USB 2/3, Ethernet Gigabit, Wi-Fi y Bluetooth, conector de 40 pines y almacenamiento microSD. Dispone de PCIe para periféricos mediante adaptadores adecuados. La capacidad RAM depende de la variante: la placa del docente tiene 8 GB, pero no toda Pi 5 tiene esa capacidad. Consultar [especificaciones oficiales](https://www.raspberrypi.com/products/raspberry-pi-5/).

**8 GB de RAM no son 8 GB de espacio para guardar archivos.** Tampoco los 27 W anunciados de una fuente equivalen a consumo continuo del equipo: consumo depende de carga, periféricos y configuración.

## 4. Ventajas prácticas y sus condiciones

- **Integración física:** puede montarse en una caja junto al sistema. Hay que prever ventilación, fijación, conectores y mantenimiento.
- **Equipo dedicado:** evita que cerrar el portátil o llevárselo detenga la aplicación. Requiere alimentación estable y configuración de arranque.
- **Software Linux:** facilita organizar aplicaciones, servicios, archivos y registros. Requiere administración y actualizaciones.
- **Conectividad:** permite enlazar el nodo, servir información y administrar remotamente. No sustituye diseñar el protocolo.
- **Procesamiento local:** puede filtrar y guardar sin enviar todo a Internet. Esto solo se cumple si la aplicación y sus dependencias funcionan localmente.
- **Posible menor espacio/consumo:** frente a ciertos PC de escritorio, puede ser ventajosa. No es una comparación universal: un mini-PC eficiente también puede ser adecuado.
- **Aprendizaje transferible:** separa firmware, aplicación, persistencia y operación, conocimientos aplicables a otros equipos.

## 5. Raspberry, PC y ESP32: elegir por responsabilidades

| Criterio | Raspberry Pi como integrador | PC como integrador |
|---|---|---|
| Demostración inicial | Requiere preparar equipo/almacenamiento | Puede aprovechar el computador ya disponible |
| Instalación permanente | Compacta y dedicable al prototipo | Adecuada si existe un PC fijo disponible |
| Procesamiento intensivo | Recursos limitados según modelo | Puede ofrecer más CPU/GPU/RAM; depende del PC |
| Conexión con ESP32 | USB serial o red | También USB serial o red |
| Interfaz electrónica | GPIO e interfaces accesibles, con protección | Normalmente adaptadores externos |
| Operación sin pantalla | Posible con servicios y administración remota | También posible si se configura |
| Costo | Incluir fuente, almacenamiento, caja y refrigeración | Incluir disponibilidad, periféricos y operación |
| Mantenimiento | Linux, almacenamiento y recuperación | También necesita mantenimiento y recuperación |

**Escoger Raspberry** cuando el prototipo necesita un nodo pequeño, dedicado y local con recursos suficientes. **Escoger PC** cuando ya hay uno dedicado, el proyecto exige software o cómputo específico, o se busca validar la idea antes de adquirir hardware. **Escoger solo ESP32** cuando las funciones caben en el microcontrolador y no se justifica otra capa.

No es obligatorio añadir una Raspberry a todo proyecto. Debe resolver una necesidad identificable.

## 6. Ejemplo: pasar de demostración a sistema instalado

### Desarrollo
El estudiante conecta ESP32 al PC para programar, revisar mensajes y probar el receptor.

### Integración
ESP32 queda instalado junto al sensor. Raspberry recibe, valida, almacena y ofrece una interfaz. El PC consulta cuando se necesita, sin ser requisito para que se registren datos.

```text
Sensor / actuador
       ↕
ESP32: adquisición + control local + protecciones
       ↕ USB serial o red
Raspberry: recepción → validación → almacenamiento → interfaz
       ↕ red
PC / navegador: configuración y consulta
```

Ejemplo de tanque: el ESP32 puede mantener las condiciones de control local; la Raspberry conserva históricos y presenta tendencias. Si la Pi reinicia, el control esencial debe continuar **porque así fue diseñado**, no simplemente por usar dos placas.

Si se exige conservar datos mientras la Pi está caída, hace falta un mecanismo adicional: almacenamiento temporal, secuencias y reenvío desde el nodo, con manejo de duplicados. El CSV en la Pi no recupera mediciones que nunca recibió.

## 7. Linux: qué aporta y qué exige

Linux administra procesos, memoria, dispositivos, usuarios y archivos. Python utiliza sus interfaces para trabajar con hardware y datos.

- **Proceso:** programa en ejecución; termina si se detiene o falla.
- **Servicio:** aplicación administrada para operar de forma controlada. En próximas prácticas se configurará con systemd.
- **Permisos:** limitan quién puede acceder a recursos; no es necesario ejecutar todo con sudo.
- **Logs:** ayudan a explicar fallas, distintos de las mediciones de negocio.
- **Recuperación:** debe probarse. Guardar un script no configura ejecución automática.

La instalación estándar no ofrece plazos deterministas garantizados. `time.sleep(2)` introduce una pausa, pero lectura, escritura y planificación añaden tiempo. Para control crítico se diseña una capa apropiada y se valida su comportamiento.

## 8. Interfaces y protocolos

- **USB serial:** la placa ESP32, mediante su interfaz USB o conversor, presenta un puerto al sistema. Requiere cable de datos, identificación del puerto y parámetros compatibles.
- **UART en pines:** enlace eléctrico diferente de conectar USB. Requiere revisar TX/RX/GND y niveles; no conectar señales de 5 V a GPIO.
- **Wi-Fi/Ethernet:** aportan conectividad de red.
- **HTTP/MQTT:** alternativas de intercambio sobre red.
- **JSON:** formato de mensajes; no reemplaza el transporte.

Un mensaje debe tener campos, unidades y reglas de validación. Para robustez pueden requerirse ID de nodo, secuencia, tiempo y estrategia ante desconexiones. No asumir recepción solo porque el emisor imprime “enviado”.

## 9. Qué medimos en el laboratorio

### Temperatura del procesador
La lectura de `/sys/class/thermal/thermal_zone0/temp` en la configuración usada se expresa en milésimas de °C: 54800 / 1000 = 54,8 °C. La ruta debe comprobarse en la placa; no es una interfaz universal para cualquier computador.

Esta temperatura describe un estado interno, **no temperatura ambiente**. El umbral de clasificación es didáctico y no cambia la refrigeración ni sustituye protecciones.

### Memoria RAM
Linux publica información en `/proc/meminfo`. No es una captura estática: consultar nuevamente puede devolver otros valores.

- **MemTotal:** RAM utilizable por Linux.
- **MemAvailable:** estimación disponible para nuevas aplicaciones sin intercambio, incluyendo memoria recuperable.
- **MemFree:** memoria completamente libre; no es lo mismo.

```text
uso_estimado_pct = (MemTotal - MemAvailable) / MemTotal × 100
```

Los dos valores deben tener la misma unidad. El porcentaje es una estimación de ocupación, no una medición completa de presión de memoria. Caché e intercambio requieren interpretación adicional. Véase [documentación del kernel](https://docs.kernel.org/filesystems/proc.html).

## 10. Adquisición, validación y clasificación

1. **Adquirir:** consultar la fuente.
2. **Interpretar:** extraer número y unidad.
3. **Validar:** comprobar presencia, finitud y relaciones plausibles.
4. **Clasificar:** aplicar una condición a datos válidos.
5. **Persistir:** guardar con metadatos.
6. **Verificar:** contrastar resultado esperado con observado.

**NORMAL:** dato válido inferior al umbral. **ALERTA:** dato válido igual o superior. **ERROR:** no hay dato válido. Un error no debe convertirse en un cero ficticio; el detalle explica la causa.

El umbral no describe por sí solo gravedad: debe justificarse para cada aplicación. La prueba modifica el umbral, no fuerza sobrecalentamiento ni agotamiento de RAM.

## 11. CSV, fecha y trazabilidad

CSV organiza registros en filas y columnas. Es fácil de inspeccionar e intercambiar, pero no sustituye todas las funciones de una base de datos. Deben documentarse separador, codificación, unidades y encabezados; utilizar `csv.writer` para campos que contengan comas o comillas.

- Una fila por intento de adquisición.
- Fecha/hora con zona e identificación de parámetros.
- Campos vacíos ante fallo del dato y detalle de error.
- Append para conservar filas; encabezado solo al crear archivo vacío.
- Política de rotación y respaldos si el sistema opera continuamente.

Hora local correcta exige sincronización/configuración. Un sello de hora incorrecto perjudica el análisis. `flush()` transfiere datos al sistema, pero no garantiza integridad ante cortes. Parar ordenadamente y probar recuperación forman parte del diseño.

SQLite, consultas y dashboard se incorporan después. El dashboard no debe ser requisito para que el proceso receptor continúe.

## 12. Limitaciones y operación responsable

La Raspberry no es automáticamente un controlador industrial certificado ni un dispositivo de seguridad. El sistema requiere evaluar alimentación, entorno, aislamiento, protecciones, almacenamiento, copias de seguridad, watchdog y pruebas según los riesgos reales.

microSD puede fallar o degradarse; SSD puede ser alternativa con accesorios apropiados. Rendimiento depende también de I/O y refrigeración. Arquitectura Arm puede limitar software disponible para x86. El costo del conjunto puede superar al de un PC existente.

Acceso remoto y operación local son distintos: Connect necesita conectividad con su servicio para la sesión; la aplicación local puede seguir funcionando sin Internet si se diseñó así. Acceso por LAN también depende de la red y de los servicios configurados. No compartir credenciales ni enlaces de autorización.

## 13. Respuesta breve para explicar en clase

> La Raspberry puede convenir como integrador porque permite dejar un computador pequeño y dedicado dentro del proyecto. El ESP32 adquiere y controla; la Raspberry recibe, procesa y conserva datos. El PC se utiliza para desarrollar y consultar. Un PC también puede integrar todo: elegimos según instalación, recursos, operación y costo total.

## 14. Preguntas para sustentar el informe

1. ¿Qué necesidad concreta del proyecto justifica Raspberry en lugar de un PC disponible?
2. ¿Qué tareas corresponden al ESP32 y cuáles a Linux?
3. ¿Qué ocurriría si se cierra Connect, falla Internet o se reinicia la Pi? Son escenarios distintos.
4. ¿Qué datos se perderían durante una desconexión y cómo podrían recuperarse?
5. ¿Qué validaciones necesitan antes de usar una lectura?
6. ¿Qué limitación del CSV justificaría migrar a SQLite?

Usar estas preguntas como apoyo a la discusión del informe vigente; no cambia extensión, fecha ni criterios publicados.

## Fuentes y ampliación

- [Especificaciones Raspberry Pi 5](https://www.raspberrypi.com/products/raspberry-pi-5/).
- [Hardware e interfaces Raspberry Pi](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html).
- [Raspberry Pi OS](https://www.raspberrypi.com/documentation/computers/os.html).
- [Raspberry Pi Connect](https://www.raspberrypi.com/documentation/services/connect.html).
- [Linux /proc y meminfo](https://docs.kernel.org/filesystems/proc.html).
- [Interfaz térmica sysfs](https://docs.kernel.org/driver-api/thermal/sysfs-api.html).
- [Python csv](https://docs.python.org/3/library/csv.html), [pathlib](https://docs.python.org/3/library/pathlib.html), [time](https://docs.python.org/3/library/time.html).
- [Semana 12 del curso](../../../semanas/semana-12-raspberry-pi-linux-sbc/marco-teorico.md).

Las comparaciones de conveniencia son análisis de diseño para el curso; no son benchmarks ni promesas de ahorro medido.
