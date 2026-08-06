# Marco teórico – Semana 15

# Recepción, validación, procesamiento y almacenamiento con SQLite

## 1. Propósito

Convertir las tramas recibidas del ESP32 en datos confiables, trazables y consultables. La Raspberry Pi no debe almacenar cualquier cadena recibida sin verificarla. Primero se valida el mensaje, después se transforma en un registro con unidad, estado, secuencia y tiempo.

## 2. Resultados de aprendizaje

Al finalizar la semana, el estudiante estará en capacidad de:

- Diferenciar dato crudo, dato validado e información procesada.
- Aplicar validaciones de estructura, tipo, rango y secuencia.
- Diseñar un esquema de base de datos para telemetría.
- Crear, insertar y consultar registros en SQLite.
- Utilizar consultas parametrizadas.
- Gestionar timestamps y calidad de datos.
- Calcular resúmenes básicos sin perder trazabilidad.
- Manejar interrupciones de recepción y errores de almacenamiento.

## 3. Cadena de datos

```text
Trama recibida
      ↓
Delimitación
      ↓
Validación de integridad
      ↓
Conversión de tipos
      ↓
Validación física
      ↓
Procesamiento
      ↓
Almacenamiento
      ↓
Consulta y visualización
```

Cada etapa puede rechazar o marcar un dato. El sistema debe registrar por qué.

## 4. Validación estructural

Antes de convertir valores se verifica:

- longitud máxima;
- terminador correcto;
- cantidad de campos;
- versión de protocolo;
- identificador de nodo;
- checksum o CRC;
- presencia de campos obligatorios.

Una trama mal formada no debe llegar a la base como medición válida.

## 5. Conversión y validación de tipo

Los campos de texto deben convertirse de manera controlada:

```python
try:
    sequence = int(fields[2])
    value = float(fields[3])
except ValueError:
    # registrar dato inválido
```

La conversión exitosa no demuestra que el valor sea físicamente razonable.

## 6. Validación de rango

Ejemplo:

```text
Temperatura permitida del proceso: -10 °C a 100 °C
```

Un valor de `999.9` puede ser numéricamente válido pero físicamente inválido. Debe marcarse como error de sensor, trama o conversión.

## 7. Calidad del dato

Se recomienda asociar un estado:

- `ok`;
- `out_of_range`;
- `checksum_error`;
- `timeout`;
- `sensor_fault`;
- `duplicate`;
- `stale`.

Esto permite distinguir ausencia de datos de una medición real igual a cero.

## 8. Timestamps

Se pueden manejar varios tiempos:

- tiempo de adquisición en ESP32;
- tiempo de recepción en Raspberry Pi;
- tiempo de inserción en la base.

Si el ESP32 no tiene reloj absoluto, puede enviar tiempo desde arranque y secuencia. La Raspberry Pi añade tiempo UTC o local al recibir.

Se recomienda almacenar tiempo en formato consistente y convertir para visualización.

## 9. Secuencia

La secuencia permite detectar pérdidas y duplicados.

```text
última secuencia = 107
nueva secuencia = 109
→ falta 108
```

La base puede registrar el salto o generar un evento. Si el nodo reinicia y vuelve a cero, debe diferenciarse de un dato antiguo duplicado.

## 10. SQLite

SQLite es una base de datos relacional embebida almacenada en un archivo. No requiere un servidor separado y resulta adecuada para un computador de borde de alcance local.

Ventajas:

- instalación simple;
- transacciones;
- consultas SQL;
- archivo único;
- integración con Python;
- buena trazabilidad para prototipos.

No debe tratarse como un archivo de texto al que varias tareas escriben sin coordinación.

## 11. Diseño de tabla

Ejemplo:

```sql
CREATE TABLE IF NOT EXISTS measurements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    received_at TEXT NOT NULL,
    node_id TEXT NOT NULL,
    sequence INTEGER NOT NULL,
    variable TEXT NOT NULL,
    value REAL,
    unit TEXT,
    quality TEXT NOT NULL,
    UNIQUE(node_id, sequence, variable)
);
```

La restricción `UNIQUE` puede ayudar a evitar duplicados, pero debe considerarse el reinicio de secuencia.

## 12. Consultas parametrizadas

No se deben construir sentencias concatenando datos recibidos.

Ejemplo en Python:

```python
cursor.execute(
    """
    INSERT INTO measurements
    (received_at, node_id, sequence, variable, value, unit, quality)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    (received_at, node_id, sequence, variable, value, unit, quality),
)
```

Las consultas parametrizadas reducen errores y riesgos de inyección.

## 13. Transacciones

Una transacción agrupa operaciones que deben completarse de forma coherente. Si una operación falla, se puede revertir.

Se debe definir:

- cuándo confirmar;
- cuántos registros agrupar;
- qué hacer ante error;
- cómo recuperar después de reinicio.

## 14. Índices

Los índices aceleran consultas frecuentes, por ejemplo por tiempo o nodo, pero ocupan espacio y aumentan el costo de inserción.

Ejemplo:

```sql
CREATE INDEX IF NOT EXISTS idx_measurements_time
ON measurements(received_at);
```

El índice debe responder a una necesidad de consulta real.

## 15. Consultas básicas

Últimas mediciones:

```sql
SELECT received_at, value, unit
FROM measurements
WHERE node_id = ? AND variable = ?
ORDER BY id DESC
LIMIT 20;
```

Resumen:

```sql
SELECT MIN(value), MAX(value), AVG(value)
FROM measurements
WHERE quality = 'ok';
```

Cantidad de fallas:

```sql
SELECT quality, COUNT(*)
FROM measurements
GROUP BY quality;
```

## 16. Retención de datos

Una base crece con el tiempo. Se debe estimar:

```text
registros por día = frecuencia × 86400
```

Ejemplo: una medición cada 5 segundos:

```text
86400 / 5 = 17280 registros por día
```

El proyecto debe decidir:

- cuánto tiempo conservar datos crudos;
- si agrega promedios;
- cuándo archiva o elimina;
- cómo realiza copia de seguridad.

## 17. Procesamiento

El procesamiento puede incluir:

- conversión de unidades;
- filtrado de valores imposibles;
- cálculo de promedio móvil;
- detección de umbral;
- cálculo de energía o consumo;
- detección de tendencia;
- resumen por intervalo.

El dato original debe conservarse cuando sea necesario para auditoría.

## 18. Ejemplo guiado

La Raspberry Pi recibe:

```text
V1,NODO02,0157,temperatura,32.6,C,OK,5B
```

Proceso:

1. verificar longitud y terminador;
2. validar checksum;
3. comprobar ocho campos;
4. convertir secuencia y valor;
5. validar `NODO02`;
6. comprobar temperatura entre -10 y 100 °C;
7. añadir tiempo de recepción;
8. insertar con `quality='ok'`;
9. actualizar resumen;
10. registrar cualquier error sin detener el receptor.

## 19. Actividad práctica

Cada grupo debe:

1. definir esquema;
2. crear base y tabla;
3. recibir al menos 50 tramas;
4. insertar datos válidos;
5. registrar tramas inválidas;
6. detectar un duplicado;
7. detectar una secuencia perdida;
8. consultar últimos datos;
9. calcular mínimo, máximo y promedio;
10. reiniciar la aplicación y verificar persistencia.

## 20. Conexión con el ABP

La base debe responder a preguntas del proyecto:

- ¿qué ocurrió?;
- ¿cuándo?;
- ¿qué nodo lo reportó?;
- ¿el dato fue válido?;
- ¿existen pérdidas?;
- ¿cómo evolucionó la variable?;
- ¿hubo recuperación después de una falla?

## 21. Diagnóstico de fallas

Si no se insertan datos:

1. revisar ruta y permisos;
2. comprobar tabla;
3. registrar excepción;
4. validar tipos;
5. comprobar restricciones;
6. confirmar `commit`;
7. probar una inserción manual;
8. revisar espacio disponible.

Si aparecen duplicados:

- revisar secuencia;
- usar clave única adecuada;
- identificar reintentos;
- comprobar reinicios;
- diferenciar mensajes repetidos de mediciones nuevas.

## 22. Errores comunes

- Guardar datos sin validar.
- Usar cero para representar error.
- Mezclar unidades.
- No registrar tiempo.
- Concatenar SQL con datos recibidos.
- Abrir múltiples conexiones sin control.
- No confirmar transacciones.
- No definir retención.
- Eliminar datos crudos después de calcular un promedio sin justificarlo.
- No realizar copia de seguridad.

## 23. Trabajo independiente

- Completar módulo `storage.py`.
- Crear consultas para dashboard.
- Estimar crecimiento mensual.
- Añadir tabla de eventos o fallas.
- Preparar visualización y servicio de la Semana 16.

## 24. Referencias de apoyo

- SQLite Documentation y SQL Language Documentation.
- Python `sqlite3` Documentation.
- `guias-laboratorio/lab-11-sqlite-dashboard-servicio/README.md`.
- `PROYECTO_FINAL.md`.
