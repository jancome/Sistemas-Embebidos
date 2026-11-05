# Informe breve — Monitoreo de RAM en Raspberry Pi
Fecha de sesión y entrega: **4 de noviembre de 2026**, Colombia. Enviar PDF de 2–4 páginas y archivos de soporte en Teams, antes de terminar la sesión. No publicar credenciales. Completar con mediciones reales; declarar pendientes.

## 1. Identificación y objetivo
Grupo:  
Integrantes (3), rol y aporte individual:  
Objetivo en palabras propias:

## 2. Entorno y método
Modelo de Raspberry / Raspberry Pi OS / Python:  
Acceso utilizado (Connect o local):  
Diagrama de adquisición → cálculo → validación → clasificación → CSV:  
Fuente consultada y significado de MemTotal/MemAvailable:  
Fórmula, derivación en palabras propias y criterio NORMAL/ALERTA/ERROR:  
Umbral elegido y por qué sirve para la prueba (no presentarlo como límite universal de fallo):

## 3. Resultados verificables
| ID | Parámetros y duración | Resultado esperado | Resultado observado | Archivo y fila/hora |
|---|---|---|---|---|
| P1: intervalo 5 s | | | | |
| P2: intervalo 2 s | | | | |
| P3: NORMAL | | | | |
| P4: ALERTA | | | | |
| P5: ERROR y restauración | | | | |

Seleccionar una fila real: total = ___; disponible = ___; porcentaje calculado = ___. Mostrar operación y contrastar con CSV.
Capturas seleccionadas, legibles y sin contraseñas: ___.

## 4. Análisis
- ¿Por qué usar MemAvailable y no MemFree?
- ¿Por qué ERROR no debe registrarse como 0 %?
- ¿Coinciden los estados con el umbral de cada fila?
- ¿Por qué el intervalo real puede superar al configurado?
- ¿Qué datos siguen disponibles al detener/reiniciar el programa?
- ¿Qué falló, cómo se diagnosticó y qué quedó pendiente?

## 5. Relación con ESP32
¿Qué cambiaría en adquisición, formato, timeout y reconexión al recibir por USB serial?
¿Qué partes de validación, procesamiento y registro conservarían?
¿Qué control/protecciones deben continuar si la Raspberry se reinicia?

## 6. Conclusiones y fuentes
Tres conclusiones sustentadas en resultados, no solo descripción del código. Para cada una completar: **observación (archivo/fila/hora) → cálculo o comparación → interpretación → límite**. Usar la [guía de razonamiento](guia_razonamiento_ram.md).

| Observación verificable | Cálculo/comparación | Qué permite concluir | Qué no se probó |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

Cambiar un umbral no demuestra saturación; una ruta inexistente no demuestra daño físico de RAM; restaurar manualmente la ruta no equivale a recuperación automática. Citar documentación y ayuda externa utilizada. Todos deben poder defender la implementación.

## Archivos adjuntos
- monitor_ram.py comentado.
- CSV por prueba (o tramos identificables por hora) en datos/.
- Evidencias en evidencias/.
- Este informe exportado a informe.pdf.

No incluir datos inventados ni la solución del ejemplo de temperatura como si fuera el reto de RAM.
