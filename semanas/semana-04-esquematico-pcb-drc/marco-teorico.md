# Marco teórico – Semana 04

## Del esquemático al PCB verificable en EasyEDA

### Propósito formativo

El esquemático expresa conectividad e intención; el PCB materializa geometría, campos electromagnéticos, disipación y fabricación. Un DRC sin errores es necesario, pero no demuestra por sí solo que la placa funcione. La revisión combina reglas automáticas, datasheets y razonamiento físico.

## 1. Esquemático como contrato eléctrico

Un buen esquemático:

- se organiza por flujo funcional y bloques;
- muestra todos los pines de alimentación y tierra;
- usa nombres de red consistentes y conectores con pinout explícito;
- asigna valores, tolerancias, potencia y referencia de componente;
- incluye programación, reset, protección y puntos de prueba;
- distingue conexiones reales de simples cruces gráficos.

El ERC detecta conflictos lógicos configurados en la herramienta; no sabe si el valor de una resistencia es correcto ni si dos señales de 3,3 V y 5 V son compatibles.

## 2. Símbolo, footprint y componente real

El símbolo representa función lógica. El footprint representa pads, taladros, máscara, patio y dimensiones. La correspondencia crítica es:

$$
\text{pin del símbolo}\longleftrightarrow\text{pad del footprint}\longleftrightarrow\text{terminal físico}
$$

La verificación se hace contra el dibujo de encapsulado del fabricante, atendiendo a vista superior/inferior, numeración, paso, diámetro de taladro y orientación de pin 1. Una vista 3D atractiva no valida esta correspondencia.

## 3. Ubicación antes que ruteo

La colocación reduce las conexiones críticas antes de trazar:

1. fijar contorno, conectores y restricciones mecánicas;
2. ubicar protección y potencia cerca de la entrada;
3. mantener desacoplamientos junto a sus pines;
4. respetar zona libre de la antena del módulo ESP32;
5. separar nodos de conmutación de señales analógicas;
6. dejar acceso a programación, prueba y ensamblaje.

La inductancia de un lazo crece con su área; por ello los lazos de alta $di/dt$ deben ser cortos y compactos. Una aproximación de caída resistiva sigue siendo:

$$
\Delta V=I\rho\frac{l}{wt}
$$

donde $w$ y $t$ son ancho y espesor de cobre. El ancho final debe verificarse con reglas de fabricante y criterios térmicos, no solo con la ecuación de resistencia.

## 4. Planos y retornos

Un plano de tierra continuo reduce impedancia de retorno. Las señales rápidas tienden a retornar bajo la pista; si atraviesan una división del plano, el retorno se desvía y aumenta el área del lazo. Los cambios de capa requieren una vía de retorno cercana cuando la referencia también cambia de capa.

Para el módulo ESP32 se respeta la colocación de antena recomendada por Espressif: borde de placa y zona sin cobre, pistas o componentes según el módulo concreto. El diseño se coteja con el hardware design guideline, no con una placa genérica encontrada en internet.

## 5. Reglas de diseño

Las reglas deben reflejar capacidad del fabricante y función eléctrica:

- ancho y separación mínimos;
- diámetro de vía, taladro y anillo anular;
- separación a borde;
- clases de red para potencia y señales;
- máscara de soldadura y serigrafía;
- restricciones diferenciales o de longitud cuando apliquen.

El DRC comprueba geometría contra esas reglas. Si las reglas son incorrectas, un reporte “cero errores” solo demuestra coherencia con una configuración incorrecta.

## 6. Ejemplo guiado de revisión

Para una placa base con ESP32, sensor analógico y relé:

1. se verifica pin–pad del módulo, conector y transistor;
2. se coloca el módulo en el borde con la antena despejada;
3. se agrupan regulador y capacitores por lazo de corriente;
4. el retorno del relé se conduce hacia la entrada de potencia, no bajo el sensor;
5. se dimensiona la pista del relé por corriente y temperatura;
6. se añaden test points de 12 V, 3,3 V, GND, señal y control;
7. otro equipo revisa el diseño sin explicación oral.

## 7. Flujo EasyEDA recomendado

1. Ejecutar Design Manager y Footprint Manager.
2. Corregir ERC y documentar excepciones justificadas.
3. Convertir o actualizar PCB preservando identificadores.
4. Definir contorno cerrado y reglas antes del ruteo.
5. Colocar por bloques y revisar restricciones mecánicas.
6. Rutear primero potencia, reloj, analógico y buses críticos.
7. Añadir plano de tierra y volver a inspeccionar retornos.
8. Ejecutar DRC, revisar 2D/3D y generar lista de riesgos manuales.

## 8. Diagnóstico de fallas de diseño

| Hallazgo | Por qué es peligroso | Corrección |
|---|---|---|
| Footprint sin cotejo | placa imposible de ensamblar | comparar dibujo y medir componente |
| Capacitor lejos del pin | lazo inductivo grande | aproximar capacitor y vía de tierra |
| Antena sobre cobre | pérdida y patrón alterado | aplicar keepout del módulo |
| Pista de potencia estrecha | caída y calentamiento | recalcular y crear clase de red |
| Serigrafía sobre pads | ensamblaje confuso | mover texto y marcar polaridad |
| DRC limpio con reglas por defecto | falsa confianza | cargar capacidades reales del fabricante |

## 9. Preguntas y trabajo independiente

1. ¿Qué corriente retorna por cada región del plano?
2. ¿Qué componente no podría reemplazarse sin cambiar footprint?
3. ¿Dónde pondría las puntas del osciloscopio durante diagnóstico?
4. ¿Qué error puede escapar al ERC y al DRC?

Entregar esquemático y PCB con revisión cruzada, lista de cinco riesgos, reporte ERC/DRC y evidencia de verificación de footprints.

## 10. Referencias precisas

- EasyEDA, *Std User Guide*, “Schematic Capture”, “Convert Schematics to PCB” y “Footprints Verification”. [Guía oficial](https://docs.easyeda.com/en/Schematic/Convert-to-PCB/).
- EasyEDA, *Std User Guide*, “PCB Layout”, “Design Rule Check”, “Board Outline” y “Copper Pour”. [Guía oficial](https://docs.easyeda.com/en/Introduction/PCB-Layout/).
- Espressif Systems, *ESP32 Hardware Design Guidelines*, Release master, §1.4 “PCB Layout Design”, pp. 18–31, en especial §§1.4.1–1.4.2 y §1.4.8. [PDF oficial](https://documentation.espressif.com/esp-hardware-design-guidelines/en/latest/esp32/esp-hardware-design-guidelines-en-master-esp32.pdf).
- Espressif Systems, documento de módulo concreto (por ejemplo ESP32-WROOM): “Peripheral Schematics”, “Recommended PCB Land Pattern” y “Module Placement”. La referencia exacta depende del módulo seleccionado.

> Consulta de la guía EasyEDA: 5 de agosto de 2026. Se deben verificar cambios de interfaz en la documentación vigente.
