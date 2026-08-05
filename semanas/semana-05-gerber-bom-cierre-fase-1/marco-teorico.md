# Marco teórico – Semana 05

## Documentación de fabricación, BOM y revisión de diseño

### Propósito formativo

Cerrar el Corte 1 significa congelar una versión reproducible del diseño. Un fabricante necesita geometría y taladros; compras necesita referencias inequívocas; ensamblaje necesita orientación; y el evaluador necesita trazabilidad desde requisitos hasta pruebas. Ninguna de estas necesidades se resuelve con una captura de pantalla del PCB.

## 1. Paquete de fabricación

Gerber describe capas gráficas y Excellon describe taladros. Para una PCB de dos capas se esperan, como mínimo:

- cobre superior e inferior;
- máscara de soldadura superior e inferior;
- serigrafía necesaria;
- contorno de placa cerrado;
- archivo de taladros metalizados/no metalizados según el servicio;
- notas de fabricación cuando una propiedad no quede codificada.

El archivo comprimido se inspecciona en un visor Gerber independiente. Se revisan capas, escala, contorno, taladros, aperturas de máscara, textos, polaridades y ausencia de objetos fuera de la placa.

## 2. Lista de materiales como especificación

Cada renglón de la BOM debe relacionar designador, cantidad, descripción, valor, tolerancia, encapsulado y número de parte del fabricante. Para partes críticas se añade proveedor y alternativa aprobada.

Una alternativa no es “cualquier resistencia de 10 kΩ”: debe conservar resistencia, tolerancia, potencia, coeficiente térmico, tensión y encapsulado que afecten el requisito. En reguladores, sensores, conectores y protecciones, la equivalencia se verifica parámetro por parámetro.

El costo de una unidad prototipo puede estimarse como:

$$
C_u=\frac{C_{PCB}+C_{envio}+C_{herramental}}{N}+\sum_j q_j C_j+C_{ensamble}
$$

La cotización debe indicar moneda, fecha, cantidad, impuestos y supuestos; de lo contrario no es comparable.

## 3. Versionado y línea base

Una línea base vincula:

- versión de esquemático y PCB;
- revisión de BOM;
- paquete Gerber generado desde esa revisión;
- lista de observaciones cerradas y abiertas;
- requisitos que cubre el diseño;
- commit o identificador de entrega.

Si se cambia un componente o una red después de generar Gerber, el paquete anterior deja de representar el diseño y debe regenerarse.

## 4. Revisión por etapas

- **ERC:** coherencia eléctrica configurada en el esquemático.
- **DRC:** cumplimiento geométrico de reglas del PCB.
- **DFM:** capacidad de fabricar según límites del proveedor.
- **DFA:** facilidad y corrección del ensamblaje.
- **Revisión funcional:** cumplimiento de requisitos, interfaces, potencia y pruebas.

Estas revisiones son complementarias. DFM no descubre un pin invertido si la geometría es fabricable.

## 5. Ejemplo guiado de liberación

1. Congelar `Rev A` de esquemático y PCB.
2. Ejecutar ERC/DRC y adjuntar reportes con excepciones justificadas.
3. Exportar BOM y resolver filas sin MPN o footprint.
4. Exportar Gerber/taladros y abrirlos en visor independiente.
5. Comparar cantidades BOM–PCB y verificar designadores extremos.
6. Revisar con lista: alimentación, polaridad, pin 1, conectores, antena, test points, contorno y textos.
7. Calcular costo para 1, 5 y 10 unidades.
8. Registrar riesgos aceptados antes de presentar el Preproyecto 1.

## 6. Prueba de escritorio antes de ordenar

El grupo realiza una “prueba sin placa”:

- seguir desde cada pin de conector hasta su destino;
- simular continuidad esperada y cortos prohibidos;
- comprobar tensión y corriente nominal de cada componente;
- imprimir el PCB a escala 1:1 y superponer componentes disponibles;
- verificar acceso físico a conectores, botones y programación;
- trazar cada requisito de hardware a una red o componente.

## 7. Diagnóstico documental

| Problema | Evidencia | Riesgo | Acción |
|---|---|---|---|
| BOM con “10k” sin MPN | compra ambigua | parte incompatible | completar especificación |
| Gerber sin contorno | visor no muestra borde cerrado | rechazo de fábrica | corregir capa de outline |
| Taladro desplazado | visor independiente no coincide | PCB inutilizable | revisar formato/unidades |
| BOM y PCB con cantidades distintas | designadores faltantes | ensamblaje incompleto | reconciliar exportación |
| Cambio posterior sin nueva revisión | fechas/commits no coinciden | pérdida de trazabilidad | regenerar paquete y versión |

## 8. Preguntas orientadoras

1. ¿Podría un tercero fabricar la placa sin hacer preguntas?
2. ¿Qué componentes no admiten sustitución y por qué?
3. ¿Qué error funcional no detecta el visor Gerber?
4. ¿Qué evidencia demuestra que el paquete corresponde a la última PCB?
5. ¿Qué riesgo se acepta para el prototipo y cómo se probará?

## 9. Trabajo independiente y entrega ABP

- Preparar carpeta de liberación con nomenclatura consistente.
- Completar matriz requisito–bloque–componente–prueba.
- Ensayar una sustentación de ocho minutos basada en decisiones y evidencia.
- Registrar retroalimentación como tareas para el firmware del Corte 2.

## 10. Referencias precisas

- EasyEDA, *Std User Guide*, “Generate Fabrication File (Gerber)”, secciones “Gerber file name” y “Gerber View”. [Guía oficial](https://docs.easyeda.com/en/PCB/Gerber-Generate/).
- EasyEDA, *Std User Guide*, “Export BOM” y “PCB Layout” (flujo de salida de fabricación). [Guía oficial](https://docs.easyeda.com/en/Introduction/PCB-Layout/).
- Espressif Systems, *ESP32 Hardware Design Guidelines*, Release master, §1.3 “Schematic Checklist”, pp. 4–18; §1.4.11 “Typical Layout Problems and Solutions”, p. 31; §1.5 “Download Guidelines”, pp. 31–32. [PDF oficial](https://documentation.espressif.com/esp-hardware-design-guidelines/en/latest/esp32/esp-hardware-design-guidelines-en-master-esp32.pdf).
- NASA, *Systems Engineering Handbook*, Rev. 2, cap. 5 “Product Realization”, §§5.3–5.4 sobre verificación y validación. [Edición oficial](https://www.nasa.gov/reference/systems-engineering-handbook/).

> Consulta de documentación web: 5 de agosto de 2026. El paquete real debe cotejarse además con las capacidades del fabricante seleccionado.
