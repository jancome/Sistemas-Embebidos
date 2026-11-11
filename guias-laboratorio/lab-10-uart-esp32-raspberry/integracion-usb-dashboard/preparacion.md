# Preparar Raspberry antes de conectar el sensor

Esta página es para quien todavía no ve el escritorio de Raspberry. Si ya lo controlas con Connect y puedes abrir su terminal, continúa con la [guía de la práctica](README.md#1-descargar-los-archivos).

## Qué necesitas tener disponible

- Raspberry Pi, fuente adecuada para su modelo, microSD y lector de tarjetas para el computador.
- Raspberry Pi OS con escritorio.
- Una red a la que pueda conectarse Raspberry.
- Mac o PC con navegador para utilizar Connect.
- Arduino IDE en el computador para programar el ESP32.

La Raspberry es un computador independiente. El Mac no se convierte en su monitor al unirlos con un cable USB. Connect permite manejar el escritorio por red.

## Si la microSD todavía no tiene sistema

1. Instala [Raspberry Pi Imager](https://www.raspberrypi.com/software/) en el Mac o PC.
2. Conecta la microSD mediante el lector.
3. En Imager, selecciona tu modelo y **Raspberry Pi OS de 64 bits con escritorio**. La variante Lite no incluye el escritorio que utilizamos en esta práctica.
4. Selecciona la microSD como destino. La escritura borra su contenido: comprueba que sea la tarjeta elegida.
5. En la personalización, guarda el nombre del equipo, usuario, contraseña, zona horaria y datos exactos de Wi-Fi. Configura el país correspondiente a la red.
6. Activa SSH si necesitas hacer el primer acceso sin monitor. Puedes habilitar Connect si Imager ofrece esa opción; se puede activar también después.
7. Escribe la imagen y espera a que termine la verificación. Si falla, revisa tarjeta y lector antes de utilizarla.
8. Expulsa la tarjeta desde el computador, colócala en Raspberry y conecta su fuente.

Como ejemplo de nombres para un grupo:

| Dato | Ejemplo | Para qué se usa |
|---|---|---|
| Nombre del equipo | raspberry-g01 | Localizar esa Raspberry en la red |
| Usuario de Linux | estudiante | Entrar a su sistema y guardar sus archivos |
| Cuenta Raspberry Pi ID | Cuenta utilizada en Connect | Vincular el equipo con el acceso remoto |

Son datos distintos. Si tu equipo ya se llama RaspberryJC y el usuario es jancome, conserva esos valores: no hay que reinstalar ni cambiar el nombre para hacer el laboratorio.

## Primer acceso

**Con pantalla:** conecta un monitor o TV a un puerto micro-HDMI de Raspberry, además de teclado y ratón. La Raspberry Pi 5 utiliza micro-HDMI; no mini-HDMI. Completa las opciones iniciales y confirma que puedes abrir el navegador.

**Sin pantalla, usando SSH:** el computador y Raspberry deben tener conectividad entre sí en la red. Abre la terminal del Mac o PC y usa los nombres que configuraste. Para el ejemplo anterior:

~~~bash
ssh estudiante@raspberry-g01.local
~~~

La primera conexión puede pedir confirmar la identidad del equipo. Después solicita la contraseña del usuario. Al escribirla no aparecen puntos ni asteriscos: es normal.

Si no encuentra el nombre, confirma que Raspberry arrancó y que tiene guardada la red correcta. También puede utilizarse su dirección IP, si la conoces. Un nombre terminado en .local depende del descubrimiento de equipos en esa red; algunas redes lo limitan.

Antes de probar repetidamente Connect, hace falta comprobar que Raspberry está realmente conectada. Si no puedes acceder por red, utiliza una pantalla para revisar la configuración o corrige los datos de red de la instalación.

## Activar y vincular Connect

Desde la terminal de Raspberry, abierta localmente o por SSH, ejecuta cada comando en una línea:

~~~bash
rpi-connect on
rpi-connect signin
~~~

El segundo muestra una dirección de vinculación. Ábrela en el navegador del computador e inicia sesión con la cuenta Raspberry Pi ID que usarás para ese equipo.

Después visita [Raspberry Pi Connect](https://connect.raspberrypi.com), busca tu dispositivo y abre **Screen sharing / Compartir pantalla**. Abrir solo la consola remota no muestra el escritorio.

Para revisar el estado:

~~~bash
rpi-connect status
rpi-connect doctor
~~~

La cuenta de Connect y la contraseña del usuario Linux cumplen funciones diferentes. Si el dispositivo ya está vinculado, normalmente basta con volver al sitio de Connect cuando Raspberry esté encendida y conectada; no se inicia la vinculación de nuevo en cada uso.

Para compartir pantalla se necesita una sesión gráfica Wayland iniciada. Si el equipo arranca solo en consola o no inicia sesión en el escritorio, revisa la opción de arranque e inicio automático en la configuración de Raspberry. También puede abrirse con:

~~~bash
sudo raspi-config
~~~

Busca las opciones del sistema para arrancar en escritorio e iniciar la sesión del usuario automáticamente. Reinicia después de guardar, cuando no haya una instalación o actualización en curso.

Si aparece command not found al usar rpi-connect, verifica que instalaste Raspberry Pi OS con escritorio y consulta la [instalación oficial de Connect](https://www.raspberrypi.com/documentation/services/connect.html). Si SSH no está habilitado y tampoco hay sesión de escritorio, primero necesitas recuperar uno de esos accesos.

## Antes de volver a la guía

Comprueba estas acciones:

1. Puedes entrar a Connect y ver el escritorio de Raspberry.
2. Dentro de ese escritorio, el navegador abre GitHub.
3. El icono de terminal abre una ventana donde puedes escribir:

   ~~~bash
   whoami
   hostname
   ~~~

whoami muestra el usuario de esa sesión; hostname muestra el nombre del equipo. En el equipo del docente pueden aparecer jancome y RaspberryJC. Si tu grupo tiene otros nombres, la ruta ~/monitor_esp32 seguirá apuntando a la carpeta personal correcta.

Si todavía hay actualizaciones pendientes, finalízalas antes de la práctica. No cierres la alimentación mientras se está modificando el sistema.

Ya puedes [descargar los archivos y preparar el sensor](README.md#1-descargar-los-archivos).

## Referencias

- [Preparación de Raspberry Pi](https://www.raspberrypi.com/documentation/computers/getting-started.html).
- [Raspberry Pi Connect: instalación, vinculación y requisitos](https://www.raspberrypi.com/documentation/services/connect.html).
