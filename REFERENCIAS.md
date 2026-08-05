# Referencias técnicas principales

Los marcos teóricos semanales priorizan fuentes primarias: manuales del fabricante, estándares, libros técnicos abiertos y documentación oficial. La explicación se adapta al español y al proyecto del curso; no se reproducen figuras ni fragmentos extensos protegidos.

## Criterio de citación del curso

Al tomar un dato de diseño, el estudiante debe registrar:

1. fabricante o entidad responsable;
2. título del documento;
3. versión o fecha;
4. capítulo, sección, tabla o página;
5. URL oficial;
6. fecha de consulta para documentación web viva.

Una página comercial o un tutorial puede ayudar a orientar la búsqueda, pero los límites eléctricos, registros, temporización y condiciones de operación se verifican en el datasheet o manual oficial.

## Fundamentos de sistemas embebidos e ingeniería de sistemas

- Edward A. Lee y Sanjit A. Seshia, *Introduction to Embedded Systems: A Cyber-Physical Systems Approach*, 2.ª ed., versión 2.3, MIT Press, 2017. [Sitio oficial y PDF autorizado](https://ptolemy.berkeley.edu/books/leeseshia/).
- NASA, *Systems Engineering Handbook*, NASA/SP-2016-6105 Rev. 2, especialmente capítulos 4, 5 y 6. [Edición oficial](https://www.nasa.gov/reference/systems-engineering-handbook/).

## Corte 1 – EasyEDA y diseño de hardware

- EasyEDA, *EasyEDA Std User Guide*: “Schematic Capture”, “Convert to PCB”, “PCB Layout”, “Design Rule Check”, “Generate Fabrication File (Gerber)” y “Export BOM”. [Documentación oficial](https://docs.easyeda.com/en/).
- Espressif Systems, *ESP32 Hardware Design Guidelines*, Release master, 21 de julio de 2026: checklist de esquemático, alimentación y layout. [PDF oficial](https://documentation.espressif.com/esp-hardware-design-guidelines/en/latest/esp32/esp-hardware-design-guidelines-en-master-esp32.pdf).
- Espressif Systems, *ESP32 Series Datasheet*, v5.3, 2026: pines, periféricos y características eléctricas/RF. [PDF oficial](https://www.espressif.com/documentation/esp32_datasheet_en.pdf).
- Analog Devices, “Seven Steps to Successful Analog-to-Digital Signal Conversion”. [Artículo técnico](https://www.analog.com/en/resources/technical-articles/seven-steps-to-successful-analog-to-digital-signal-conversion.html).
- Analog Devices, *Electronics I and II*, cap. 20 “Analog to Digital Conversion”. [Texto universitario abierto](https://wiki.analog.com/university/courses/electronics/text/chapter-20).

Para cada sensor, actuador, regulador, protección y módulo se añade el datasheet exacto de la referencia seleccionada.

## Corte 2 – ESP32, protocolos y FreeRTOS

- Espressif Systems, *ESP32 Technical Reference Manual*, v5.8, 2026. [PDF oficial](https://www.espressif.com/sites/default/files/documentation/esp32_technical_reference_manual_en.pdf).
- Espressif Systems, *ESP-IDF Programming Guide*, rama estable para ESP32: periféricos, Wi-Fi, Bluetooth, protocolos, FreeRTOS, memoria y watchdog. [Documentación oficial](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/).
- Espressif Systems, *Arduino-ESP32 Documentation*, cuando el curso use este framework. [Documentación oficial](https://docs.espressif.com/projects/arduino-esp32/en/latest/).
- FreeRTOS, *Mastering the FreeRTOS Real Time Kernel*: tareas, colas, recursos y grupos de eventos. [Libro oficial](https://www.freertos.org/Documentation/RTOS_book.html).
- IETF, RFC 9110, *HTTP Semantics*. [Estándar](https://www.rfc-editor.org/rfc/rfc9110).
- IETF, RFC 8259, *The JavaScript Object Notation (JSON) Data Interchange Format*. [Estándar](https://www.rfc-editor.org/rfc/rfc8259).
- OASIS, *MQTT Version 5.0*, OASIS Standard, 7 de marzo de 2019. [PDF oficial](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.pdf).

## Corte 3 – Raspberry Pi 4, Linux y datos

- Raspberry Pi Ltd., *Raspberry Pi 4 Model B Datasheet*, Release 1.1, marzo de 2024. [PDF oficial](https://datasheets.raspberrypi.com/rpi4/raspberry-pi-4-datasheet.pdf).
- Raspberry Pi, documentación de hardware, Raspberry Pi OS, configuración y acceso remoto. [Documentación oficial](https://www.raspberrypi.com/documentation/).
- OpenSSH, manuales de cliente, servidor y configuración. [Documentación oficial](https://www.openssh.com/manual.html).
- Linux Foundation, *Filesystem Hierarchy Standard 3.0*. [Especificación](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html).
- Python Software Foundation, *Python 3 Documentation*: tutorial, `sqlite3` y `logging`. [Documentación oficial](https://docs.python.org/3/).
- Python Packaging Authority, guías de entornos virtuales y dependencias. [Documentación oficial](https://packaging.python.org/).
- SQLite, documentación de lenguaje, transacciones, WAL, respaldo e integridad. [Documentación oficial](https://www.sqlite.org/docs.html).
- systemd, manuales `systemd.service`, `systemd.unit` y `journalctl`. [Documentación oficial](https://www.freedesktop.org/software/systemd/man/latest/).

## Material previo del curso

El curso reutiliza y adapta materiales desarrollados previamente para EasyEDA, ESP32, Wokwi, Wi-Fi, Bluetooth/BLE, HTTP, MQTT y FreeRTOS. Esos materiales complementan, pero no sustituyen, la lectura de las fuentes primarias ni la medición sobre el prototipo.

## Nota de vigencia

Índice revisado el **5 de agosto de 2026**. La documentación web puede cambiar; antes de diseñar o programar se confirma la versión de hardware, framework, sistema operativo y biblioteca usada por el grupo.
