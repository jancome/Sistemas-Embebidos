# Laboratorio: adquisición, validación y registro de datos en Raspberry Pi
**Sesión y entrega de clase: 4 de noviembre de 2026 (Colombia).**  
Complemento práctico del Lab 09, con adelanto de procesamiento y persistencia. Compatible con Raspberry Pi 4/5 y Raspberry Pi OS. No sustituye el enlace ESP32–Raspberry, SQLite ni el dashboard de los laboratorios siguientes.

## Lectura de apoyo

[Marco teórico ampliado: características, ventajas, limitaciones y Raspberry frente a PC](marco-teorico.md). Explica arquitectura ESP32–Raspberry, Linux, adquisición, validación y CSV, con preguntas para sustentar el informe.

## Objetivo
Construir y comprobar el flujo **fuente Linux → adquisición Python → validación → clasificación → CSV**; distinguir almacenamiento, memoria y sensor interno. Acceso mediante Raspberry Pi Connect (escritorio) o local. SSH es opcional.

## Organización y requisitos
Grupos de **3 estudiantes**, según las normas del curso. Roles rotativos: programación, pruebas y documentación; registrar aportes individuales. Raspberry configurada y actualizada, Python 3 y Thonny/editor. Solo biblioteca estándar: no instalar paquetes. No usar GPIO ni componentes externos. No publicar contraseñas, IP públicas ni enlaces de autorización.

## Secuencia propuesta (120 minutos)
15 min hardware/video; 35 min demostración de temperatura; 45 min reto RAM; 15 min pruebas y análisis; 10 min entrega.
Antes de clase el docente debe ensayar adquisición y escritura en la placa real. El código publicado no implica que el hardware de cada grupo ya esté verificado.

## Parte A — demostración del docente: temperatura CPU
Guía detallada y programa: [monitor_temperatura.py](monitor_temperatura.py).

1. Mostrar [Introducing Raspberry Pi 5](https://www.youtube.com/watch?v=yul4gq_LrOI). Pausar para reconocer CPU, RAM, microSD, USB, red y refrigeración; no es necesario memorizar especificaciones ni seguir marcas de tiempo.
2. Explicar: CPU ejecuta; RAM mantiene datos temporales; microSD conserva código/CSV. La temperatura medida es la del procesador, **no la del ambiente**.
3. Abrir terminal **dentro del escritorio de la Raspberry** y ejecutar:
   ```bash
   vcgencmd measure_temp
   mkdir -p ~/CORTE3/Clase1/MonitorCPU
   cd ~/CORTE3/Clase1/MonitorCPU
   ```
4. Descargar el programa enlazado (botón Raw/Download de GitHub) y guardarlo como `monitor_temperatura.py` en esa carpeta, o pegar su contenido en Thonny y guardar con ese nombre. No copiar mensajes Traceback ni los delimitadores de Markdown.
5. Explicar parámetros, lectura de `/sys/class/thermal/thermal_zone0/temp` en milésimas de °C, conversión entre 1000, validación, decisión, manejo de error y CSV.
6. Ejecutar:
   ```bash
   python3 monitor_temperatura.py
   ```
7. Dejar ~30 segundos y detener con **Ctrl+C** en la terminal. Si se ejecuta desde Thonny usar Stop, y comprobar el CSV; Ctrl+C permite el cierre previsto en el programa.
8. Abrir `temperatura.csv`, junto al script. Mostrar fecha con zona horaria, temperatura, umbral, estado y detalle. Los valores son mediciones reales del equipo; no usar datos de ejemplo como evidencia.
9. Detener, cambiar el umbral por encima/debajo de una lectura reciente, guardar y ejecutar de nuevo: NORMAL/ALERTA. No calentar la placa. Es un **umbral didáctico**, no límite de daño ni control del ventilador.
10. Detener, cambiar SOLO `RUTA_SENSOR` a `Path("/ruta_inexistente/temp")`, ejecutar y observar ERROR con temperatura vacía; detener y restaurar ruta correcta. No modificar archivos de /sys.
11. Mostrar recuperación manual al restaurar la configuración. El intervalo es aproximado: el procesamiento añade tiempo. El CSV usa append; conserva las filas anteriores. No cambiar encabezados entre ejecuciones en el mismo archivo.

## Parte B — reto estudiantil: monitor de memoria RAM

Implementar `monitor_ram.py`, aplicando el patrón de adquisición, validación, clasificación y registro a una fuente diferente de la temperatura. La explicación y el procedimiento están completos en esta misma guía.

**Todos los valores numéricos de ejemplo son ilustrativos.** Cada grupo debe sustituirlos por sus mediciones reales y justificar sus conclusiones con archivos y filas concretos.

### Empezar por una pregunta observable
**Pregunta:** ¿qué proporción de la RAM utilizable no está disponible para nuevas aplicaciones en este momento?

No comenzamos con una declaración como “la memoria está mal”. Necesitamos una fuente, una definición de uso y mediciones. El ejercicio estudia una estimación de ocupación y el comportamiento del programa; no es un diagnóstico completo de rendimiento ni una prueba física de la RAM.

**Para decir en clase:** “Antes de programar debemos saber qué queremos conocer y con qué dato podemos responder”.

### Encontrar la fuente antes de extraer valores
En la terminal de la Raspberry ejecutar:
```bash
cat /proc/meminfo
```
También se puede consultar desde Python:
```python
from pathlib import Path
contenido = Path("/proc/meminfo").read_text()
print(contenido)
```
Localizar MemTotal, MemAvailable y MemFree. La información la proporciona el kernel; no es una tabla que el estudiante deba rellenar manualmente. Si se consulta de nuevo, los valores pueden variar.

**Ejemplo ilustrativo:**
```text
MemTotal:       8000000 kB
MemFree:        1000000 kB
MemAvailable:   6000000 kB
```

| Campo | Interpretación | Uso en esta actividad |
|---|---|---|
| MemTotal | RAM utilizable por Linux | Referencia total para el porcentaje |
| MemAvailable | Estimación disponible para nuevas aplicaciones sin intercambio | Referencia de disponibilidad |
| MemFree | Memoria completamente libre | Sirve para discutir por qué no equivale a disponibilidad |

Linux utiliza memoria como caché; parte puede recuperarse. MemAvailable incluye una estimación de memoria recuperable y no se calcula simplemente tomando MemFree. Su definición está documentada por el kernel, no se deduce de una captura aislada.

En esta interfaz la etiqueta kB representa cantidades de 1024 bytes, por eso el CSV emplea el sufijo `_kib`. No hay que convertir a GB para obtener un porcentaje: basta usar la misma unidad en total y disponible.

**Pregunta al grupo:** “¿Qué nombre de campo usaríamos para estimar lo que podría aprovechar otra aplicación? ¿Por qué no elegir automáticamente el campo que contiene la palabra Free?”.

### Justificar la fórmula, paso por paso
A partir del ejemplo:
```text
Total utilizable = 8 000 000 KiB
Disponible estimada = 6 000 000 KiB

Cantidad no disponible estimada:
8 000 000 − 6 000 000 = 2 000 000 KiB

Fracción respecto al total:
2 000 000 / 8 000 000 = 0,25

Expresada como porcentaje:
0,25 × 100 = 25 %
```

Por eso usamos:
```text
uso_estimado_pct = (total - disponible) / total * 100
```

Restamos para obtener el complemento de la disponibilidad; dividimos entre el total para expresar una proporción; multiplicamos por 100 para expresarla por cada cien unidades.

**Interpretación permitida:** “En esta lectura, el uso estimado con el criterio definido es 25 % y la disponibilidad estimada es 75 %”.

**Lo que todavía no podemos concluir:** “Hay un fallo”, “el sistema está lento” o “esa memoria se desperdicia”. Para diagnosticar presión, rendimiento o una fuga harían falta otras medidas y observación temporal.

**Verificación del estudiante:** seleccionar total y disponible de **una misma fila** del CSV, hacer el cálculo a mano y contrastar el porcentaje. No mezclar capturas de momentos distintos.

### Entender qué parte del código obtiene cada dato
Seguir esta correspondencia, sin memorizar todo el programa:
| Operación | Papel en el razonamiento |
|---|---|
| Leer /proc/meminfo | Obtener observaciones |
| Separar líneas y campos | Interpretar el formato |
| Buscar MemTotal y MemAvailable por nombre | Seleccionar las variables necesarias |
| Convertir textos a enteros | Poder operar con números |
| Aplicar la fórmula | Obtener la medida definida |
| Comparar con el umbral | Aplicar una regla de clasificación |
| Escribir el CSV | Conservar la evidencia |

No tomar los valores por “línea 1” o “línea 3”: el contrato relevante es el nombre del campo. El prefijo `def` define una función; llamarla ejecuta ese bloque. Separar adquisición, validación y registro facilita localizar el origen de una falla.

### Validar antes de calcular o clasificar
Cada comprobación tiene un motivo:
| Comprobación | Qué evita |
|---|---|
| Ambos campos presentes | Calcular con una variable ausente |
| Unidad y formato esperados | Interpretar otro tipo de dato como memoria |
| Números válidos | Operar con texto incorrecto |
| Total > 0 | División entre cero o total imposible |
| 0 <= disponible <= total | Porcentajes negativos o superiores a 100 por datos incoherentes |
| Porcentaje finito entre 0 y 100 | Propagar un resultado inválido |
| Intervalo > 0 y umbral entre 0 y 100 | Ejecutar con una configuración incoherente |

Estas condiciones detectan ciertos datos inválidos; no certifican la integridad física de la memoria.

### Diferenciar medición y decisión
La lectura y la fórmula producen el porcentaje. **El umbral lo elegimos nosotros**: no lo proporciona MemAvailable ni hay en esta actividad un valor universal de 70 % que signifique falla.

Regla de la práctica:
```text
Dato válido y porcentaje < umbral   → NORMAL
Dato válido y porcentaje >= umbral  → ALERTA
No hay dato válido                 → ERROR
```

**Ejemplo ilustrativo con 25 %:**
| Porcentaje | Umbral elegido | Estado | Explicación |
|---:|---:|---|---|
| 25 | 70 | NORMAL | 25 < 70 |
| 25 | 20 | ALERTA | 25 >= 20 |

Cambiar el umbral puede cambiar el estado sin que haya cambiado el uso de memoria. En la Raspberry real la lectura fluctúa, por lo que se comprueba la condición en cada fila.

**Conclusión de esta prueba:** la decisión implementada responde a la comparación especificada.

**No demuestra:** que la RAM se haya saturado, que exista una emergencia ni que el umbral sea adecuado para un proceso real. No saturar RAM para producir el estado.

### Distinguir ERROR de ALERTA
Para probar ERROR se cambia temporalmente **solo la ruta escrita en el código** a `/ruta_inexistente/meminfo`. No borrar ni modificar archivos de /proc.

Si falla esa lectura:
- No conocemos el total/disponible/porcentaje de esa adquisición.
- Esos campos de medición quedan vacíos.
- Se conserva la fecha, el umbral de configuración, ERROR y el detalle.
- No se inventa 0 % ni se reutiliza el dato anterior como si fuera nuevo.

Restaurar la ruta y ejecutar otra vez comprueba que vuelve a adquirir datos. Esta recuperación de configuración es **manual**.

**Conclusión permitida:** “Ante una ruta inexistente, el programa registró ERROR y volvió a medir después de restaurar la ruta”.

**No permite concluir:** que falló físicamente la RAM, que se probó una desconexión USB o que ya existe recuperación automática ante cualquier falla.

### Comprobar muestreo y persistencia con evidencia
#### Intervalo
Comparar registros consecutivos de una misma ejecución:
```text
Ejemplo ilustrativo:
18:10:00 → 18:10:05 → 18:10:10

Separación media entre primera y tercera lectura:
(10 segundos) / (3 lecturas - 1) = 5 segundos
```

La fórmula para un tramo continuo es `(hora_final - hora_inicial) / (cantidad_de_lecturas - 1)`, con al menos dos lecturas. No aplicarla mezclando ejecuciones separadas por pausas manuales. Los sellos con resolución de segundos no revelan retardos menores a un segundo.

Al cambiar de 5 s a 2 s, la expectativa es menor separación temporal y más registros en igual duración. Los tiempos reales incluyen trabajo y planificación de Linux; no son una garantía de tiempo real.

#### Persistencia
1. Detener de forma ordenada.
2. Abrir memoria.csv y comprobar filas reales.
3. Guardar una copia para la prueba.
4. Ejecutar de nuevo y verificar nuevas filas sin borrar las anteriores.

Eso demuestra conservación en el archivo entre ejecuciones. No equivale a probar integridad ante cortes eléctricos ni arranque automático. Si una hoja de cálculo muestra una sola columna, importar como CSV con separador coma; alternativamente inspeccionar con editor de texto.

### Requisitos funcionales
- Intervalo inicial **5 segundos**, configurable, finito y mayor que cero.
- Umbral porcentual configurable entre 0 y 100; condición de ALERTA: porcentaje >= umbral.
- Validar presencia de ambas claves, números válidos, total > 0 y 0 <= disponible <= total; porcentaje finito entre 0 y 100.
- Si lectura/conversión/validación falla, registrar ERROR y detalle, dejando vacíos los campos de medición (total, disponible y porcentaje); conservar el umbral configurado; no usar ceros inventados ni conservar la lectura anterior como nueva.
- Mostrar cada resultado y guardar `memoria.csv` junto al script; agregar sin borrar, encabezado solo nuevo/vacío.
- Columnas: `fecha_hora,mem_total_kib,mem_disponible_kib,porcentaje_usado,umbral_pct,estado,detalle`.
- Fecha con zona horaria, Ctrl+C para finalizar; no ejecutar como root.
- Un error de escritura debe comunicarse claramente y detener el registro; no afirmar que se guardó una fila si falló el disco.

### Pruebas mínimas
Detener antes de editar, guardar y ejecutar. Guardar CSV separado por prueba o identificar el tramo por fecha/hora.
| ID | Acción | Evidencia esperada |
|---|---|---|
| P1 | Intervalo 5 s, ejecutar al menos 60 s | Al menos 12 registros; total/disponible/porcentaje coherentes |
| P2 | Intervalo 2 s, ejecutar al menos 30 s | Al menos 12 registros; menor separación temporal |
| P3 | Umbral mayor que uso observado | NORMAL si uso permanece inferior |
| P4 | Umbral menor o igual al uso observado | ALERTA cuando se cumple la condición |
| P5 | Ruta de lectura temporal inexistente; luego restaurar | ERROR con mediciones vacías y detalle; posteriormente lectura válida |

Los umbrales son decisiones didácticas, no límites universales de fallo de la RAM. Cambiarlos demuestra la regla de clasificación, no saturación real. Una ruta inexistente demuestra manejo de error de adquisición, no daño físico ni recuperación automática. Para cada resultado identificar el archivo y la fila/hora, calcular o comparar y declarar qué se pudo demostrar.

No saturar RAM ni abrir procesos en masa para generar ALERTA. Revisar condición por fila porque el uso fluctúa. Un ejemplo numérico calculado a mano puede ayudar, pero se etiqueta como ejemplo y no sustituye mediciones reales.

### Relacionar cada prueba con lo que puede demostrar
| Prueba | Qué observar | Qué justifica | Qué no justifica |
|---|---|---|---|
| P1: lectura y CSV | Total/disponible, cálculo manual y filas | Adquisición y cálculo coherentes con la fuente | Estado físico o rendimiento general de RAM |
| P2: cambio de intervalo | Diferencias entre timestamps de cada tramo | Cambio de cadencia observable | Periodicidad exacta garantizada |
| P3 y P4: umbrales | Porcentaje y umbral de cada fila | Regla NORMAL/ALERTA coherente | Saturación real o umbral de seguridad |
| P5: ruta inválida/restaurada | Campos vacíos, detalle y siguiente lectura válida | Manejo del fallo de lectura y restauración manual | Falla física ni recuperación automática de todo el sistema |

Distinguir expectativa de observación: si no coincide, informar discrepancia y revisar. No adaptar los datos para que encajen con la expectativa.

<a id="conclusiones-con-evidencia"></a>

### Cómo construir conclusiones con evidencia
Usar esta secuencia:
```text
Observación → cálculo o comparación → interpretación → límite
```

**Modelo con casillas para sus datos reales:**
> En [archivo, fila/hora] registramos total [T] y disponible [D]. Aplicando (T−D)/T×100 obtuvimos [P] %. Con umbral [U], la comparación [P < U o P >= U] corresponde a [estado]. El CSV registró [resultado observado]. Esto permite concluir [comportamiento comprobado]. No permite concluir [algo que la prueba no midió].

Para el intervalo:
> En el tramo [inicio-fin], [N] registros tienen una separación media de [valor]. Al comparar con el tramo de otro intervalo observamos [diferencia]. La medición utiliza sellos de segundos y no demuestra periodicidad de tiempo real.

Para el fallo:
> Al usar la ruta inexistente, en [fila/hora] se registró ERROR con [detalle] y valores de medición vacíos. Tras restaurarla, [fila/hora] volvió a registrar datos válidos. Se comprobó la restauración manual del acceso a la fuente, no una falla física.

Una conclusión no es “aprendimos mucho”, “el programa funciona” o un resultado copiado del ejemplo. Debe indicar qué evidencia la respalda.

## Entregable de hoy — antes de terminar la sesión
Entregar **un ZIP por grupo en Teams**, con nombre `grupoXX_monitoreo_linux_2026-11-04.zip`:
```text
grupoXX/
  monitor_ram.py
  datos/                 # CSV de las pruebas
  evidencias/            # Capturas legibles, sin credenciales
  informe.pdf
```
El informe es **breve, de 2–4 páginas** y se elabora con los resultados de hoy; usar la [plantilla](plantilla_informe.md). No se exige otro informe posterior con fecha no acordada. Si faltó una prueba, declararla como pendiente, no inventarla. Código y CSV no cuentan en las páginas.

### Informe: contenido obligatorio
1. Grupo, integrantes, roles y aportes.
2. Objetivo, modelo Pi, OS/Python y método de acceso.
3. Diagrama fuente → cálculo → validación → clasificación → CSV; explicación de MemAvailable y fórmula.
4. Tabla P1–P5 con parámetros, esperado, observado y evidencia (archivo y fila/hora).
5. Un cálculo manual usando una fila real; comparación NORMAL/ALERTA/ERROR; fallas y limitaciones.
6. Qué cambiaría si los datos vinieran del ESP32 por USB serial (adquisición, mensaje, timeout, validación y recuperación), conservando procesamiento/registro.
7. Conclusiones y fuentes: respaldar cada conclusión con datos, cálculo o comparación, interpretación y límite de la prueba; explicar ayuda externa recibida y comprensión propia.

## Criterios de revisión
Lista de comprobación del laboratorio, **sin modificar pesos de EVALUACION.md**:
- Adquisición/cálculo correcto con MemTotal y MemAvailable.
- Validación y manejo de los tres estados.
- CSV trazable, persistente y coherente.
- Pruebas verificables y análisis del informe.
- Organización, comentarios útiles y sustentación individual.
Cada integrante debe explicar una sección y una prueba. La tarea, hora exacta de cierre, calificación y retroalimentación se gestionan en Teams.

## Conexión con el proyecto ESP32–Raspberry

No llegamos a la conclusión “necesitamos Raspberry para todo” por medir RAM. Esta actividad demuestra un patrón de software que puede reutilizarse.

La aplicación integrada tendrá que cambiar adquisición y formato: puerto USB serial o red, campos del mensaje, unidades, timeout y tratamiento de reconexión. Se conserva el razonamiento de validar, procesar, clasificar y guardar, adaptado al nuevo dato. Esas funciones futuras deben probarse; no se consideran ya implementadas.

**Preguntas de salida:** ¿qué medimos?, ¿cómo lo calculamos?, ¿qué parámetro elegimos?, ¿qué demostró cada prueba?, ¿qué no podemos afirmar todavía?

Próximos pasos del curso: enlace USB serial u otra comunicación seleccionada, SQLite, dashboard y ejecución como servicio. El control esencial debe diseñarse para continuar ante una interrupción de la supervisión.

## Referencias
- [Lab 09](../README.md), [Lab 10](../../lab-10-uart-esp32-raspberry/README.md), [Lab 11](../../lab-11-sqlite-dashboard-servicio/README.md).
- [Normas](../../../NORMAS_DE_CLASE.md), [Evaluación](../../../EVALUACION.md).
- Linux: `/proc/meminfo` y [documentación proc](https://docs.kernel.org/filesystems/proc.html).
- [Python csv](https://docs.python.org/3/library/csv.html), [pathlib](https://docs.python.org/3/library/pathlib.html).
