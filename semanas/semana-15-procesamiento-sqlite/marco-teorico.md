# Marco teórico – Semana 15

## Validación, procesamiento y persistencia con SQLite

### Propósito formativo

Una secuencia de mensajes solo se convierte en información confiable si conserva procedencia, tiempo, unidad y calidad. La base de datos no debe aceptar silenciosamente cualquier valor ni mezclar adquisición, validación y presentación.

## 1. Pipeline de datos

```text
bytes → parseo → validación → objeto de dominio → transformación → transacción SQLite
```

Cada etapa tiene una salida definida. Un error de parseo no se convierte en cero; se registra como dato rechazado. La validación incluye:

- tipo y presencia de campos;
- rango físico y tasa de cambio plausible;
- secuencia y duplicado;
- timestamp y antigüedad;
- unidad y versión de esquema;
- estado/calidad informado por el nodo.

## 2. Tiempo, muestreo y estadística

Con muestras $x_i$:

$$
\bar{x}=\frac{1}{n}\sum_{i=1}^{n}x_i
$$

$$
s=\sqrt{\frac{1}{n-1}\sum_{i=1}^{n}(x_i-\bar{x})^2}
$$

El promedio no representa datos faltantes ni sustituye la serie original. Para muestreo irregular, un promedio simple puede sesgar la interpretación; se conserva timestamp y se define la ventana.

La completitud en un intervalo es:

$$
C=\frac{N_{válidas}}{N_{esperadas}}\times100\%
$$

Se reportan por separado recibidas, válidas, duplicadas, tardías y ausentes.

## 3. Modelo relacional mínimo

Una tabla de mediciones puede contener:

```sql
measurements(
  id INTEGER PRIMARY KEY,
  device_id TEXT NOT NULL,
  seq INTEGER NOT NULL,
  ts_utc TEXT NOT NULL,
  variable TEXT NOT NULL,
  value REAL,
  unit TEXT NOT NULL,
  quality TEXT NOT NULL,
  received_at TEXT NOT NULL,
  UNIQUE(device_id, seq, variable)
)
```

La restricción `UNIQUE` hace visible el duplicado. `NOT NULL`, `CHECK` y claves protegen invariantes, pero no reemplazan la validación de dominio.

## 4. Transacciones y concurrencia

Una transacción agrupa operaciones atómicamente. Se prepara la sentencia, se enlazan parámetros y se confirma solo si todas las operaciones son válidas. No se construye SQL concatenando datos externos.

SQLite permite múltiples lectores y serializa escritura. El modo WAL puede mejorar convivencia entre lectura y escritura, pero requiere comprender archivos auxiliares, checkpoint y almacenamiento. Se usa una conexión o estrategia explícita por hilo/proceso según la biblioteca.

## 5. Ejemplo guiado

1. Llega `seq=1842`, timestamp, `31.4 °C`, calidad `ok`.
2. Parser verifica formato; validador confirma rango y edad.
3. Conversión mantiene valor original y agrega categoría calculada.
4. Inserción parametrizada dentro de transacción.
5. Una repetición de `seq=1842` activa la restricción y aumenta contador de duplicados.
6. Consultas calculan últimos 20 valores y estadísticas de una ventana temporal.
7. El dashboard consume consultas, no toca el puerto serie.

## 6. Procedimiento de laboratorio

1. Definir diccionario de datos y política de calidad.
2. Crear esquema con claves, restricciones e índices justificados.
3. Insertar lote conocido con válidos, inválidos y duplicados.
4. Verificar rollback ante error dentro de una transacción.
5. Ejecutar consultas de últimos, mínimo, máximo, promedio y completitud.
6. Medir crecimiento del archivo y tiempo de consulta.
7. Respaldar/restaurar una copia y documentar retención.

## 7. Diagnóstico

| Síntoma | Causa probable | Corrección |
|---|---|---|
| Valores cero inesperados | error convertido en cero | usar calidad/NULL y rechazo |
| Filas duplicadas | sin clave idempotente | `UNIQUE` por dispositivo/secuencia |
| `database is locked` | transacción larga/concurrencia | acortar escritura y revisar WAL |
| Consultas lentas | filtro sin índice o sin límite | plan de consulta e índice |
| Hora fuera de orden | reloj/zona/formato | UTC, fuente y `received_at` |
| Archivo crece sin límite | retención ausente | política de archivo/agregación |

## 8. Preguntas y trabajo independiente

1. ¿Qué diferencia hay entre dato faltante, cero y dato inválido?
2. ¿Cuál es la clave natural que detecta duplicados?
3. ¿Qué operación debe ser atómica?
4. ¿Qué consulta responderá la pregunta del proyecto?

Entregar diccionario, esquema SQL, dataset de prueba, consultas y evidencia de rollback/duplicado.

## 9. Referencias precisas

- SQLite, “CREATE TABLE”, §§2–3: sintaxis y restricciones `PRIMARY KEY`, `NOT NULL`, `UNIQUE`, `CHECK` y `FOREIGN KEY`. [Documentación oficial](https://www.sqlite.org/lang_createtable.html).
- SQLite, “Transaction”, §§1–2.3: transacciones, lectura y escritura. [Documentación oficial](https://www.sqlite.org/lang_transaction.html).
- SQLite, “Write-Ahead Logging”, §§1–3 y §6: funcionamiento, concurrencia y precauciones. [Documentación oficial](https://www.sqlite.org/wal.html).
- Python, módulo `sqlite3`, §§“Tutorial”, “How to use placeholders” y “Transaction control”. [Biblioteca estándar](https://docs.python.org/3/library/sqlite3.html).

> Consulta: 5 de agosto de 2026. Las consultas y el esquema del ejemplo son elaboración propia.
