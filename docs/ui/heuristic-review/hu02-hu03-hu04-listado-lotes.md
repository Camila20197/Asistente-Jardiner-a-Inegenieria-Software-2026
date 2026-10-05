# Evaluación heurística — HU-02 / HU-03 / HU-04 · Listado de lotes por especie

Archivo maquetado: `docs/ui/mockups/pantalla-hu02-hu03-hu04-listado-lotes.html`

## Ciclo 1 — Generación del maquetado

**Prompt utilizado:** generar el maquetado HTML de la pantalla que lista los lotes de semillas de una especie (HU-02 alta, HU-03 modificación/baja, HU-04 alerta de stock crítico — RF01, RF02, RF03), para el perfil "Usuario/jardinero-a", mobile-first, Bootstrap 5, paleta y tipografía del grupo, botones de acción de 48×48 mínimo ubicados para uso con una mano. Debe mostrar los lotes existentes con su cantidad, año y procedencia, destacar visualmente la alerta de stock crítico a nivel de especie, y ofrecer edición/baja por lote y alta de un lote nuevo.

**Respuesta obtenida (síntesis):** encabezado con nombre de especie y botón de volver; banner de alerta de stock bajo (RF03); tarjetas por lote con badge de estado (bajo/agotado) y botones de editar/dar de baja; barra inferior fija con "Cargar nuevo lote". Se incluye un lote dado de baja como ejemplo de que el historial se conserva (HU-03). Contenido completo en el archivo HTML citado arriba.

## Ciclo 2 — Evaluación heurística (rol: especialista en interfaz de usuario)

**Prompt utilizado:** igual estructura que en HU-01, aplicada a esta pantalla, considerando que "dar de baja" es una acción destructiva sobre datos reales del usuario.

**Respuesta obtenida:**

| # | Heurística | Evaluación | Justificación |
|---|---|---|---|
| 1 | Visibilidad del estado del sistema | Cumple | La alerta de stock bajo y el estado de cada lote (bajo/agotado) son visibles sin acción adicional. |
| 2 | Coincidencia con el mundo real | Cumple | Usa vocabulario del dominio ("lote", "cosecha", "procedencia"). |
| 3 | Control y libertad del usuario | Incumple | No hay confirmación ni forma de deshacer inmediatamente después de tocar "Dar de baja". |
| 4 | Consistencia y estándares | Cumple | Mismas tarjetas, badges y botones que en el resto del sistema. |
| 5 | Prevención de errores | Incumple | "Dar de baja" ejecuta sin diálogo de confirmación pese a ser irreversible en la práctica. |
| 6 | Reconocimiento antes que recuerdo | Cumple | Toda la información del lote está en la tarjeta, no hay que recordar datos de otra pantalla. |
| 7 | Flexibilidad y eficiencia de uso | Parcial | No hay forma de ordenar o filtrar lotes (por año, por cantidad); no es crítico con pocos lotes, pero no escala. |
| 8 | Diseño estético y minimalista | Parcial | El banner de alerta compite visualmente con el título "Lotes registrados" inmediatamente debajo. |
| 9 | Ayuda a reconocer, diagnosticar y recuperarse de errores | Incumple | Al no haber confirmación de baja (punto 5), tampoco hay forma de recuperarse de una baja accidental. |
| 10 | Ayuda y documentación | Incumple | No hay ícono ni texto de ayuda contextual en la pantalla. |

## Decisión del grupo docs/ui/heuristic-review

| # | Decisión (Aceptado/Rechazado) | Motivo |
|---|---|---|
| 3 | Aceptado | Se agregara un modal de confirmacion antes de la baja con opcion a cancelar |
| 5 | Aceptado | Se alinea ocn la decision del item 3 para prevenir eliminaciones accidentales con los dedos en movilidad |
| 7 | Rechazado | Una especie no suele tener mas de 2 o 3 lotes simultaneos. Agregar filtros en esta pantalla recargaria visualmente la interfaz de forma innecesaria |
| 8 | Rechazado | Es una decision de diseño priorizar el RNF de seguridad y la visibilidad de stock critico sobre la estetica, garantizando que la alerta se destaque ante todo|
| 9 | Aceptado | El modal de confirmacion previene el error; adicionalmente, los lotes dados de baja conservan su registro historico visible, sin eliminarse fisicamente de la base |
| 10 | Rechazado | Los terminos "Stock bajo" y "Agotado" son autoexplicativos en el lenguaje del dominio para el usuario |

## Ciclos adicionales

**Motivo del ajuste:** la clienta aclaró que la existencia de semillas no se cuenta (son muy chicas), sino que se registra como "hay o no hay stock" por lote, con año y procedencia. Se reemplazó el modelo de cantidad por este.

**Hallazgo #7 (Flexibilidad — "no permite ordenar por cantidad") — deja de aplicar**, ya que no existe más un valor numérico de cantidad para ordenar.

**Hallazgos #3, #5, #9 (falta de confirmación al dar de baja/marcar sin stock) — siguen vigentes sin cambios**, ahora aplicados al botón "Marcar sin stock" en lugar de "Dar de baja".

**Decisión del grupo docs/ui/heuristic-review:** sin cambios respecto de la tabla original — las filas #3, #5 y #9 siguen aceptadas.

## Ciclo adicional 2 — corrección de alcance

El grupo decidió acotar el ajuste anterior: **se revierte el modelo "en stock sí/no"** y se vuelve al modelo de cantidad del SRS (cantidadInicial/cantidadActual, alerta por umbral de RF03) sin cambios. Solo se agrega **mes de cosecha** como dato nuevo, opcional, junto al año que ya existía en el SRS. El hallazgo #7 ("ya no aplica" del ciclo anterior) queda sin efecto: vuelve a aplicar tal como en la evaluación original, ya que la cantidad numérica está de nuevo presente.
