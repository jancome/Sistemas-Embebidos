# Instalación de software

## Unidad 1 – Diseño de placa base

Instalar o habilitar una herramienta EDA aprobada en el syllabus:

- EasyEDA;
- KiCad;
- Proteus;
- Altium, cuando exista licencia disponible.

La herramienta debe permitir trabajar esquemático, footprints, PCB, DRC, Gerber y BOM.

## Unidad 2 – Firmware y comunicaciones

Instalar:

1. Visual Studio Code u otro IDE compatible con el kit seleccionado.
2. Toolchain del microcontrolador.
3. Controladores USB requeridos.
4. Bibliotecas para SPI, Wi-Fi, Bluetooth/BLE, HTTP/MQTT y RTOS.
5. Monitor serial y herramientas de depuración.

Cuando se utilice ESP32, pueden emplearse ESP-IDF, PlatformIO o Arduino IDE, según el nivel y la práctica definida.

## Unidad 3 – Raspberry Pi 4

1. Instalar Raspberry Pi Imager.
2. Preparar Raspberry Pi OS.
3. Configurar usuario, red y SSH.
4. Verificar comandos y fundamentos de Linux.
5. Instalar el entorno del lenguaje de alto nivel seleccionado; se utilizará Python.
6. Instalar bibliotecas de GPIO, comunicación serial o de red, base de datos y dashboard.
7. Configurar la ejecución automática y el registro de eventos.

## Verificación mínima

- El microcontrolador es detectado y puede ejecutar un programa de prueba.
- El proyecto EDA ejecuta ERC o DRC.
- La comunicación SPI puede observarse o registrarse.
- Wi-Fi y Bluetooth/BLE pueden demostrarse.
- HTTP o MQTT intercambia datos.
- La Raspberry Pi es accesible por SSH.
- El programa de alto nivel puede leer GPIO o recibir datos.
- La base local puede crear, insertar y consultar registros.
