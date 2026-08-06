# Marco teórico – Semana 01

# Introducción a los sistemas embebidos y arquitectura distribuida

## 1. Propósito

Esta semana presenta el curso, diagnostica los conocimientos previos y establece la arquitectura general del proyecto ABP. El objetivo no es comenzar por una lista de componentes, sino comprender qué problema se resolverá, qué variable física se observará, qué decisiones debe tomar el sistema y cómo se repartirán las funciones entre la electrónica, el ESP32 y la Raspberry Pi 4.

## 2. Resultados de aprendizaje

Al finalizar la semana, el estudiante estará en capacidad de:

- Diferenciar un sistema embebido de un computador de propósito general.
- Identificar sensor, acondicionamiento, procesamiento, comunicación y actuación.
- Distinguir microcontrolador, SoC y computador de placa única —SBC—.
- Formular una necesidad de ingeniería mediante requisitos verificables.
- Representar una solución mediante diagramas de contexto y de bloques.
- Proponer una distribución inicial de funciones entre EasyEDA, ESP32 y Raspberry Pi 4.

## 3. Qué es un sistema embebido

Un sistema embebido es una combinación de hardware y software diseñada para cumplir una función específica dentro de un equipo o proceso. A diferencia de un computador general, sus recursos, interfaces, tiempos y consumo se seleccionan para una aplicación concreta.

Ejemplos:

- controlador de temperatura;
- sistema de monitoreo de energía;
- registrador de variables ambientales;
- control de acceso;
- nodo de detección de fugas;
- sistema de mantenimiento predictivo.

Un sistema embebido no se define solamente porque tenga un microcontrolador. Debe existir una función claramente delimitada, una interacción con el entorno y criterios que permitan decidir si cumple o no su propósito.

## 4. Cadena funcional

La estructura básica puede representarse así:

```text
Variable física
      ↓
Sensor
      ↓
Acondicionamiento e interfaz eléctrica
      ↓
Procesamiento local
      ↓
Comunicación
      ↓
Procesamiento de alto nivel
      ↓
Actuación, registro o visualización
```

Cada bloque debe responder cuatro preguntas:

1. ¿Qué recibe?
2. ¿Qué entrega?
3. ¿Qué límites eléctricos o temporales tiene?
4. ¿Cómo se comprobará que funciona?

## 5. Microcontrolador y SBC

### Microcontrolador

Integra CPU, memoria y periféricos en un dispositivo orientado al control. En este curso el ESP32 se utilizará para:

- leer sensores;
- generar señales de control;
- ejecutar tareas periódicas;
- manejar interfaces como GPIO, ADC, UART, SPI e I2C;
- mantener operación local aunque la red falle;
- transmitir datos.

### Computador de placa única

La Raspberry Pi 4 ejecuta un sistema operativo completo y se utilizará para:

- administrar archivos y procesos;
- ejecutar aplicaciones Python;
- recibir y procesar datos;
- almacenar históricos;
- mostrar dashboards;
- ejecutar servicios;
- registrar eventos y facilitar administración remota.

La división no debe ser arbitraria. Las tareas críticas de adquisición y control periódico pertenecen normalmente al microcontrolador; el almacenamiento, la visualización y el procesamiento de mayor nivel corresponden al SBC.

## 6. Arquitectura tecnológica del curso

```text
CORTE 1 – EasyEDA
Requerimientos → esquemático → PCB → Gerber → BOM

CORTE 2 – ESP32
Drivers → adquisición → control → comunicaciones → FreeRTOS

CORTE 3 – Raspberry Pi 4
Linux → Python → recepción → base de datos → dashboard → servicio
```

Los cortes no son proyectos separados. Cada uno produce una parte del mismo sistema.

## 7. Requisitos funcionales y no funcionales

### Requisito funcional

Describe una acción del sistema.

Ejemplo:

> El nodo debe medir temperatura cada 5 segundos y almacenar una lectura válida.

### Requisito no funcional

Describe una condición de desempeño, seguridad, costo o robustez.

Ejemplos:

- operar con alimentación de 5 V;
- no exceder determinado consumo;
- recuperarse después de una desconexión;
- almacenar datos durante una semana;
- usar componentes disponibles localmente;
- mantener error de medición dentro de un margen definido.

Un requisito útil debe ser específico y verificable. Expresiones como “debe funcionar bien” o “debe ser rápido” no son suficientes.

## 8. Interfaces y límites

En una arquitectura inicial deben identificarse:

- tensión de alimentación;
- tensión lógica;
- corriente máxima;
- tipo de señal: analógica, digital, pulsos o datos;
- velocidad de actualización;
- protocolo de comunicación;
- condiciones de falla.

El ESP32 y la Raspberry Pi 4 trabajan con lógica de 3,3 V. Por ello, cualquier interfaz debe comprobarse antes de conectar los equipos. La compatibilidad mecánica o el hecho de que dos conectores encajen no demuestra compatibilidad eléctrica.

## 9. Ejemplo guiado

### Problema

Supervisar el nivel de un depósito y registrar eventos de nivel bajo.

### Arquitectura inicial

```text
Nivel de agua
      ↓
Sensor
      ↓
Interfaz eléctrica
      ↓
ESP32
  ├── alarma local
  └── datos
        ↓
Raspberry Pi 4
  ├── base de datos
  ├── dashboard
  └── registro de fallas
```

### Posibles requisitos

- medir cada 10 segundos;
- indicar localmente nivel crítico;
- conservar la alarma aunque se pierda la red;
- registrar fecha y estado;
- permitir consulta desde la red local;
- recuperarse después de reinicio.

### Pruebas futuras

- sensor desconectado;
- pérdida temporal de comunicación;
- reinicio de la Raspberry Pi;
- nivel fuera del rango esperado;
- recuperación automática.

## 10. Actividad práctica

Cada grupo debe construir:

1. declaración del problema;
2. usuario o proceso beneficiado;
3. variable física principal;
4. entrada y salida;
5. diagrama de contexto;
6. diagrama de bloques;
7. cinco requisitos funcionales;
8. cinco requisitos no funcionales;
9. tres fallas previsibles;
10. tres pruebas de aceptación.

## 11. Conexión con el proyecto ABP

El producto de esta semana es la primera versión de la arquitectura. No debe considerarse definitiva. Se revisará a medida que aparezcan restricciones de sensores, alimentación, PCB, firmware y comunicación.

La pregunta central es:

> ¿Qué debe permanecer funcionando localmente en el ESP32 y qué puede delegarse a la Raspberry Pi 4?

## 12. Diagnóstico de fallas desde la arquitectura

Antes de construir, se debe aprender a ubicar una falla por bloques. Si no aparece una medición en el dashboard, las causas posibles incluyen:

- sensor sin alimentación;
- interfaz eléctrica incorrecta;
- driver que no responde;
- dato no publicado;
- pérdida de red;
- aplicación de Raspberry Pi detenida;
- base de datos bloqueada;
- error en la visualización.

Una buena arquitectura permite probar cada bloque por separado.

## 13. Errores comunes

- Empezar el proyecto seleccionando módulos sin requisitos.
- Confundir una idea general con un problema de ingeniería.
- Ubicar todo el procesamiento en la Raspberry Pi y dejar al ESP32 como simple cable.
- Pretender controlar cargas directamente desde GPIO.
- No definir qué ocurre cuando falla la comunicación.
- Usar términos como “inteligente” o “automático” sin describir funciones medibles.
- No diferenciar variable física, señal eléctrica y dato digital.

## 14. Trabajo independiente

- Mejorar la redacción del problema.
- Consultar al menos tres alternativas de sensor.
- Registrar tensiones, corrientes e interfaces preliminares.
- Elaborar una tabla de riesgos.
- Preparar la matriz de requerimientos de la Semana 02.

## 15. Referencias de apoyo

- `SYLLABUS.md` y `ABP_PROYECTO_DE_CURSO.md` del repositorio.
- Espressif Systems, documentación oficial de ESP32.
- Raspberry Pi Ltd., documentación oficial de Raspberry Pi.
- EasyEDA, documentación oficial de captura esquemática y diseño de PCB.
