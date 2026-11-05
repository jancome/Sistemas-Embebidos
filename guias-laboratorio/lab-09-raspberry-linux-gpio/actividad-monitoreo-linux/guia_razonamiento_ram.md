# Cómo razonar y explicar el monitor de RAM

Esta guía acompaña el [laboratorio](README.md) y la [plantilla de informe](plantilla_informe.md). Explica el camino desde una pregunta hasta una conclusión. **Los números de los ejemplos son ilustrativos; cada grupo debe sustituirlos por sus mediciones.**

## 1. Empezar por una pregunta observable
**Pregunta:** ¿qué proporción de la RAM utilizable no está disponible para nuevas aplicaciones en este momento?

No comenzamos con una declaración como “la memoria está mal”. Necesitamos una fuente, una definición de uso y mediciones. El ejercicio estudia una estimación de ocupación y el comportamiento del programa; no es un diagnóstico completo de rendimiento ni una prueba física de la RAM.

**Para decir en clase:** “Antes de programar debemos saber qué queremos conocer y con qué dato podemos responder”.

## 2. Encontrar la fuente antes de extraer valores
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

## 3. Justificar la fórmula, paso por paso
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

## 4. Entender qué parte del código obtiene cada dato
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

## 5. Validar antes de calcular o clasificar
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

## 6. Diferenciar medición y decisión
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

## 7. Distinguir ERROR de ALERTA
Para probar ERROR se cambia temporalmente **solo la ruta escrita en el código** a `/ruta_inexistente/meminfo`. No borrar ni modificar archivos de /proc.

Si falla esa lectura:
- No conocemos el total/disponible/porcentaje de esa adquisición.
- Esos campos de medición quedan vacíos.
- Se conserva la fecha, el umbral de configuración, ERROR y el detalle.
- No se inventa 0 % ni se reutiliza el dato anterior como si fuera nuevo.

Restaurar la ruta y ejecutar otra vez comprueba que vuelve a adquirir datos. Esta recuperación de configuración es **manual**.

**Conclusión permitida:** “Ante una ruta inexistente, el programa registró ERROR y volvió a medir después de restaurar la ruta”.

**No permite concluir:** que falló físicamente la RAM, que se probó una desconexión USB o que ya existe recuperación automática ante cualquier falla.

## 8. Comprobar muestreo y persistencia con evidencia
### Intervalo
Comparar registros consecutivos de una misma ejecución:
```text
Ejemplo ilustrativo:
18:10:00 → 18:10:05 → 18:10:10

Separación media entre primera y tercera lectura:
(10 segundos) / (3 lecturas - 1) = 5 segundos
```

La fórmula para un tramo continuo es `(hora_final - hora_inicial) / (cantidad_de_lecturas - 1)`, con al menos dos lecturas. No aplicarla mezclando ejecuciones separadas por pausas manuales. Los sellos con resolución de segundos no revelan retardos menores a un segundo.

Al cambiar de 5 s a 2 s, la expectativa es menor separación temporal y más registros en igual duración. Los tiempos reales incluyen trabajo y planificación de Linux; no son una garantía de tiempo real.

### Persistencia
1. Detener de forma ordenada.
2. Abrir memoria.csv y comprobar filas reales.
3. Guardar una copia para la prueba.
4. Ejecutar de nuevo y verificar nuevas filas sin borrar las anteriores.

Eso demuestra conservación en el archivo entre ejecuciones. No equivale a probar integridad ante cortes eléctricos ni arranque automático. Si una hoja de cálculo muestra una sola columna, importar como CSV con separador coma; alternativamente inspeccionar con editor de texto.

## 9. Relacionar cada prueba con lo que puede demostrar
| Prueba | Qué observar | Qué justifica | Qué no justifica |
|---|---|---|---|
| P1: lectura y CSV | Total/disponible, cálculo manual y filas | Adquisición y cálculo coherentes con la fuente | Estado físico o rendimiento general de RAM |
| P2: cambio de intervalo | Diferencias entre timestamps de cada tramo | Cambio de cadencia observable | Periodicidad exacta garantizada |
| P3 y P4: umbrales | Porcentaje y umbral de cada fila | Regla NORMAL/ALERTA coherente | Saturación real o umbral de seguridad |
| P5: ruta inválida/restaurada | Campos vacíos, detalle y siguiente lectura válida | Manejo del fallo de lectura y restauración manual | Falla física ni recuperación automática de todo el sistema |

Distinguir expectativa de observación: si no coincide, informar discrepancia y revisar. No adaptar los datos para que encajen con la expectativa.

## 10. Cómo construir una conclusión del informe
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

## 11. Qué transferimos al proyecto con ESP32
No llegamos a la conclusión “necesitamos Raspberry para todo” por medir RAM. Esta actividad demuestra un patrón de software que puede reutilizarse.

La aplicación integrada tendrá que cambiar adquisición y formato: puerto USB serial o red, campos del mensaje, unidades, timeout y tratamiento de reconexión. Se conserva el razonamiento de validar, procesar, clasificar y guardar, adaptado al nuevo dato. Esas funciones futuras deben probarse; no se consideran ya implementadas.

**Preguntas de salida:** ¿qué medimos?, ¿cómo lo calculamos?, ¿qué parámetro elegimos?, ¿qué demostró cada prueba?, ¿qué no podemos afirmar todavía?

## Referencias
- [Linux: /proc y definición de meminfo](https://docs.kernel.org/filesystems/proc.html).
- [Marco teórico del laboratorio](marco-teorico.md).
- [Pruebas y entrega](README.md).
