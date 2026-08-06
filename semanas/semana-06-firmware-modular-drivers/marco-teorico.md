# Marco teórico – Semana 06

# Firmware modular, arquitectura por capas y drivers en ESP32

## 1. Propósito

Iniciar el segundo corte trasladando la arquitectura electrónica a una arquitectura de software mantenible. El firmware no debe concentrarse en un único archivo con funciones largas y retardos bloqueantes. Cada periférico y servicio debe tener responsabilidades, interfaces y pruebas definidas.

## 2. Resultados de aprendizaje

Al finalizar la semana, el estudiante estará en capacidad de:

- Organizar un proyecto C/C++ por módulos.
- Diferenciar aplicación, servicio, driver y abstracción de hardware.
- Interpretar un datasheet para implementar inicialización y lectura.
- Definir interfaces públicas mediante archivos de cabecera.
- Manejar estados y códigos de error.
- Diseñar pruebas mínimas para un driver.
- Separar configuración, credenciales y lógica de aplicación.

## 3. Firmware y software de propósito general

El firmware se ejecuta estrechamente ligado al hardware. Debe considerar:

- tiempos de respuesta;
- memoria limitada;
- periféricos;
- interrupciones;
- estados de energía;
- fallas físicas;
- reinicios;
- comunicación con otros dispositivos.

Por eso, una función que “funciona” en una demostración puede ser inadecuada para operación continua si bloquea tareas, ignora errores o depende de un orden accidental.

## 4. Arquitectura por capas

Una organización recomendada es:

```text
Aplicación
   ↓
Servicios
   ↓
Drivers
   ↓
HAL / periféricos del ESP32
   ↓
Hardware físico
```

### Aplicación

Implementa la lógica del proyecto: decisiones, estados generales y reglas de operación.

### Servicios

Coordinan funciones reutilizables, por ejemplo:

- adquisición periódica;
- gestión de alarmas;
- publicación de datos;
- almacenamiento temporal;
- configuración.

### Driver

Encapsula el acceso a un sensor, actuador o integrado. Debe conocer registros, comandos, tiempos y errores del dispositivo.

### HAL

Proporciona acceso a GPIO, ADC, SPI, I2C, UART u otros recursos de bajo nivel.

## 5. Archivos de cabecera y de implementación

Un módulo C/C++ suele separar:

```text
sensor.h    → interfaz pública
sensor.cpp  → implementación
```

La cabecera declara tipos, constantes y funciones necesarias para otros módulos. La implementación contiene detalles internos.

Ejemplo conceptual:

```cpp
enum class SensorStatus {
    Ok,
    NotInitialized,
    Timeout,
    InvalidData
};

SensorStatus sensorInit();
SensorStatus sensorRead(float& value);
```

La interfaz evita que el resto del programa dependa de registros o pines internos.

## 6. Estado y ciclo de vida

Un driver debe definir su ciclo:

1. creación o configuración;
2. inicialización;
3. verificación de identidad;
4. operación normal;
5. detección de error;
6. recuperación o reinicio;
7. desactivación, si aplica.

No debe asumirse que el sensor siempre responde correctamente después del encendido.

## 7. Lectura de datasheets

Para implementar un driver se identifican:

- tensión y límites eléctricos;
- dirección o chip select;
- registros;
- secuencia de inicialización;
- formato de datos;
- orden de bytes;
- tiempos mínimos;
- estados de ocupado;
- códigos de identificación;
- condición de reset;
- errores posibles.

El estudiante debe poder señalar qué sección del datasheet justifica cada valor del código.

## 8. Tipos, unidades y escalamiento

Los datos crudos deben diferenciarse de la variable física.

```text
cuentas ADC → voltaje → variable calibrada
registro de 16 bits → escala → °C
```

Se recomienda nombrar variables con claridad:

- `rawCounts`;
- `voltageV`;
- `temperatureC`;
- `sampleTimestampMs`.

Evitar números mágicos sin explicación:

```cpp
const float SensorScale = 0.0625f;
```

## 9. Manejo de errores

Un driver no debe devolver un valor aparentemente válido cuando ocurrió una falla. Alternativas:

- código de estado;
- valor y bandera de validez;
- estructura de resultado;
- excepción, solo cuando la plataforma y el diseño lo justifican.

Ejemplo conceptual:

```cpp
struct Measurement {
    float value;
    bool valid;
    uint32_t timestampMs;
};
```

## 10. Bloqueos y retardos

El uso indiscriminado de `delay()` detiene la ejecución de la tarea actual y dificulta la concurrencia. Para tareas periódicas se recomienda usar tiempo transcurrido o mecanismos de RTOS.

Una máquina de estados permite esperar sin bloquear:

```text
IDLE → START_MEASUREMENT → WAIT → READ → VALIDATE → IDLE
```

## 11. Configuración

Los pines, periodos, umbrales y direcciones deben concentrarse en archivos o estructuras de configuración.

No deben publicarse:

- contraseñas Wi-Fi;
- tokens;
- claves privadas;
- datos personales.

## 12. Ejemplo guiado

### Sensor de temperatura hipotético

El datasheet indica:

- dirección I2C fija;
- registro de identificación;
- registro de configuración;
- dos bytes de temperatura;
- escala de 0,01 °C por cuenta.

El driver debe:

1. iniciar el bus;
2. leer identificación;
3. escribir configuración;
4. solicitar dos bytes;
5. unirlos en una palabra;
6. aplicar escala;
7. validar rango;
8. devolver estado.

El servicio de adquisición llama al driver cada periodo; la aplicación decide si activa una alarma.

## 13. Estructura sugerida del proyecto

```text
src/
  main.cpp
  app/
    app_controller.cpp
  services/
    acquisition_service.cpp
  drivers/
    temperature_sensor.cpp
  hal/
    board_pins.cpp
include/
  app/
  services/
  drivers/
config/
  project_config.h
```

La estructura puede simplificarse, pero debe reflejar responsabilidades.

## 14. Actividad práctica

Cada grupo debe:

1. crear el árbol del proyecto;
2. definir módulos;
3. seleccionar un periférico;
4. consultar el datasheet;
5. implementar `init` y una operación principal;
6. manejar al menos dos errores;
7. probar con datos válidos;
8. provocar una falla;
9. registrar resultados.

## 15. Conexión con el ABP

El firmware debe corresponder a los bloques diseñados en EasyEDA. Para cada interfaz física debe existir:

```text
conector/pin → HAL → driver → servicio → función del proyecto
```

Esta trazabilidad evita software desconectado del diseño electrónico.

## 16. Diagnóstico de fallas

Si un driver no responde:

1. comprobar alimentación;
2. verificar pinout;
3. probar el bus con un ejemplo mínimo;
4. leer identificación;
5. observar señales con analizador lógico;
6. confirmar frecuencia y modo;
7. revisar orden de bytes;
8. verificar tiempos;
9. aislar la aplicación y probar solo el driver.

## 17. Errores comunes

- Colocar todo en `setup()` y `loop()`.
- Copiar una librería sin entender el protocolo.
- Mezclar lectura del sensor con decisiones de negocio.
- Devolver cero cuando hay error.
- Usar variables globales sin control.
- Dejar valores y pines dispersos.
- No documentar unidades.
- Bloquear el programa mientras espera un periférico.
- No probar la desconexión del sensor.

## 18. Trabajo independiente

- Completar un driver funcional.
- Documentar funciones públicas.
- Relacionar cada registro con el datasheet.
- Añadir prueba de error.
- Preparar el periférico SPI de la Semana 07.

## 19. Referencias de apoyo

- Documentación oficial Arduino-ESP32 y ESP-IDF.
- Datasheet del periférico elegido.
- `SYLLABUS.md`, `INSTALACION_SOFTWARE.md` y `ABP_PROYECTO_DE_CURSO.md`.
