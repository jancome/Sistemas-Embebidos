# Marco teórico – Semana 17

# Integración final, verificación, demostración y sustentación técnica

## 1. Propósito

Cerrar el curso integrando los tres cortes en un único sistema embebido distribuido. La entrega final debe demostrar coherencia entre requerimientos, electrónica, PCB, firmware, comunicaciones, Raspberry Pi, almacenamiento, visualización y recuperación ante fallas.

## 2. Resultados de aprendizaje

Al finalizar la semana, el estudiante estará en capacidad de:

- Verificar el cumplimiento de requisitos.
- Ejecutar una demostración técnica reproducible.
- Presentar evidencias de medición y diagnóstico.
- Explicar la arquitectura completa.
- Justificar decisiones electrónicas y de software.
- Analizar limitaciones y riesgos.
- Demostrar recuperación ante fallas.
- Sustentar individualmente su aporte y el sistema global.

## 3. Integración de los tres cortes

```text
CORTE 1 – EasyEDA
Requisitos, electrónica, PCB, Gerber y BOM
        ↓
CORTE 2 – ESP32
Drivers, adquisición, control, comunicaciones y FreeRTOS
        ↓
CORTE 3 – Raspberry Pi 4
Linux, recepción, validación, SQLite, dashboard y servicio
```

La entrega no debe presentar tres trabajos independientes. Debe mostrar cómo cada decisión del primer corte habilita o limita el segundo y cómo el segundo suministra datos y funciones al tercero.

## 4. Trazabilidad de requisitos

Cada requisito debe relacionarse con una evidencia.

| ID | Requisito | Diseño | Prueba | Resultado | Evidencia |
|---|---|---|---|---|---|
| RF-01 | medir cada 5 s | tarea ESP32 | registrar 20 periodos | cumple/no cumple | tabla de tiempos |
| RF-02 | registrar históricos | SQLite | consultar 100 datos | cumple/no cumple | captura y consulta |
| RNF-01 | recuperarse tras reinicio | servicio | reiniciar Raspberry Pi | cumple/no cumple | log y video |

Un requisito sin prueba no puede considerarse demostrado.

## 5. Verificación y validación

### Verificación

Pregunta si el sistema fue construido conforme al diseño.

Ejemplos:

- ¿el PCB coincide con el esquemático?;
- ¿la trama cumple la especificación?;
- ¿la tabla tiene los campos definidos?;
- ¿el servicio usa las rutas correctas?

### Validación

Pregunta si la solución satisface la necesidad real.

Ejemplos:

- ¿la frecuencia de medición sirve para el proceso?;
- ¿el dashboard permite tomar una decisión?;
- ¿la alarma local funciona cuando se pierde la red?;
- ¿el costo es razonable para el contexto?

## 6. Plan de pruebas final

El plan debe incluir condiciones normales, límites y fallas.

### Pruebas funcionales

- lectura de sensor;
- activación de salida;
- publicación o transmisión;
- almacenamiento;
- visualización;
- comando permitido, si aplica.

### Pruebas eléctricas

- tensiones de alimentación;
- corriente del nodo;
- temperatura de componentes críticos;
- niveles lógicos;
- respuesta de etapa de potencia.

### Pruebas temporales

- periodo de muestreo;
- latencia de control;
- tiempo de comunicación;
- tiempo de recuperación;
- tiempo de arranque.

### Pruebas de falla

- sensor desconectado;
- periférico ausente;
- pérdida de red;
- pérdida de UART;
- broker o servidor detenido;
- Raspberry Pi reiniciada;
- trama inválida;
- base de datos no disponible.

## 7. Evidencia cuantitativa

Una demostración debe incluir mediciones, no solo apreciaciones.

Ejemplos:

- error de medición;
- corriente promedio;
- corriente máxima;
- latencia;
- porcentaje de paquetes válidos;
- número de pérdidas;
- tiempo de reconexión;
- uso de almacenamiento;
- tiempo de actividad.

## 8. Demostración reproducible

La demostración debe tener una secuencia clara:

1. presentar necesidad y arquitectura;
2. mostrar placa y conexiones;
3. encender con fuente segura;
4. verificar alimentación;
5. mostrar adquisición local;
6. activar salida;
7. mostrar comunicación;
8. consultar base de datos;
9. abrir dashboard;
10. provocar una falla;
11. observar detección;
12. recuperar operación;
13. mostrar logs;
14. cerrar con resultados y limitaciones.

## 9. Estado seguro

El sistema debe definir qué ocurre durante:

- arranque;
- reinicio;
- pérdida de sensor;
- pérdida de comunicación;
- error de configuración;
- apagado.

Una salida no debe activarse accidentalmente porque un GPIO queda flotante o porque el software aún no ha iniciado.

## 10. Documentación electrónica

La entrega debe contener:

- diagrama de bloques;
- esquemático;
- PCB;
- Gerber;
- BOM;
- alimentación y protecciones;
- interfaces;
- pinout;
- mediciones;
- cambios frente al Preproyecto 1.

## 11. Documentación del ESP32

- arquitectura por capas;
- drivers;
- tareas;
- periodos y prioridades;
- colas o sincronización;
- protocolo;
- estados de error;
- recuperación;
- cambios frente al Preproyecto 2.

## 12. Documentación de Raspberry Pi

- instalación y red;
- aplicación Python;
- recepción;
- validación;
- esquema SQLite;
- consultas;
- dashboard;
- servicio;
- logs;
- pruebas de reinicio.

## 13. Sustentación individual

Cada integrante debe poder explicar:

- problema y requisitos;
- un bloque electrónico;
- una sección del firmware;
- el protocolo de comunicación;
- una consulta o módulo de Raspberry Pi;
- una falla y su diagnóstico;
- una decisión que cambiaría en una nueva versión.

El reparto de tareas no exime del conocimiento integral.

## 14. Análisis de riesgos

El informe debe reconocer riesgos residuales:

- precisión insuficiente;
- ruido;
- dependencia de red;
- desgaste de microSD;
- falta de aislamiento;
- disponibilidad de componentes;
- seguridad de credenciales;
- escalabilidad;
- límites térmicos.

No se espera un producto industrial certificado, pero sí conciencia de los pasos faltantes.

## 15. Costos y viabilidad

Actualizar la BOM final con:

- componentes realmente usados;
- PCB;
- Raspberry Pi y accesorios;
- fuente;
- carcasa;
- repuestos;
- costos de envío;
- costo total;
- costo por unidad para una cantidad definida.

La viabilidad no depende solo del precio; incluye disponibilidad, mantenimiento y confiabilidad.

## 16. Ejemplo de prueba de recuperación

### Condición

Desconectar el enlace entre ESP32 y Raspberry Pi durante 20 segundos.

### Resultado esperado

- ESP32 continúa adquisición y control local.
- Raspberry Pi marca enlace desconectado después del timeout.
- Dashboard muestra dato antiguo.
- Log registra la pérdida.
- Al reconectar, se valida la primera trama.
- El estado vuelve a normal.
- Se registra el tiempo de recuperación.

### Evidencia

- video;
- timestamps de log;
- tabla de tiempos;
- captura del dashboard;
- secuencia antes y después.

## 17. Diagnóstico final

Cuando una prueba falla, el grupo debe evitar modificar varios bloques al mismo tiempo. Orden:

1. reproducir;
2. definir síntoma;
3. localizar bloque;
4. medir entrada y salida;
5. revisar logs;
6. comparar con especificación;
7. aplicar una corrección;
8. repetir prueba;
9. registrar resultado.

## 18. Errores comunes

- Preparar una demostración sin plan B.
- Depender de internet externo.
- No llevar copias del código.
- Mostrar solo el dashboard y ocultar el hardware.
- No medir alimentación.
- No demostrar fallas.
- Confundir video editado con prueba técnica.
- No conocer el código propio.
- Presentar requisitos diferentes a los evaluados.
- Ignorar limitaciones.

## 19. Lista de cierre

- [ ] Requisitos trazados.
- [ ] PCB y BOM finales.
- [ ] Firmware compilable.
- [ ] Dependencias documentadas.
- [ ] Base de datos funcional.
- [ ] Dashboard operativo.
- [ ] Servicio habilitado.
- [ ] Logs disponibles.
- [ ] Pruebas de falla ejecutadas.
- [ ] Informe revisado.
- [ ] Video disponible.
- [ ] Copias de respaldo.
- [ ] Sustentación ensayada.

## 20. Referencias de apoyo

- `PROYECTO_FINAL.md`.
- `EVALUACION.md`.
- `plantillas/README.md`.
- Marcos teóricos de las semanas 1 a 16.
- Documentación oficial de EasyEDA, ESP32, Raspberry Pi, Python, SQLite y FreeRTOS.
