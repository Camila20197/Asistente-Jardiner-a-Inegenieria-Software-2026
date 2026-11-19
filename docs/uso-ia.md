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
## TP2

### [TP2] Parte A — Escenarios de atributo de calidad

El registro está junto a los escenarios, como pide la guía: `docs/requirements/quality-scenarios/quality-scenarios.md`, sección "Registro de uso de IA".

### [TP2] Parte B — Maquetado y evaluación heurística

Un documento por pantalla en `docs/ui/heuristic-review/`, con los prompts, las respuestas de la IA, la decisión del grupo sobre cada hallazgo y los ciclos adicionales.

### [TP2] Revisión del repositorio contra el checklist antes de la entrega

**Herramienta:** Claude
**Tarea:** revisar los entregables del TP2 contra el checklist y las rutas de la guía.
**Resultado:** señaló carpetas con nombres distintos a los de la guía, cuatro decisiones de revisión heurística sin completar, prompts de evaluación faltantes en siete documentos, referencias a requerimientos no funcionales inexistentes en el SRS, y una pantalla sin historia de usuario que la respalde.
**Modificado/descartado:** sobre la pantalla de ficha de especie, la IA presentó dos opciones y la decisión la tomó el grupo: [completar con lo que decidieron].
**Error detectado:** la IA afirmó que el aviso de "pendiente de formalizar" estaba en dos pantallas, la ficha de especie y el alta de especie. Al revisarlo, solo estaba en la ficha: el aviso del alta de especie explica la carga incremental y es correcto.

---

## [TP4]

### [TP4] Arquitectura de partida

**Herramienta:** Claude
**Tarea:** armar el TP4 de la HU-08 (diseño, código en Python, pruebas y documento).
**Resultado:** la primera propuesta partía de un documento de arquitectura que la IA había generado aparte, distinto del TP3 que presentó el grupo.
**Modificado/descartado:** se descartó y se pidió rehacer todo sobre el TP3 presentado.
**Error detectado:** la IA tomó como base un documento que no era la entrega del grupo.

### [TP4] Primera versión: los dos caminos

**Herramienta:** Claude
**Tarea:** implementar la HU-08 completa sobre el TP3, incluido el lado servidor (API de sincronización, Cola y Procesador), con una página que mostrara el recorrido de cada observación por la arquitectura.
**Resultado:** una versión con dos caminos (sin señal, la observación queda en el teléfono; con señal, llega hasta la base central) y una página con un botón que reproducía solo el recorrido completo.
**Modificado/descartado:** se descartó el recorrido automático: la demostración la hacemos en vivo, cargando y guardando cada observación nosotras. Después se descartó también el lado servidor, al alinear el trabajo con el diseño detallado que ya había subido el grupo (siguiente entrada).
**Error detectado:** ninguno; fue una decisión de alcance del grupo.

### [TP4] Alineación con el diseño detallado del grupo

**Herramienta:** Claude
**Tarea:** rehacer desde cero el código, las pruebas y el documento para que siguieran el diseño que el grupo ya había escrito (`docs/desing/diseño-detallado.md`): la HU-08 acotada a la captura sin conexión, EC-01 y EC-04, DA-01, la tabla de entidades y el diagrama de robustez, con sus elementos y sus nombres.
**Resultado:** el documento `docs/design/diseno-detallado.md` conserva la introducción, la ficha, la tabla de coherencia, la tabla de entidades y los elementos y flechas de la robustez del grupo, y lo completa con las secciones del Anexo de la consigna.
**Modificado/descartado:** la IA señaló y se corrigió en el diagrama y el documento del grupo:
* El diagrama no estaba dentro de un bloque ` ```mermaid `, así que GitHub lo mostraba como texto.
* Las formas no eran las que sugiere la Referencia: el actor estaba dibujado como una frontera y las entidades como paralelogramos. Se usaron rectángulo redondeado para «boundary», círculo para «controller» y rectángulo con barras para «entity», con leyenda, y los estereotipos con comillas angulares («») en lugar de `&lt;&lt;control&gt;&gt;`. Se escribió «controller», como en la Referencia y el ejemplo de la consigna.
* La carpeta se llamaba `docs/desing/` y el archivo llevaba eñe; la consigna pide `docs/design/diseno-detallado.md`.
* Errores de tipeo: «dispoibilidad», «esta respaldada», «Repository-» y el título sin espacio después de `#`.
* Las siglas pasaron de una línea corrida a una tabla.
**Error detectado:** tres diferencias del diseño con los TP anteriores, que se documentaron y se corrigieron en esos documentos (sección 2.4 del diseño): el catálogo de relaciones del TP3 no tenía la lectura del catálogo de especies; el modelo de dominio del TP1 no tenía los atributos de la tabla de entidades (`estado_sync`, `version`, `last_modified`); y el «menos de 1 s» de EC-01 no está en la medida del escenario 3.1 del TP2, sino en el recorrido sin conexión del TP3. Se dejó, indicando de dónde sale. También se aclaró por qué `Usuario` figura en la tabla de entidades pero no en la robustez.

### [TP4] Implementación (Parte B)

**Herramienta:** Claude
**Tarea:** programar en Python las clases de las secuencias, la persistencia en memoria y en SQLite, el cifrado y la pantalla con Flask.
**Resultado:** el código de `src/`, que sigue las secuencias A y B del diseño, y una página con el teléfono, el diagrama de robustez con el recorrido en cámara lenta y el archivo cifrado tal como queda en el disco.
**Modificado/descartado:** la clave del cifrado se deriva de la contraseña (PBKDF2) y no se guarda, porque la medida del escenario 4.1 pide que sin las credenciales los datos sean inaccesibles. El repositorio en memoria no cifra, porque no deja nada guardado. No se agregó una interfaz para el cifrado: tiene una sola implementación.
**Error detectado:**
* Al usar la página en el navegador, los archivos de la página daban 404: Flask atendía `/static` con su propia carpeta, que no existe. Se corrigió y se amplió la prueba de arranque (CP-33) para que lo detecte.
* Las pruebas de arranque usaban el reloj de la computadora, porque `crear_app` armaba el controlador con la fecha del sistema; eso viola la regla de no depender del reloj sin controlarlo. Se agregó el reloj como parámetro.
* En el diagrama de la página, un cable pasaba por encima de la etiqueta «Repositorio local» y un globo tapaba «Cifrado local»; se reacomodaron. En pantallas angostas la página se desbordaba de costado; se corrigió.

### [TP4] Diagrama de clases (paso 5)

**Herramienta:** pyreverse (pylint) y Claude
**Tarea:** obtener el diagrama de clases desde el código y contrastarlo con la robustez y las secuencias.
**Resultado:** la salida de pyreverse está en `docs/design/clases-pyreverse.mmd`; el diagrama revisado, en la sección 4.2 del diseño.
**Modificado/descartado:** pyreverse dibujó las interfaces de los repositorios como herencia y no mostró las dependencias que ocurren dentro de los métodos; se corrigió a mano y cada diferencia quedó en la sección 4.3.
**Error detectado:** ninguno en el código.

### [TP4] Pruebas (Parte C)

**Herramienta:** Claude
**Tarea:** diseñar los casos de prueba desde los criterios de aceptación y el código, escribirlos con pytest y medir cobertura y complejidad ciclomática.
**Resultado:** 37 casos de prueba (50 ejecuciones), todos con la red cortada y el reloj fijo, y 100% de cobertura de sentencias y ramas en todo `src/`.
**Modificado/descartado:** como la cobertura dio 100%, se hizo una prueba de mutación manual: 23 defectos metidos de a uno, todos detectados por al menos un caso. Al armar la tabla de complejidad aparecieron caminos que la cobertura de ramas no marca (en una sola línea): se ampliaron CP-22, CP-30 y CP-31 y se agregó CP-32. Al medir la cobertura con el arranque incluido, apareció sin probar `main()`: se agregó CP-37.
**Error detectado:** CP-31 mezclaba dos comportamientos (el rechazo al guardar y la especie inexistente al mostrar); se separó en CP-31 y CP-32.

