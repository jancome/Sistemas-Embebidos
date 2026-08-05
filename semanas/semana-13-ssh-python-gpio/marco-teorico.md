# Marco teórico – Semana 13

## Red, SSH y aplicación modular en Python

### Propósito formativo

Administrar un SBC de borde exige identificarlo en red, acceder de forma autenticada y reproducir su entorno de software. Python acelera integración, pero debe estructurarse con las mismas reglas de interfaces, errores y pruebas usadas en el firmware.

## 1. Identidad y alcance de red

Una interfaz posee dirección IP, prefijo, ruta y DNS. El hostname ayuda a identificar el equipo, pero no reemplaza la dirección. En la red local, mDNS puede resolver `hostname.local`; su disponibilidad depende del cliente y la red.

Un diagnóstico sigue capas:

1. enlace físico o asociación Wi-Fi;
2. dirección y ruta;
3. resolución de nombre;
4. puerto y servicio;
5. autenticación;
6. aplicación.

“No entra por SSH” no basta: timeout, conexión rechazada y permiso denegado señalan causas distintas.

## 2. SSH y confianza

SSH cifra la sesión y autentica servidor y usuario. La huella del host debe verificarse la primera vez; aceptar cualquier clave elimina protección frente a suplantación. La autenticación por clave usa un par:

- clave privada: permanece protegida en el cliente;
- clave pública: se instala en `authorized_keys` del servidor.

Buenas prácticas: usuario individual, clave con permisos restrictivos, deshabilitar accesos innecesarios, no exponer el puerto directamente a internet y mantener el sistema actualizado.

## 3. Python como aplicación, no como script único

Una estructura mínima:

```text
app/
  config.py
  acquisition.py
  transport.py
  storage.py
  main.py
tests/
pyproject.toml o requirements.lock
```

`main` orquesta; los módulos encapsulan. La configuración no secreta se separa del código; credenciales se inyectan desde entorno o archivo protegido. Las dependencias se fijan y se instalan en un entorno virtual para reproducibilidad.

## 4. Excepciones, recursos y tiempo

Una excepción se captura donde puede agregarse contexto o recuperarse; capturar `Exception` y continuar silenciosamente oculta defectos. Archivos, sockets y conexiones se cierran con administradores de contexto.

El reloj de pared sirve para timestamps civiles; el reloj monotónico sirve para duraciones y timeouts:

$$
\Delta t=t_{mono,2}-t_{mono,1}
$$

No se calculan timeouts con una hora que NTP puede ajustar.

## 5. Ejemplo guiado

1. Raspberry Pi recibe hostname `edge-grupo03`.
2. Se habilita SSH y se verifica huella desde el equipo del estudiante.
3. Se instala clave pública y se prueba inicio sin compartir la privada.
4. Se crea entorno virtual y aplicación modular.
5. `transport.py` entrega un objeto de dominio; no escribe directamente SQLite.
6. `main.py` registra inicio, configuración no sensible y errores con código de salida.
7. Otro integrante clona/configura el entorno desde la documentación y ejecuta una prueba.

## 6. Procedimiento de laboratorio

1. Registrar hostname, IP, interfaz y ruta.
2. Habilitar SSH mediante configuración oficial.
3. Verificar huella y configurar clave.
4. Probar timeout, usuario incorrecto y clave no autorizada.
5. Crear entorno virtual y archivo de dependencias.
6. Construir módulo que reciba una línea de prueba y la convierta a estructura validada.
7. Ejecutar pruebas desde terminal remota y registrar código de salida.

## 7. Diagnóstico

| Mensaje/síntoma | Interpretación | Acción |
|---|---|---|
| `No route to host` | red/ruta | revisar IP y segmento |
| `Connection timed out` | filtro, IP o servicio inaccesible | puerto y alcance |
| `Connection refused` | host responde, SSH no escucha | habilitar servicio |
| `Permission denied` | autenticación | usuario, clave y permisos |
| Importa en un equipo, no en otro | entorno no reproducible | fijar dependencias |
| Archivo funciona solo desde cierta carpeta | ruta relativa frágil | resolver ruta/configuración |

## 8. Preguntas y trabajo independiente

1. ¿Cómo se verifica que el host remoto es el correcto?
2. ¿Qué secretos nunca deben entrar al repositorio?
3. ¿Qué módulo conoce el protocolo y cuál conoce la base de datos?
4. ¿Cómo reconstruir el entorno en otra Raspberry Pi?

Entregar registro de red sin secretos, evidencia SSH, árbol Python, dependencias fijadas y prueba de error controlado.

## 9. Referencias precisas

- Raspberry Pi, “Remote access”, §§“Find the IP address”, “Access a remote terminal with SSH” y “Configure SSH without a password”. [Documentación oficial](https://www.raspberrypi.com/documentation/computers/remote-access.html).
- OpenSSH, manuales `ssh(1)`, `sshd(8)`, `ssh_config(5)` y `sshd_config(5)`. [Manuales oficiales](https://www.openssh.com/manual.html).
- Python Software Foundation, *The Python Tutorial*, §§4–6 (control, funciones y módulos), §8 (errores/excepciones), §10 (biblioteca estándar) y §12 (entornos virtuales). [Documentación oficial](https://docs.python.org/3/tutorial/).
- Python Packaging Authority, “Installing packages using pip and virtual environments”. [Guía oficial](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/).

> Consulta: 5 de agosto de 2026. Las capturas entregadas deben ocultar claves, contraseñas y datos personales.
