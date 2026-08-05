# Marco teórico – Semana 12

## Raspberry Pi 4, computadores de placa única y fundamentos de Linux

### Propósito formativo

La Raspberry Pi no sustituye al ESP32: extiende el sistema con recursos de cómputo, archivos, procesos, red y aplicaciones de alto nivel. La arquitectura debe conservar control temporal y estado seguro en el microcontrolador, y ubicar en el SBC las funciones que se benefician de un sistema operativo.

## 1. MCU frente a SBC

| Criterio | ESP32 como MCU/SoC | Raspberry Pi 4 como SBC |
|---|---|---|
| Arranque | firmware directo, corto | firmware de arranque + kernel + servicios |
| Temporización | control fino/RTOS | planificador general, latencia variable |
| Memoria | limitada, sin memoria virtual general | RAM amplia y memoria virtual |
| Almacenamiento | flash embebida | microSD/USB y sistema de archivos |
| Operación | función dedicada | múltiples procesos/usuarios |
| Falla típica | watchdog/reset del nodo | proceso, servicio, OS o almacenamiento |

Una tarea se asigna al ESP32 si exige respuesta local predecible, bajo consumo o supervivencia sin red. Se asigna a Raspberry Pi si requiere base de datos, interfaz web, librerías complejas, archivos o administración remota.

## 2. Capas del sistema Linux

```text
aplicación Python / dashboard
servicios y bibliotecas de usuario
llamadas al sistema
kernel Linux: procesos, memoria, red, drivers, archivos
hardware Raspberry Pi 4
```

El kernel arbitra CPU, memoria y dispositivos. El espacio de usuario ejecuta procesos aislados con identidades y permisos. Una aplicación no debe ejecutarse como `root` solo para evitar comprender permisos.

## 3. Archivos, procesos y permisos

En Linux, configuración, dispositivos y estado se exponen mediante jerarquías de archivos. Conceptos mínimos:

- ruta absoluta y relativa;
- usuario, grupo y permisos de lectura/escritura/ejecución;
- proceso, PID, estado y código de salida;
- entrada/salida estándar;
- paquete, repositorio y actualización;
- sistema de archivos persistente frente a memoria temporal.

Los permisos `rwx` se asignan a propietario, grupo y otros. El principio de mínimo privilegio concede solo lo requerido por GPIO, puerto serie, base de datos y red.

## 4. Recursos y capacidad

La utilización se observa, no se adivina. Para una aplicación:

$$
U_{CPU}=\frac{t_{CPU}}{t_{pared}}\times100\%
$$

La tasa de crecimiento del almacenamiento es:

$$
S_{día}=N_{registros/día}\cdot B_{registro}\cdot F_{overhead}
$$

Con muestreo cada segundo hay 86 400 registros/día. La política de retención debe definirse antes de llenar la tarjeta.

## 5. Ejemplo guiado de partición

Para un sistema de ventilación:

- ESP32: mide, filtra, controla ventilador y entra en estado seguro si el sensor falla.
- Raspberry Pi: recibe datos, valida, agrega, almacena, visualiza y notifica.
- Si Linux reinicia, el control continúa y el ESP32 marca muestras pendientes o pérdida.
- Al volver el servicio, se negocia continuidad usando secuencia y timestamp.

La Raspberry Pi no genera PWM crítico de seguridad desde un proceso Python sujeto a pausas del sistema operativo.

## 6. Instalación y verificación inicial

1. Crear imagen de Raspberry Pi OS con Imager y usuario no predeterminado.
2. Configurar zona horaria, hostname y acceso remoto seguro.
3. Arrancar con fuente adecuada y comprobar voltaje/temperatura.
4. Actualizar índices y paquetes según política del laboratorio.
5. Registrar versión de OS, kernel, arquitectura y espacio.
6. Crear usuario/grupo y carpeta del proyecto con permisos mínimos.
7. Verificar hora, red y reinicio limpio.

## 7. Diagnóstico

| Síntoma | Nivel probable | Comprobación |
|---|---|---|
| No arranca | fuente, imagen o microSD | LED, tensión e imagen verificada |
| Se reinicia bajo carga | potencia/temperatura | logs, undervoltage y temperatura |
| Aplicación “desaparece” | proceso no supervisado | PID, código de salida y journal |
| Archivo no se puede escribir | permisos/ruta/disco | propietario, montaje y espacio |
| Hora incorrecta | red/NTP/zona | estado de sincronización |
| GPIO/serial inaccesible | grupo/permisos | grupos del usuario y dispositivo |

## 8. Preguntas y trabajo independiente

1. ¿Qué función no puede esperar al arranque de Linux?
2. ¿Qué proceso necesita privilegios y por qué?
3. ¿Cuánto almacenamiento consume un mes de datos?
4. ¿Qué evidencia permite reconstruir un reinicio?

Entregar cuadro MCU–SBC aplicado, inventario de sistema, estimación de almacenamiento y distribución definitiva de responsabilidades.

## 9. Referencias precisas

- Raspberry Pi Ltd., *Raspberry Pi 4 Model B Datasheet*, Release 1.1, §2 “Features”, p. 6; §4 “Electrical Specification”, pp. 7–8; §5 “Peripherals”, pp. 9–11. [PDF oficial](https://datasheets.raspberrypi.com/rpi4/raspberry-pi-4-datasheet.pdf).
- Raspberry Pi, “Getting started” y “Install an operating system”, apartados de Raspberry Pi Imager y personalización del sistema. [Documentación oficial](https://www.raspberrypi.com/documentation/computers/getting-started.html).
- Linux Foundation, *Filesystem Hierarchy Standard 3.0*, §§3–5 sobre jerarquía raíz, `/usr` y `/var`. [Especificación](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html).
- Lee y Seshia, *Introduction to Embedded Systems*, 2.ª ed., caps. 8–12 para arquitecturas de cómputo, entrada/salida y concurrencia. [UC Berkeley](https://ptolemy.berkeley.edu/books/leeseshia/).

> Consulta: 5 de agosto de 2026. Los comandos concretos pueden cambiar entre versiones; el concepto y la evidencia permanecen.
