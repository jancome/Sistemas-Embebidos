# Marco teórico – Semana 16

# Dashboard, ejecución como servicio, logs y recuperación ante fallas

## 1. Propósito

Convertir la aplicación de borde en un sistema operable y mantenible. No basta con ejecutar manualmente un script y observar datos durante unos minutos. El proyecto debe iniciar automáticamente, registrar eventos, mostrar estado e históricos y recuperarse ante fallas previsibles.

## 2. Resultados de aprendizaje

Al finalizar la semana, el estudiante estará en capacidad de:

- Diseñar un dashboard basado en información útil.
- Separar adquisición, almacenamiento y presentación.
- Configurar la aplicación como servicio del sistema.
- Generar logs con niveles y contexto.
- Implementar reinicio y reconexión controlados.
- Verificar comportamiento después de reiniciar la Raspberry Pi.
- Definir indicadores de salud del sistema.
- Diseñar pruebas de robustez.

## 3. Dashboard e interfaz

Un dashboard no es una colección de gráficas decorativas. Debe responder preguntas operativas:

- ¿el nodo está conectado?;
- ¿cuándo llegó el último dato válido?;
- ¿cuál es el valor actual?;
- ¿se superó un umbral?;
- ¿cuántos datos se perdieron?;
- ¿existen fallas activas?;
- ¿cómo cambió la variable en el tiempo?;

## 4. Información mínima recomendada

### Estado actual

- nodo;
- conexión;
- última secuencia;
- última medición;
- calidad;
- tiempo desde el último dato;
- estado de alarma.

### Histórico

- gráfica temporal;
- mínimo, máximo y promedio;
- eventos de falla;
- periodos sin comunicación;
- cambios de estado.

### Diagnóstico

- versión de la aplicación;
- tiempo de actividad;
- tamaño de base de datos;
- estado del servicio;
- contador de errores;
- última excepción relevante.

## 5. Separación de responsabilidades

Una arquitectura recomendada:

```text
Receptor
   ↓
Validador
   ↓
SQLite
   ↓
Servicio de consultas
   ↓
Dashboard
```

El dashboard no debe leer directamente el puerto serial y escribir la base dentro de la misma función de presentación. La separación facilita pruebas y recuperación.

## 6. Actualización de interfaz

La interfaz debe distinguir:

- valor actual;
- valor histórico;
- dato antiguo;
- dato inválido;
- ausencia de conexión.

Mostrar el último valor sin indicar su antigüedad puede inducir a una interpretación incorrecta.

## 7. Ejecución como servicio

Un servicio permite que la aplicación:

- inicie al arrancar Linux;
- se ejecute sin sesión interactiva;
- tenga usuario y directorio definidos;
- reinicie ante ciertos errores;
- registre salida;
- pueda consultarse y detenerse.

Con `systemd` se define una unidad de servicio.

Ejemplo conceptual:

```ini
[Unit]
Description=Aplicación de borde del proyecto
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=usuario
WorkingDirectory=/home/usuario/proyecto
ExecStart=/home/usuario/proyecto/.venv/bin/python -m app.main
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Los nombres y rutas deben adaptarse al proyecto.

## 8. Comandos de servicio

```bash
sudo systemctl daemon-reload
sudo systemctl enable nombre.service
sudo systemctl start nombre.service
systemctl status nombre.service
journalctl -u nombre.service
```

El estudiante debe comprender qué hace cada comando y no limitarse a copiarlo.

## 9. Política de reinicio

Reiniciar siempre y sin pausa puede crear un ciclo rápido de fallas.

Debe definirse:

- qué errores justifican reinicio;
- cuánto esperar;
- cuántos intentos realizar;
- cuándo permanecer detenido;
- cómo informar la causa.

Una falla de configuración no suele corregirse reiniciando repetidamente.

## 10. Logging

Niveles frecuentes:

- `DEBUG`: detalle para desarrollo;
- `INFO`: eventos normales importantes;
- `WARNING`: condición anormal recuperable;
- `ERROR`: operación fallida;
- `CRITICAL`: falla grave.

Un registro útil incluye:

- timestamp;
- módulo;
- nivel;
- nodo;
- operación;
- contexto;
- excepción.

Ejemplo:

```text
2026-11-18T14:02:11Z WARNING receiver node=NODO03 event=timeout elapsed_s=10
```

## 11. Rotación de logs

Los archivos de log pueden crecer indefinidamente. Se debe usar:

- `journald`;
- rotación de archivos;
- límites de tamaño;
- retención temporal;
- compresión o eliminación controlada.

## 12. Recuperación de comunicación

Cuando se pierde el ESP32:

1. marcar enlace como desconectado;
2. conservar último valor con estado `stale`;
3. registrar timeout;
4. cerrar o reiniciar la interfaz si es necesario;
5. esperar antes de reintentar;
6. detectar reconexión;
7. validar la primera trama;
8. registrar recuperación.

## 13. Recuperación después de reinicio

La aplicación debe:

- iniciar sin intervención;
- abrir la base existente;
- comprobar tablas;
- iniciar receptor;
- recuperar estado operativo;
- evitar duplicar datos;
- publicar que volvió a estar disponible.

## 14. Monitoreo de salud

Indicadores posibles:

```text
last_valid_message_age_s
received_count
invalid_count
lost_sequence_count
database_error_count
service_uptime_s
```

Estos indicadores permiten verificar robustez de forma cuantitativa.

## 15. Ejemplo guiado

Proyecto de temperatura:

- ESP32 envía cada 5 s.
- Raspberry Pi considera desconexión después de 15 s.
- El dashboard muestra verde si el último dato tiene menos de 10 s, amarillo entre 10 y 15 s y rojo después de 15 s.
- El receptor reintenta abrir el puerto cada 5 s.
- El servicio reinicia solo ante una excepción no controlada.
- Los logs registran desconexión y recuperación.

## 16. Pruebas de robustez

Cada grupo debe ejecutar y documentar:

1. inicio normal;
2. cierre manual del proceso;
3. reinicio automático;
4. reinicio de Raspberry Pi;
5. desconexión del ESP32;
6. reconexión;
7. base de datos temporalmente no disponible;
8. trama inválida;
9. red caída, si aplica;
10. espacio de almacenamiento cercano al límite, mediante simulación segura.

## 17. Actividad práctica

1. construir una vista de estado;
2. consultar históricos de SQLite;
3. mostrar antigüedad del último dato;
4. configurar logging;
5. crear servicio;
6. habilitar inicio automático;
7. reiniciar Raspberry Pi;
8. comprobar servicio;
9. provocar desconexión;
10. verificar recuperación y logs.

## 18. Conexión con el ABP

La entrega debe demostrar que el prototipo puede operar como sistema y no solo como experimento.

Trazabilidad:

```text
falla prevista
→ mecanismo de detección
→ estado visible
→ acción de recuperación
→ evidencia en log
→ prueba de retorno a operación
```

## 19. Diagnóstico de fallas

Si el servicio no inicia:

1. revisar `systemctl status`;
2. consultar `journalctl`;
3. comprobar rutas;
4. verificar usuario y permisos;
5. activar el entorno correcto;
6. ejecutar el comando manualmente;
7. revisar dependencias;
8. comprobar archivo de configuración.

Si el dashboard no muestra datos:

- verificar base;
- ejecutar consulta manual;
- revisar rango temporal;
- comprobar zona horaria;
- confirmar que el receptor inserta;
- revisar excepciones de presentación;
- verificar puerto de la interfaz web.

## 20. Errores comunes

- Ejecutar el servicio como `root` sin necesidad.
- Usar rutas relativas que cambian al iniciar.
- Reiniciar siempre, incluso por configuración inválida.
- No limitar logs.
- Mostrar datos antiguos como actuales.
- Mezclar receptor y dashboard en un único ciclo bloqueante.
- No probar reinicio real.
- Depender de una sesión SSH abierta.
- Ocultar excepciones.
- No registrar recuperación.

## 21. Trabajo independiente

- Completar archivo de servicio.
- Preparar prueba de reinicio.
- Documentar indicadores de salud.
- Revisar logs y retención.
- Preparar demostración final completa.

## 22. Referencias de apoyo

- Raspberry Pi Documentation y documentación de Linux.
- Manual de `systemd`, `systemctl` y `journalctl`.
- Python Logging Documentation.
- `guias-laboratorio/lab-11-sqlite-dashboard-servicio/README.md`.
- `PROYECTO_FINAL.md`.
