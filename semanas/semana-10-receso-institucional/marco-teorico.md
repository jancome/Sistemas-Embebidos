# Marco teórico – Semana 10

# Consolidación autónoma de la Fase 2 durante el receso institucional

## 1. Propósito

La Semana 10 corresponde al receso institucional y no introduce contenido nuevo. Este documento organiza el repaso autónomo para que cada grupo cierre vacíos antes de integrar FreeRTOS y presentar el Preproyecto ABP 2.

## 2. Resultados esperados

Al finalizar el repaso, el estudiante debe poder:

- Explicar la arquitectura de firmware del proyecto.
- Identificar el driver desarrollado y su relación con el datasheet.
- Interpretar una transacción SPI.
- Diferenciar Wi-Fi, Bluetooth Clásico y BLE.
- Explicar el protocolo HTTP o MQTT seleccionado.
- Mostrar cómo el sistema responde ante una desconexión.
- Preparar una distribución inicial de tareas para FreeRTOS.

## 3. Mapa de integración del segundo corte

```text
Hardware diseñado en EasyEDA
        ↓
HAL de ESP32
        ↓
Drivers
        ↓
Servicios de adquisición y actuación
        ↓
SPI / periféricos
        ↓
Wi-Fi / Bluetooth / BLE
        ↓
HTTP o MQTT
        ↓
Aplicación del proyecto
```

Cada bloque debe tener una prueba independiente y una interfaz definida.

## 4. Lista de verificación del firmware

### Organización

- El proyecto compila sin advertencias críticas.
- Los pines y parámetros están centralizados.
- Los drivers están separados de la aplicación.
- Las unidades están documentadas.
- Los errores no se representan como mediciones válidas.

### Driver

- Existe función de inicialización.
- Se verifica identidad o respuesta.
- Se manejan timeout y desconexión.
- La conversión de datos está documentada.
- El código se relaciona con el datasheet.

### Comunicación

- La conexión no bloquea la adquisición.
- Hay estados de conexión.
- Se registra la causa de falla.
- Existe reintento con espera.
- El payload tiene identificador, secuencia y unidad.

## 5. Revisión de tiempos

Cada función debe tener un tiempo máximo esperado.

Ejemplos:

| Operación | Periodo | Tiempo máximo | Acción si excede |
|---|---:|---:|---|
| Lectura de sensor | 1 s | 50 ms | marcar inválida |
| Publicación | 30 s | 3 s | almacenar y reintentar |
| Actualización de salida | 100 ms | 10 ms | registrar falla |

Esta tabla prepara la transición hacia tareas concurrentes.

## 6. Datos compartidos

Antes de usar FreeRTOS se debe identificar qué información comparten los módulos:

- última medición;
- estado de alarma;
- estado de conexión;
- contador de fallas;
- comandos recibidos;
- buffer de mensajes.

Para cada dato se define:

- quién lo produce;
- quién lo consume;
- con qué frecuencia;
- qué ocurre si se pierde;
- si requiere cola, mutex, notificación o copia local.

## 7. Ejercicio de arquitectura

Transformar el flujo secuencial:

```text
leer sensor
→ controlar carga
→ conectar Wi-Fi
→ publicar
→ esperar
```

En una propuesta concurrente:

```text
Tarea de adquisición → cola → tarea de control
                         └──→ tarea de comunicación
```

La propuesta debe justificar periodos, prioridades y mecanismo de intercambio.

## 8. Pruebas de consolidación

Cada grupo debe ejecutar:

1. arranque normal;
2. sensor desconectado;
3. periférico SPI ausente;
4. red no disponible;
5. servidor o broker detenido;
6. recuperación del enlace;
7. medición fuera de rango;
8. operación local sin comunicación.

Para cada prueba se registra síntoma, causa, evidencia y corrección.

## 9. Conexión con el ABP

La Fase 2 debe demostrar que el nodo ESP32 puede:

- adquirir una variable;
- validar la medición;
- controlar una salida;
- comunicarse;
- reconocer fallas;
- continuar operando localmente;
- recuperarse sin intervención innecesaria.

## 10. Errores comunes detectables durante el repaso

- Dependencia excesiva de `delay()`.
- Código duplicado.
- Uso de variables globales sin protección.
- Reconexión dentro de un ciclo infinito.
- Driver acoplado directamente al dashboard.
- Mensajes sin identificación.
- Ausencia de estados de error.
- Pruebas realizadas solo con condiciones ideales.

## 11. Trabajo autónomo sugerido

- Corregir observaciones de las semanas 6 a 9.
- Dibujar la arquitectura de tareas.
- Completar la bitácora.
- Organizar capturas y mediciones.
- Preparar preguntas sobre concurrencia.
- Ensayar la sustentación técnica del Preproyecto 2.

## 12. Referencias de apoyo

- Marcos teóricos de las semanas 6, 7, 8 y 9.
- Documentación oficial de ESP32 y FreeRTOS.
- `EVALUACION.md` y `evaluaciones/preproyectos/README.md`.
