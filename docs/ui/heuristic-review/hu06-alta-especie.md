# Evaluación heurística — HU-06 · Alta manual de especie

Archivo maquetado: `docs/ui/mockups/pantalla-hu06-alta-especie.html`

## Ciclo 1 — Generación del maquetado

**Prompt utilizado:** generar el maquetado del alta manual de especie (HU-06 — RF08), que se dispara como flujo alternativo desde HU-02/HU-05/HU-08 cuando la especie buscada no existe en el catálogo compartido. Mismo perfil y criterios técnicos; incluir nombre, selección de meses de siembra y cuidados básicos, y dejar explícito que el catálogo resultante es compartido entre todos los usuarios (a diferencia de los lotes y la bitácora, que son privados).

**Respuesta obtenida (síntesis):** formulario con campo de nombre, una grilla de 12 checkboxes para los meses de siembra, textarea de cuidados básicos, y un aviso aclarando el carácter compartido del catálogo. Barra inferior con Cancelar/Guardar. Contenido completo en el archivo HTML citado arriba.

## Ciclo 2 — Evaluación heurística (rol: especialista en interfaz de usuario)

**Respuesta obtenida:**

| # | Heurística | Evaluación | Justificación |
|---|---|---|---|
| 1 | Visibilidad del estado del sistema | Incumple | Ningún campo indica si es obligatorio; todos se ven con el mismo peso visual. |
| 2 | Coincidencia con el mundo real | Cumple | Vocabulario reconocible ("meses de siembra", "cuidados básicos"). |
| 3 | Control y libertad del usuario | Cumple | Botón "Cancelar" disponible en todo momento. |
| 4 | Consistencia y estándares | Cumple | Mismo patrón de barra inferior y estilo de formulario que el resto de la app. |
| 5 | Prevención de errores | Incumple | No valida que se haya seleccionado al menos un mes antes de permitir guardar. |
| 6 | Reconocimiento antes que recuerdo | Parcial | La grilla de 12 meses exige recorrer visualmente los 12 casilleros en vez de un patrón más guiado (ej. rango desde/hasta), aunque permite meses no contiguos. |
| 7 | Flexibilidad y eficiencia de uso | Cumple | Permite seleccionar cualquier combinación de meses, no solo un rango continuo. |
| 8 | Diseño estético y minimalista | Cumple | Formulario corto y sin elementos sobrantes. |
| 9 | Ayuda a reconocer, diagnosticar y recuperarse de errores | Incumple | No hay ningún mensaje si se intenta guardar sin nombre. |
| 10 | Ayuda y documentación | Parcial | El aviso sobre el catálogo compartido orienta al usuario, pero no hay ejemplos de qué escribir en "cuidados básicos". |

## Decisión del grupo (a completar)

| # | Decisión (Aceptado/Rechazado) | Motivo |
|---|---|---|
| 1 | | |
| 5 | Aceptado | Se marcará la sección "Identidad" como obligatoria y se deshabilitará el botón de guardado si los campos clave están vacíos. |
| 6 | Aceptado | Se reemplazó la lista por selectores de rango de meses (Desde/Hasta) por actividad, mejorando la usabilidad. |
| 9 | Aceptado | Se incluirá un resumen de errores en la parte superior del formulario al intentar enviar datos inválidos. |
| 10 | Aceptado | Se agregaron placeholders descriptivos (ej. "ej: riego moderado, sol pleno") en cada campo del formulario. |

## Ciclos adicionales

**Motivo del ajuste:** la entrevista con la clienta amplió sustancialmente el alcance de esta pantalla (reproducción, actividades de calendario, problemas fitosanitarios, fotos, cuidados incrementales), además de agregar los campos de identidad estructurados (género/epíteto/autor/variedad) con vista previa del formato correcto.

**Prompt utilizado (ciclo adicional):** rediseñar el formulario incorporando los puntos anteriores, dejando explícito que solo la identidad es obligatoria y todo lo demás se completa de forma incremental, y usando el mismo criterio de campos "opcional" que ya usan otras pantallas.

**Hallazgos de la vuelta anterior — estado:**
- El hallazgo #1 (Visibilidad — "ningún campo indica si es obligatorio") queda **resuelto**: ahora cada sección aclara "(obligatoria)" u "(opcional)" explícitamente.
- Los hallazgos #5 y #9 (falta de validación de meses/nombre) siguen sin resolverse — el formulario todavía no valida antes de guardar.

**Hallazgo nuevo:**

| # | Heurística | Evaluación | Justificación |
|---|---|---|---|
| 7 | Flexibilidad y eficiencia de uso | Incumple | Pese a que el alert aclara que la carga es incremental, no hay un botón del tipo "guardar y completar después" — todo pasa por el mismo botón "Guardar", lo que puede generar dudas sobre si guardar con campos vacíos es realmente válido. |

**Decisión del grupo (a completar):**

| # | Decisión (Aceptado/Rechazado) | Motivo |
|---|---|---|
| 7 (nuevo) | Aceptado | Se modificó el texto del botón principal a "Guardar borrador / Ficha parcial" y se añadió un aviso de "Carga incremental habilitada". |
