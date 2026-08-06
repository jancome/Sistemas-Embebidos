# Marco teórico – Semana 13

# Acceso remoto, Python y GPIO en Raspberry Pi 4

## 1. Propósito

Configurar una forma segura y reproducible de administrar la Raspberry Pi 4, desarrollar aplicaciones en Python y utilizar sus GPIO sin superar los límites eléctricos. La Raspberry Pi debe tratarse como un computador Linux con pines de propósito general, no como una fuente de potencia.

## 2. Resultados de aprendizaje

Al finalizar la semana, el estudiante estará en capacidad de:

- Acceder a la Raspberry Pi mediante SSH.
- Identificar hostname, dirección IP y puerto.
- Organizar una aplicación Python por módulos.
- Crear y activar un entorno virtual.
- Interpretar la numeración BCM y el pinout físico.
- Configurar entradas y salidas digitales.
- Utilizar resistencias pull-up y pull-down.
- Aplicar límites eléctricos y etapas de potencia.
- Registrar errores y estados básicos de la aplicación.

## 3. Acceso SSH

SSH permite administrar la terminal de la Raspberry Pi desde otro computador.

```text
Cliente SSH → red local → servidor SSH de Raspberry Pi
```

Ejemplo conceptual:

```bash
ssh usuario@rpi-g03-borde.local
```

Para que funcione deben cumplirse varias condiciones:

- Raspberry Pi encendida;
- servidor SSH habilitado;
- conectividad de red;
- hostname o IP correctos;
- usuario válido;
- autenticación aceptada;
- puerto accesible.

## 4. Seguridad del acceso remoto

Buenas prácticas:

- cambiar credenciales predeterminadas;
- usar contraseña robusta o claves SSH;
- no exponer el puerto a internet sin necesidad;
- limitar usuarios;
- mantener el sistema actualizado;
- revisar intentos y logs;
- no compartir claves privadas.

## 5. Transferencia de archivos

Herramientas como `scp` o SFTP permiten transferir archivos.

Ejemplo conceptual:

```bash
scp archivo.py usuario@rpi-g03-borde.local:/home/usuario/proyecto/
```

Sin embargo, para proyectos se recomienda utilizar control de versiones o un procedimiento documentado, evitando copias desordenadas con nombres ambiguos.

## 6. Python en el computador de borde

Python se utilizará para:

- recibir tramas;
- validar datos;
- controlar GPIO no críticos;
- almacenar registros;
- generar visualización;
- registrar eventos;
- ejecutar servicios.

La aplicación debe separarse en módulos:

```text
app/
  main.py
  config.py
  receiver.py
  validator.py
  storage.py
  gpio_io.py
  logger_setup.py
```

## 7. Entornos virtuales

La aplicación debe tener un entorno aislado:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install gpiozero pyserial
python -m pip freeze > requirements.txt
```

El archivo `requirements.txt` permite reconstruir las dependencias.

## 8. Manejo de errores en Python

Una aplicación robusta no debe terminar ante cualquier excepción.

Ejemplo conceptual:

```python
try:
    value = read_sensor()
except TimeoutError as exc:
    logger.warning("Timeout: %s", exc)
```

No se recomienda capturar todas las excepciones y ocultarlas. Debe registrarse el contexto suficiente para diagnosticar.

## 9. GPIO de Raspberry Pi

Los pines del conector incluyen:

- alimentación de 3,3 V;
- alimentación de 5 V;
- tierra;
- GPIO;
- interfaces como UART, I2C y SPI.

No todos son GPIO. Conectar una señal en un pin de 5 V por error puede dañar el circuito.

## 10. Numeración física y BCM

### Numeración física

Cuenta la posición en el conector.

### Numeración BCM

Utiliza la identificación del controlador GPIO.

Las bibliotecas pueden adoptar un esquema específico. Se debe documentar cuál se usa y comprobar con el comando `pinout` o la documentación oficial.

## 11. Límites eléctricos

Los GPIO operan con lógica de 3,3 V y no son tolerantes a 5 V.

Reglas:

- no conectar señales de 5 V directamente;
- limitar corriente de LED;
- no alimentar motores, relés o cargas desde GPIO;
- utilizar transistor, MOSFET, driver u optoacoplador;
- verificar tierra común;
- configurar estado seguro al iniciar;
- evitar cortocircuitos entre salida y alimentación.

## 12. Entradas digitales

Una entrada no debe quedar flotante. Se utiliza:

- pull-up;
- pull-down;
- resistencia externa;
- polarización interna, cuando sea apropiada.

Ejemplo con pull-up:

```text
3,3 V
  │
resistencia
  │
GPIO ─── pulsador ─── GND
```

- pulsador abierto: entrada alta;
- pulsador cerrado: entrada baja.

## 13. Salidas digitales

Para un LED:

```text
GPIO → resistencia → LED → GND
```

El valor de resistencia se calcula según tensión, caída del LED y corriente segura:

```text
R = (VGPIO - VLED) / ILED
```

La corriente debe mantenerse dentro de límites conservadores y documentados.

## 14. GPIO Zero

GPIO Zero proporciona abstracciones de alto nivel como LED, Button y OutputDevice.

Ejemplo conceptual:

```python
from gpiozero import LED, Button
from signal import pause

led = LED(17)
button = Button(27, pull_up=True)
button.when_pressed = led.on
button.when_released = led.off
pause()
```

El estudiante debe comprender la conexión eléctrica y no depender únicamente del nombre de la clase.

## 15. Rebote de contactos

Un pulsador puede producir múltiples transiciones rápidas. Puede mitigarse mediante:

- filtrado hardware;
- tiempo de estabilización software;
- parámetros de biblioteca;
- máquina de estados.

El rebote debe observarse y no asumirse.

## 16. Ejemplo guiado

### Requisito

Indicar mediante LED que la aplicación de borde está activa y permitir un pulsador de mantenimiento.

### Diseño

- GPIO 17: LED con resistencia.
- GPIO 27: pulsador a GND con pull-up.
- pulsación: registrar evento y cambiar modo.
- salida segura al iniciar: LED apagado.

### Pruebas

1. ejecutar manualmente;
2. medir nivel lógico;
3. pulsar varias veces;
4. observar rebote;
5. desconectar pulsador;
6. comprobar que la entrada mantiene estado definido;
7. detener programa y revisar estado final.

## 17. Actividad práctica

Cada grupo debe:

1. acceder por SSH;
2. crear entorno virtual;
3. instalar dependencias;
4. identificar pinout;
5. dibujar el circuito;
6. conectar LED y pulsador;
7. programar eventos;
8. registrar timestamps;
9. probar rebote o desconexión;
10. documentar límites eléctricos.

## 18. Conexión con el ABP

El GPIO de Raspberry Pi puede usarse para:

- indicadores de estado del computador de borde;
- pulsador de mantenimiento;
- señal de disponibilidad;
- entrada digital auxiliar;
- control de una etapa externa no crítica.

El control principal y la protección local deben permanecer en ESP32 cuando requieran respuesta determinista.

## 19. Diagnóstico de fallas

Si SSH no conecta:

1. comprobar IP;
2. verificar red;
3. confirmar servicio SSH;
4. probar hostname e IP;
5. revisar usuario;
6. comprobar puerto;
7. observar logs.

Si el GPIO no responde:

1. confirmar numeración;
2. medir tensión;
3. verificar tierra;
4. revisar resistencia y polaridad;
5. comprobar configuración de entrada/salida;
6. probar un script mínimo;
7. revisar permisos y proceso que ocupa el pin.

## 20. Errores comunes

- Confundir número físico con BCM.
- Aplicar 5 V a un GPIO.
- Conectar LED sin resistencia.
- Dejar entradas flotantes.
- Alimentar relés o motores directamente.
- Ejecutar scripts siempre con `sudo`.
- Instalar dependencias fuera del entorno virtual.
- No liberar recursos al terminar.
- Ignorar rebote.
- No registrar errores de red o GPIO.

## 21. Trabajo independiente

- Crear módulo `gpio_io.py`.
- Preparar `requirements.txt`.
- Documentar pinout del proyecto.
- Añadir logs de eventos.
- Preparar la integración ESP32–Raspberry Pi de la Semana 14.

## 22. Referencias de apoyo

- Raspberry Pi Documentation: acceso remoto y hardware GPIO.
- GPIO Zero Documentation.
- Python Documentation.
- `NORMAS_DE_CLASE.md` y `guias-laboratorio/lab-09-raspberry-linux-gpio/README.md`.
