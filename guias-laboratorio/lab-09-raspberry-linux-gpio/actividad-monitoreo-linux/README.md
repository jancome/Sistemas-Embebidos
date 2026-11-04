# Laboratorio: adquisición, validación y registro de datos en Raspberry Pi
**Sesión y entrega de clase: 4 de noviembre de 2026 (Colombia).**  
Complemento práctico del Lab 09, con adelanto de procesamiento y persistencia. Compatible con Raspberry Pi 4/5 y Raspberry Pi OS. No sustituye el enlace ESP32–Raspberry, SQLite ni el dashboard de los laboratorios siguientes.

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
**No repetir la temperatura:** implementar `monitor_ram.py`, usando como referencia la arquitectura anterior, no sustituyendo nombres de variables sin comprenderlos.

### Fuente y cálculo
Consultar `/proc/meminfo`:
```python
from pathlib import Path
contenido = Path("/proc/meminfo").read_text()
print(contenido)
```
Localizar **MemTotal** y **MemAvailable**, extraer sus números por nombre (no por posición fija). Ambos aparecen en la misma unidad; la unidad se cancela en el cociente.
```text
porcentaje_usado = (MemTotal - MemAvailable) / MemTotal * 100
```
**MemAvailable no es MemFree.** Es una estimación de memoria utilizable por nuevas aplicaciones sin intercambio, incluyendo memoria recuperable. La cifra describe uso estimado, no presión de memoria por sí sola. Puede diferir del redondeo o criterio de otra herramienta.

### Requisitos funcionales
- Intervalo inicial **5 segundos**, configurable, finito y mayor que cero.
- Umbral porcentual configurable entre 0 y 100; condición de ALERTA: porcentaje >= umbral.
- Validar presencia de ambas claves, números válidos, total > 0 y 0 <= disponible <= total; porcentaje finito entre 0 y 100.
- Si lectura/conversión/validación falla, registrar ERROR y detalle, dejando las columnas numéricas vacías; no usar ceros inventados ni conservar la lectura anterior como nueva.
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
| P5 | Ruta de lectura temporal inexistente; luego restaurar | ERROR con numéricos vacíos y detalle; posteriormente lectura válida |

No saturar RAM ni abrir procesos en masa para generar ALERTA. Revisar condición por fila porque el uso fluctúa. Un ejemplo numérico calculado a mano puede ayudar, pero se etiqueta como ejemplo y no sustituye mediciones reales.

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
7. Conclusiones y fuentes; explicar ayuda externa recibida y comprensión propia.

## Criterios de revisión
Lista de comprobación del laboratorio, **sin modificar pesos de EVALUACION.md**:
- Adquisición/cálculo correcto con MemTotal y MemAvailable.
- Validación y manejo de los tres estados.
- CSV trazable, persistente y coherente.
- Pruebas verificables y análisis del informe.
- Organización, comentarios útiles y sustentación individual.
Cada integrante debe explicar una sección y una prueba. La tarea, hora exacta de cierre, calificación y retroalimentación se gestionan en Teams.

## Conexión con el curso
Esta práctica prepara recepción/procesamiento de datos externos. El ESP32 realizará adquisición/control local; la Pi procesará/guardará/visualizará. El control esencial no debe depender de la interfaz Linux. Próximos pasos: enlace USB serial/otra comunicación seleccionada, SQLite, dashboard y servicio.

## Referencias
- [Lab 09](../README.md), [Lab 10](../../lab-10-uart-esp32-raspberry/README.md), [Lab 11](../../lab-11-sqlite-dashboard-servicio/README.md).
- [Normas](../../../NORMAS_DE_CLASE.md), [Evaluación](../../../EVALUACION.md).
- Linux: `/proc/meminfo` y [documentación proc](https://docs.kernel.org/filesystems/proc.html).
- [Python csv](https://docs.python.org/3/library/csv.html), [pathlib](https://docs.python.org/3/library/pathlib.html).
