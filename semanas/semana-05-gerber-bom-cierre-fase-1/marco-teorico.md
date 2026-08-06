# Marco teórico – Semana 05

# Archivos de fabricación, BOM, cotización y cierre de la Fase 1

## 1. Propósito

Cerrar el primer corte convirtiendo el diseño de EasyEDA en un paquete técnico que pueda ser revisado, cotizado, fabricado y ensamblado por una persona distinta al diseñador. La calidad del proyecto no se demuestra solo con una vista 3D; se demuestra mediante documentación coherente y verificable.

## 2. Resultados de aprendizaje

Al finalizar la semana, el estudiante estará en capacidad de:

- Generar y revisar archivos Gerber y de perforación.
- Identificar las capas necesarias para fabricación.
- Elaborar una lista de materiales —BOM— trazable.
- Definir alternativas de componentes críticos.
- Preparar cotización de PCB, componentes y ensamble.
- Ejecutar una revisión previa a fabricación.
- Sustentar la arquitectura y decisiones del Preproyecto ABP 1.

## 3. Qué es un paquete de fabricación

El fabricante de PCB no recibe el archivo conceptual del proyecto como única evidencia. Requiere archivos que describan geometría de cobre, máscara, serigrafía, contorno y perforaciones.

Un paquete habitual incluye:

- cobre superior;
- cobre inferior;
- máscara de soldadura superior e inferior;
- serigrafía superior e inferior, cuando aplique;
- contorno de placa;
- archivo de taladros;
- archivos internos para placas multicapa;
- documento de especificaciones de fabricación.

Los nombres exactos dependen de la herramienta y el fabricante.

## 4. Archivos Gerber

Gerber es un formato utilizado para describir capas de una PCB. Cada capa debe revisarse por separado y en conjunto.

Aspectos por comprobar:

- contorno cerrado;
- orientación;
- dimensiones;
- pads y vías;
- aperturas de máscara;
- referencias de serigrafía;
- ausencia de textos sobre pads;
- pistas completas;
- zonas de cobre;
- perforaciones presentes;
- coincidencia entre capas.

La generación sin errores no garantiza que el archivo represente la intención del diseño. Debe abrirse en un visor Gerber independiente.

## 5. Archivo de perforación

El archivo de taladros contiene posiciones y diámetros para:

- pines through-hole;
- vías;
- agujeros de montaje;
- ranuras, cuando el proceso lo permite.

Se debe confirmar que los agujeros mecánicos y eléctricos estén incluidos y que sus diámetros sean compatibles con los componentes.

## 6. Revisión previa a fabricación

La revisión debe hacerse en tres niveles.

### Revisión eléctrica

- alimentación correcta;
- tierra común o aislamiento definido;
- protecciones presentes;
- entradas no flotantes;
- señales de programación disponibles;
- niveles lógicos compatibles.

### Revisión física

- huellas correctas;
- orientación de componentes;
- acceso a conectores;
- espacio para tornillos y carcasa;
- zona de antena libre;
- altura de componentes;
- disipación y ventilación.

### Revisión de fabricación

- DRC sin errores no justificados;
- contorno cerrado;
- anchos y separaciones compatibles;
- taladros válidos;
- serigrafía legible;
- Gerber verificado.

## 7. Lista de materiales —BOM—

La BOM relaciona cada referencia del esquemático con un componente real.

Campos recomendados:

| Campo | Descripción |
|---|---|
| Designador | R1, C3, U2, J1 |
| Cantidad | Número de unidades |
| Descripción | Función y valor |
| Parte del fabricante | Código exacto |
| Footprint | Encapsulado usado |
| Tolerancia | Cuando aplique |
| Tensión/potencia | Límite relevante |
| Proveedor | Fuente de compra |
| Costo | Valor unitario |
| Alternativa | Reemplazo validado |

Una BOM con “resistencia”, “sensor” o “regulador” sin número de parte no es suficiente para fabricar.

## 8. Sustitución de componentes

Una alternativa no se valida solo porque tenga el mismo nombre comercial. Debe comprobarse:

- pinout;
- encapsulado;
- tensión;
- corriente;
- tolerancia;
- velocidad;
- temperatura;
- disponibilidad;
- compatibilidad de firmware.

Los componentes críticos deben tener al menos una alternativa cuando sea posible.

## 9. Cotización

El costo total puede incluir:

```text
Costo total = PCB + componentes + envío + ensamble + impuestos + contingencia
```

También deben considerarse:

- cantidad mínima;
- repuestos;
- herramientas especiales;
- conectores y cables;
- fuente de alimentación;
- carcasa;
- tiempo de entrega.

El precio unitario cambia con la cantidad. Una placa económica puede resultar costosa si requiere componentes difíciles de conseguir.

## 10. Diseño para ensamble y prueba

Una placa debe facilitar su montaje y diagnóstico.

Buenas prácticas:

- referencias visibles;
- polaridades indicadas;
- pin 1 identificado;
- conectores nombrados;
- puntos de prueba;
- componentes orientados de forma coherente;
- espacio para soldadura;
- acceso al puerto de programación;
- indicador de alimentación;
- posibilidad de aislar bloques.

## 11. Ejemplo guiado de revisión

Para una placa base con ESP32, sensor y salida MOSFET:

1. abrir el Gerber en visor;
2. comprobar contorno y dimensiones;
3. confirmar zona de antena sin cobre;
4. verificar pads de conectores;
5. confirmar taladros de montaje;
6. revisar que las pistas de potencia sean suficientes;
7. comparar designadores de BOM con PCB;
8. verificar parte exacta del regulador;
9. confirmar polaridad de diodo y capacitor;
10. revisar puntos de prueba;
11. calcular costo total;
12. documentar riesgos antes de fabricar.

## 12. Preproyecto ABP 1

La entrega debe demostrar la trazabilidad completa:

```text
problema
→ requisitos
→ arquitectura
→ selección de componentes
→ alimentación y protección
→ esquemático
→ PCB
→ DRC
→ Gerber
→ BOM
→ cotización
→ plan de prueba
```

Cada integrante debe explicar el sistema completo, aunque tenga un rol específico.

## 13. Pruebas previstas antes del ensamble

El equipo debe definir cómo verificará la placa cuando llegue:

1. inspección visual;
2. continuidad entre alimentación y tierra;
3. prueba de cortocircuito;
4. encendido con fuente limitada en corriente;
5. verificación de reguladores;
6. programación del ESP32;
7. prueba de sensor;
8. prueba de salida sin carga;
9. prueba con carga;
10. registro de mediciones.

## 14. Diagnóstico de fallas de documentación

Fallas frecuentes:

- componente de BOM que no coincide con footprint;
- conector invertido;
- ausencia de archivo de taladros;
- contorno abierto;
- referencia de serigrafía sobre pad;
- número de parte descontinuado;
- regulador sin margen térmico;
- costo incompleto;
- diseño sin punto de programación.

La corrección debe registrarse como una revisión del diseño, no como un cambio informal.

## 15. Errores comunes

- Enviar Gerber sin abrirlo en un visor.
- Confiar únicamente en la vista 3D.
- Exportar BOM sin completar números de parte.
- No incluir costos de envío o repuestos.
- Usar componentes de biblioteca que no existen comercialmente.
- Fabricar antes de revisar una impresión 1:1.
- No guardar una versión congelada de la entrega.
- Modificar el diseño después de generar Gerber sin regenerar archivos.

## 16. Trabajo independiente

- Completar el paquete de fabricación.
- Congelar una versión identificada.
- Presentar Gerber, BOM y cotización.
- Preparar la sustentación del Preproyecto 1.
- Registrar observaciones para el firmware del Corte 2.
- Definir qué interfaces de hardware deben validarse primero con ESP32.

## 17. Referencias de apoyo

- EasyEDA Std User Guide: generación y revisión de Gerber, exportación de BOM y proceso de PCB.
- Reglas del fabricante seleccionado.
- Datasheets y dibujos mecánicos.
- `EVALUACION.md`, `ABP_PROYECTO_DE_CURSO.md` y `PROYECTO_FINAL.md`.
