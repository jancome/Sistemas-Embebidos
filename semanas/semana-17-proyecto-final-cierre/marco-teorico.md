# Marco teórico – Semana 17

## Integración, verificación, validación y sustentación final

### Propósito formativo

El cierre no agrega una tecnología nueva. Integra y demuestra, con trazabilidad, que la solución construida satisface la necesidad formulada. La sustentación debe distinguir evidencia de funcionamiento, cumplimiento de requisitos, límites y trabajo futuro.

## 1. Integración por interfaces

Integrar no es conectar todo al final. Cada frontera debe tener un contrato:

- sensor–placa: rango, nivel, alimentación y error;
- placa–ESP32: pin, periférico y protección;
- tareas de firmware: tipo, tasa, cola y timeout;
- ESP32–Raspberry Pi: medio, trama/protocolo, secuencia y recuperación;
- aplicación–SQLite: esquema, transacción y retención;
- base/API–dashboard: consulta, unidad y antigüedad.

La prueba incremental sigue el flujo de energía y datos, conservando una evidencia por frontera.

## 2. Verificación y validación

- **Verificación:** ¿el sistema cumple los requisitos especificados?
- **Validación:** ¿la solución satisface la necesidad real en su contexto?

Una matriz de trazabilidad final contiene:

| ID | Requisito | Método | Condición | Criterio | Resultado | Evidencia |
|---|---|---|---|---|---|---|

Métodos posibles: inspección, análisis, demostración y prueba. “Se vio funcionar” no sustituye un criterio cuantitativo.

## 3. Diseño de casos de prueba

Cada caso incluye precondiciones, versión, instrumentos, pasos, resultado esperado, resultado observado y conclusión. Deben cubrir:

- nominal: cadena completa en condición normal;
- límites: mínimo/máximo de rango y carga;
- transición: arranque, cambio de estado y apagado;
- falla: sensor ausente, enlace perdido, dato inválido y reinicio;
- recuperación: retorno automático sin datos corruptos;
- regresión: funciones anteriores después de un cambio.

La cobertura de requisitos se calcula como:

$$
C_R=\frac{N_{requisitos\ aprobados}}{N_{requisitos\ aplicables}}\times100\%
$$

Se informa también el número de requisitos críticos fallidos; no se oculta detrás del porcentaje.

## 4. Incertidumbre y evidencia

Una medición se acompaña de instrumento, resolución y condiciones. Si se compara contra un límite $L$, el margen es:

$$
M=L-|x_{medido}|
$$

Un margen menor que la incertidumbre no demuestra cumplimiento robusto. Los gráficos deben llevar variable, unidad, escala, periodo y fuente.

## 5. Demostración técnica sugerida

1. Identificar versión de PCB, firmware y aplicación.
2. Encender desde estado sin energía.
3. Mostrar adquisición y actuación local.
4. Rastrear una muestra por enlace, validación, SQLite y dashboard.
5. Desconectar enlace; observar estado degradado sin perder control seguro.
6. Restablecer enlace; medir recuperación y duplicados.
7. Reiniciar Raspberry Pi; comprobar `systemd`, logs y continuidad.
8. Presentar un requisito no alcanzado y la evidencia que lo explica.

## 6. Diagnóstico de integración

| Falla visible | Aislamiento recomendado |
|---|---|
| Actuador no responde | orden → GPIO → driver → etapa de potencia → carga |
| No hay datos en Raspberry Pi | sensor → cola → transporte → enlace → parser |
| Base vacía con datos recibidos | validador → transacción → ruta/permisos |
| Dashboard vacío con base llena | consulta/API → filtro temporal → presentación |
| No recupera tras reinicio | unidad → usuario → entorno → dependencia → logs |

Cambiar varias capas a la vez destruye la evidencia causal. Se fija una versión, se reproduce y se aísla una frontera.

## 7. Preguntas para sustentación

1. ¿Qué requisito guio la decisión más importante?
2. ¿Qué medición refuta una alternativa considerada?
3. ¿Cuál es el modo de falla más crítico y su estado seguro?
4. ¿Qué parte es determinista y cuál depende de Linux/red?
5. ¿Qué limitación permanece y cómo se abordaría?

## 8. Trabajo independiente y cierre

- Congelar versiones y generar paquete reproducible.
- Completar matriz de trazabilidad y anexar datos originales.
- Ensayar demostración nominal y de falla con tiempo limitado.
- Revisar que informe, video y repositorio no contengan credenciales.
- Registrar lecciones aprendidas por electrónica, firmware, red y operación.

## 9. Referencias precisas

- NASA, *Systems Engineering Handbook*, NASA/SP-2016-6105 Rev. 2, cap. 5, §§5.3 “Product Verification” y 5.4 “Product Validation”; cap. 6, §6.4 “Technical Risk Management”. [Edición oficial](https://www.nasa.gov/reference/systems-engineering-handbook/).
- Lee y Seshia, *Introduction to Embedded Systems*, 2.ª ed., cap. 13 “Invariants and Temporal Logic” y cap. 14 “Equivalence and Refinement”. [UC Berkeley](https://ptolemy.berkeley.edu/books/leeseshia/).
- Documentación primaria citada en los marcos de semanas 1–16; la versión aplicada debe coincidir con cada herramienta y componente del proyecto.

> Este marco no sustituye rúbricas ni condiciones de entrega del curso; organiza la evidencia técnica para demostrar su cumplimiento.
