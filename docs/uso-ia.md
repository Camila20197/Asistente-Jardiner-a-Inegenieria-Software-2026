### [TP1] Requerimentos Funcionales

**Herramienta:** Claude y Deepseek.
**Tarea:** Evaluar y mejorar requerimientos funcionales planteados.
**Resultado:** Al hacer discutir ambas IAs se logró una mejora significativa en la respuesta y en la adecuacion de los RF.
**Modificado/descartado:** Descartamos algunos RF ya que estimamos que estaban fuera del alcance, de acuerdo al tiempo que tenemos.
**Error detectado:** Si, se invento un RF que no existia, RF13.

### [TP1] Diagramas de Contexto y Diagramas de Dominio

**Herramienta:** Claude y Gemini.
**Tarea:** Realizar los diagramas en mermaid desde el bosquejo inicial en papel.
**Resultado:** Diagramas obtenidos tal como los habiamos pedido.
**Modificado/descartado:** Nada.
**Error detectado:** Ninguno.

### [TP1] Casos de Uso e Historias de Usuario

**Herramienta:** Claude y Deepseek.
**Tarea:** Evaluar y mejorar los CU e HU planteadas.
**Resultado:** Al hacer discutir ambas IAs se logró una mejora significativa en la respuesta.
**Modificado/descartado:** Descartamos casos de uso y los etiquetamos como no obligatorios.
**Error detectado:** Si, vinculo CU e HU a un RF que no existia, RF13.

### [TP1] Especificaciones generales en el chequeo general del TP

**Herramienta:** Claude 
**Tarea:** Ser un contrapunto para evaluar lo presentado, teniendo como base el checklist.
**Resultado:** Mejora en la redacción y especificaciones.
**Modificado/descartado:** Lo que no gustaba, no se poía.
**Error detectado:** Si, realizaba mas tarea de la pedida, por ejemplo, aagregacion de RNF.

---

## [TP2]

### Redacción inicial de los escenarios

**Herramienta:** Gemini AI
**Tarea:** identificar atributos de calidad críticos y redactar los escenarios a partir del SRS.
**Resultado:** una primera versión con cinco atributos, un escenario por atributo y sugerencias de escenarios adicionales.
**Modificado/descartado:** se ampliaron los escenarios a tres por atributo y se reescribió la justificación de la selección.
**Error detectado:** la primera versión asumía un uso institucional, con varios técnicos y un administrador operando sobre el mismo stock, e incluía un escenario de Integridad en el que un usuario de "público general" modificaba lotes ajenos. Eso contradice la decisión del TP1 de que el prototipo es de uso personal y que los lotes son privados por usuario. 

### Revisión de consistencia previa a la entrega

**Herramienta:** Claude
**Tarea:** revisar los escenarios contra el SRS y contra la consigna.
**Resultado:** señaló tres problemas.
**Modificado/descartado:** se aceptaron los tres y se corrigieron.
**Error detectado:** los escenarios citaban RNF01 y RNF02 "ya definidos en el SRS", pero el SRS no tiene requerimientos no funcionales: venían de los apuntes iniciales y nunca se pasaron. El escenario 5.1 nombraba "CropCalendar" mientras el SRS habla de Google Calendar. Y la medida de 5.3 ("en menos de unos pocos minutos") no era cuantificable, cuando la consigna pide que la medida verifique o cuantifique la respuesta.