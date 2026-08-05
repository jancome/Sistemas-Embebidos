# Marco teórico – Semana 16

## Dashboard, servicios, observabilidad y recuperación

### Propósito formativo

Una demostración manual no equivale a operación robusta. El sistema debe arrancar sin intervención, exponer estado sin alterar la adquisición, registrar causas de falla y recuperarse de interrupciones previstas. El dashboard muestra evidencia; no debe ser el dueño de la lógica crítica.

## 1. Separación de responsabilidades

```text
adquisición → validación → persistencia
                         ↓
                    consultas/API → dashboard
```

El dashboard lee una vista o API; no abre el puerto serie ni decide el estado del actuador. Esta separación permite reiniciar la interfaz sin perder adquisición.

Una visualización mínima muestra:

- valor actual con timestamp y calidad;
- estado de ESP32, enlace, base y servicio;
- histórico con unidad y escala;
- última actualización y datos faltantes;
- alarmas diferenciadas de fallas de comunicación.

## 2. Servicio `systemd`

Una unidad de servicio define descripción, dependencias, usuario, directorio, comando de inicio, política de reinicio y destino de instalación. Principios:

- ejecutar con usuario dedicado y permisos mínimos;
- usar rutas absolutas y entorno explícito;
- no incluir secretos directamente en un repositorio público;
- establecer `Restart` y espera para evitar bucles agresivos;
- declarar dependencia de red solo al nivel realmente requerido;
- emitir salida al journal o a un sistema de logs administrado.

`enabled` significa configurado para iniciar; `active` significa actualmente ejecutándose. Ambos estados deben verificarse.

## 3. Logs y métricas

Un evento útil contiene timestamp, nivel, componente, acción, identificador y contexto no sensible. Niveles típicos: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.

Las métricas responden “cuánto”; los logs explican “qué ocurrió”. Mínimos:

- mensajes recibidos/válidos/rechazados;
- edad de última muestra;
- reconexiones y duración de caída;
- uso de disco;
- reinicios del proceso;
- latencia de inserción/consulta.

## 4. Robustez medible

Disponibilidad observada:

$$
A=\frac{T_{operativo}}{T_{total}}
$$

Tiempo medio de recuperación observado:

$$
MTTR=\frac{\sum t_{recuperación}}{N_{fallas}}
$$

La recuperación debe ser acotada y evitar duplicar datos. Un servicio que reinicia cada segundo sin resolver configuración no está recuperado: está en un bucle de falla.

## 5. Ejemplo guiado de servicio

1. La aplicación inicia, valida configuración y abre base de datos.
2. Si UART no está disponible, registra advertencia y reintenta con backoff sin terminar.
3. Si la configuración es inválida, sale con código no cero para evitar operar incorrectamente.
4. `systemd` reinicia ante fallo transitorio con espera acotada.
5. El dashboard muestra `stale` cuando la última muestra excede el umbral.
6. Tras reinicio del SBC, servicio, recepción, inserción y vista vuelven sin comandos manuales.

## 6. Procedimiento de laboratorio

1. Ejecutar aplicación como usuario no privilegiado.
2. Crear unidad y verificar sintaxis/estado.
3. Habilitarla y reiniciar Raspberry Pi.
4. Comprobar proceso, journal, base y dashboard.
5. Desconectar ESP32, detener red y provocar dato inválido.
6. Medir detección, comportamiento degradado y recuperación.
7. Verificar que no haya duplicados ni secretos en logs.

## 7. Diagnóstico

| Síntoma | Evidencia útil | Causa probable |
|---|---|---|
| Servicio activo sin datos | logs y edad de muestra | dependencia externa caída |
| Reinicios continuos | contador/código de salida | configuración o excepción inmediata |
| Funciona manual, falla como servicio | usuario, ruta, entorno | dependencia implícita del shell |
| Dashboard congela adquisición | perfiles/arquitectura | acoplamiento o consulta bloqueante |
| Disco lleno | uso y rotación | logs/retención sin límite |
| Valor viejo parece actual | timestamp no visible | falta de estado `stale` |

## 8. Preguntas y trabajo independiente

1. ¿Qué indica que el sistema está sano, no solo el proceso vivo?
2. ¿Qué fallas son recuperables y cuáles requieren intervención?
3. ¿Cuánto tarda en detectar y recuperar una desconexión?
4. ¿Qué dato de diagnóstico podría revelar un secreto?

Entregar unidad de servicio, dashboard, logs anotados, métricas y matriz de inyección de fallas con tiempos.

## 9. Referencias precisas

- systemd, `systemd.service(5)`, apartados `[Service]`, `ExecStart=`, `Restart=` y tabla de códigos/causas de reinicio. [Manual oficial](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html).
- systemd, `systemd.unit(5)`, apartados de dependencias, condiciones e instalación; `journalctl(1)` para consulta de eventos. [Manuales oficiales](https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html).
- Python, módulo `logging`, §§“Basic Logging Tutorial”, “Advanced Logging Tutorial” y “LogRecord attributes”. [Documentación oficial](https://docs.python.org/3/howto/logging.html).
- SQLite, “How To Corrupt Your Database Files” y “Database Backup API” para límites de almacenamiento y respaldo. [Documentación oficial](https://www.sqlite.org/howtocorrupt.html).

> Consulta: 5 de agosto de 2026. La unidad concreta se adapta a rutas, usuario y framework del grupo.
