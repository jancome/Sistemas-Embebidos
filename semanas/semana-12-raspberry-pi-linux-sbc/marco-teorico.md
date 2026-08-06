# Marco teórico – Semana 12

# Raspberry Pi 4, computador de placa única y fundamentos de Linux

## 1. Propósito

Iniciar el tercer corte comprendiendo la Raspberry Pi 4 como computador de placa única —SBC— y no como un microcontrolador grande. La presencia de un sistema operativo cambia la forma de administrar procesos, memoria, archivos, usuarios, red y recuperación ante fallas.

## 2. Resultados de aprendizaje

Al finalizar la semana, el estudiante estará en capacidad de:

- Diferenciar microcontrolador y SBC.
- Explicar la división de responsabilidades entre ESP32 y Raspberry Pi 4.
- Preparar una microSD con Raspberry Pi OS.
- Configurar usuario, hostname, red y SSH.
- Utilizar comandos básicos de Linux.
- Identificar procesos, servicios, permisos y sistema de archivos.
- Diseñar una arquitectura de computador de borde para el proyecto.

## 3. ESP32 frente a Raspberry Pi 4

| Característica | ESP32 | Raspberry Pi 4 |
|---|---|---|
| Tipo | microcontrolador/SoC embebido | computador de placa única |
| Sistema operativo | firmware o RTOS | Linux completo |
| Arranque | rápido y controlado | proceso de arranque del OS |
| Almacenamiento | flash limitada | microSD/almacenamiento externo |
| Tiempo real | mejor control temporal | no determinista por defecto |
| Consumo | menor | mayor |
| Función principal | adquisición y control | procesamiento, datos e interfaz |

La Raspberry Pi no debe reemplazar al ESP32 en tareas críticas de tiempo real. Si Linux se reinicia, la adquisición local y las protecciones esenciales deben continuar en el microcontrolador.

## 4. Computación de borde

La computación de borde procesa datos cerca de la fuente, antes de enviarlos a servicios externos.

Ventajas:

- menor latencia;
- operación local;
- reducción del tráfico;
- mayor privacidad;
- capacidad de filtrar y resumir datos;
- continuidad durante fallas de internet.

En este curso la Raspberry Pi 4 recibe datos del ESP32, los valida, almacena y visualiza.

## 5. Arquitectura del sistema operativo

Una visión simplificada:

```text
Aplicaciones de usuario
      ↓
Bibliotecas y servicios
      ↓
Kernel Linux
      ↓
Drivers
      ↓
Hardware Raspberry Pi
```

El kernel administra CPU, memoria, dispositivos, procesos y sistema de archivos. Las aplicaciones no controlan directamente todo el hardware; utilizan interfaces del sistema operativo.

## 6. Raspberry Pi OS

Raspberry Pi OS es la distribución oficial basada en Linux. Para una instalación académica se debe definir:

- versión del sistema;
- arquitectura;
- hostname;
- usuario;
- contraseña segura;
- red;
- zona horaria;
- SSH;
- paquetes requeridos.

La preparación puede realizarse con Raspberry Pi Imager. En modo headless se preconfiguran varios de estos parámetros antes del primer arranque.

## 7. Sistema de archivos

Directorios relevantes:

- `/home`: archivos de usuarios;
- `/etc`: configuración;
- `/var`: datos variables y logs;
- `/usr`: programas y bibliotecas;
- `/tmp`: archivos temporales;
- `/dev`: dispositivos;
- `/proc`: información de procesos y kernel;
- `/sys`: interfaces del sistema y hardware.

Los proyectos del estudiante deben residir en una carpeta clara dentro de su usuario, no dispersos entre directorios del sistema.

## 8. Usuarios y permisos

Linux diferencia propietario, grupo y otros usuarios.

Permisos básicos:

- lectura —r—;
- escritura —w—;
- ejecución —x—.

Comandos útiles:

```bash
pwd
ls -la
cd
mkdir
cp
mv
rm
chmod
chown
```

No se recomienda ejecutar toda la aplicación con privilegios de administrador. Deben asignarse permisos específicos.

## 9. Procesos

Un proceso es una instancia de un programa en ejecución.

Comandos útiles:

```bash
ps
htop
kill
systemctl
journalctl
```

El estudiante debe poder responder:

- ¿qué proceso recibe datos?;
- ¿cuánta memoria utiliza?;
- ¿se reinicia automáticamente?;
- ¿dónde registra errores?;

## 10. Administración de paquetes

En sistemas basados en Debian se utilizan herramientas como:

```bash
sudo apt update
sudo apt install nombre-paquete
```

Antes de instalar se debe conocer la función del paquete. No se recomienda copiar comandos de internet con privilegios elevados sin comprenderlos.

## 11. Entornos virtuales de Python

En versiones modernas de Raspberry Pi OS, las dependencias Python del proyecto deben gestionarse mediante un entorno virtual.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install paquete
```

El entorno virtual separa dependencias del sistema y facilita reproducibilidad.

## 12. Red y hostname

La Raspberry Pi debe tener una identidad dentro de la red.

Datos por registrar:

- hostname;
- dirección IP;
- interfaz usada;
- puerta de enlace;
- DNS;
- método de asignación: DHCP o estática;
- puerto de aplicación.

Un hostname descriptivo puede ser:

```text
rpi-g03-borde
```

## 13. Ejemplo guiado de arquitectura

Proyecto de monitoreo:

```text
ESP32
  ├── lectura cada 2 s
  ├── control local
  └── transmisión
        ↓
Raspberry Pi 4
  ├── servicio receptor
  ├── validación
  ├── SQLite
  ├── dashboard
  └── logs
```

La Raspberry Pi puede reiniciarse sin que el control local del ESP32 se detenga. Al volver, recupera la comunicación y continúa almacenando datos.

## 14. Actividad práctica

Cada grupo debe:

1. preparar la microSD;
2. instalar Raspberry Pi OS;
3. configurar usuario y hostname;
4. habilitar red y SSH;
5. iniciar sesión;
6. actualizar el sistema;
7. crear carpeta de proyecto;
8. crear entorno virtual;
9. mostrar información de CPU, memoria y almacenamiento;
10. documentar la arquitectura de borde.

## 15. Conexión con el ABP

El grupo debe definir:

- datos recibidos del ESP32;
- frecuencia;
- protocolo;
- procesamiento local;
- persistencia;
- visualización;
- estrategia de inicio automático;
- comportamiento si la Raspberry Pi falla.

## 16. Diagnóstico de fallas

Si la Raspberry Pi no inicia:

1. revisar fuente;
2. verificar microSD;
3. observar indicadores;
4. comprobar imagen del sistema;
5. probar otra fuente o tarjeta;
6. revisar pantalla o red;
7. consultar logs si inicia parcialmente.

Si no aparece en la red:

- revisar configuración Wi-Fi/Ethernet;
- verificar DHCP;
- comprobar hostname;
- consultar el router;
- conectar monitor temporalmente;
- revisar interfaz con comandos de red.

## 17. Errores comunes

- Apagar retirando energía sin cierre correcto.
- Usar fuente insuficiente.
- Trabajar siempre como `root`.
- Instalar paquetes globalmente sin entorno virtual.
- Mezclar archivos del proyecto con configuración del sistema.
- No guardar credenciales de forma segura.
- Pretender ejecutar control crítico solo en Linux.
- No documentar hostname e IP.
- No realizar copia de seguridad.

## 18. Trabajo independiente

- Completar configuración headless.
- Crear estructura Python.
- Guardar lista de dependencias.
- Definir servicios que necesitará el proyecto.
- Preparar la práctica de SSH, Python y GPIO de la Semana 13.

## 19. Referencias de apoyo

- Raspberry Pi Documentation: Raspberry Pi OS, instalación y configuración.
- Documentación oficial de acceso remoto.
- Python Documentation.
- `SYLLABUS.md`, `INSTALACION_SOFTWARE.md` y `NORMAS_DE_CLASE.md`.
