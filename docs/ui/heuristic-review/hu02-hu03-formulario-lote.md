# Evaluación heurística — HU-02 / HU-03 · Formulario de alta/edición de lote

Archivo maquetado: `docs/ui/mockups/pantalla-hu02-hu03-formulario-lote.html`

## Ciclo 1 — Generación del maquetado

**Prompt utilizado:** generar el formulario de alta/edición de lote (HU-02, HU-03 — RF01, RF02), mismo perfil, mismos criterios técnicos que las pantallas anteriores. Debe incluir cantidad inicial, año y procedencia, representar los flujos alternativos A1 (cantidad ≤ 0) y A2 (año futuro) de CU01, y la opción de dar de baja el lote cuando se usa en modo edición.

**Respuesta obtenida (síntesis):** formulario con especie de solo lectura (llega desde la pantalla anterior), campos de cantidad/año/procedencia, mensajes de error de ejemplo activables con un botón de demostración, sección de "dar de baja" y barra inferior con Cancelar/Guardar. Contenido completo en el archivo HTML citado arriba.

## Ciclo 2 — Evaluación heurística (rol: especialista en interfaz de usuario)

**Respuesta obtenida:**

| # | Heurística | Evaluación | Justificación |
|---|---|---|---|
| 1 | Visibilidad del estado del sistema | Parcial | En el mockup estático los errores de validación solo aparecen con un botón de demostración; en la versión funcional deberían dispararse automáticamente al perder foco o al intentar guardar. |
| 2 | Coincidencia con el mundo real | Cumple | Campos y unidades reconocibles para quien maneja semillas (año de cosecha, procedencia). |
| 3 | Control y libertad del usuario | Incumple | El bloque "Dar de baja" aparece siempre en el mockup, aunque el texto aclara que debería verse solo en modo edición — no está realmente condicionado. |
| 4 | Consistencia y estándares | Cumple | Mismo patrón de formulario y barra inferior que el resto de las pantallas. |
| 5 | Prevención de errores | Parcial | Los campos numéricos usan `min`/`max` de HTML, pero el año futuro no queda bloqueado de forma dura, solo advertido por mensaje. |
| 6 | Reconocimiento antes que recuerdo | Cumple | La especie queda visible arriba; no hay que recordar de qué pantalla se vino. |
| 7 | Flexibilidad y eficiencia de uso | Incumple | No hay valores pre-cargados (ej. año actual sugerido), el usuario siempre tipea todo desde cero. |
| 8 | Diseño estético y minimalista | Cumple | Formulario corto, sin elementos sobrantes. |
| 9 | Ayuda a reconocer, diagnosticar y recuperarse de errores | Cumple | Los mensajes de error son específicos por campo y explican la regla (A1/A2). |
| 10 | Ayuda y documentación | Incumple | No hay aclaración de qué se espera en "procedencia" para quien no lo tenga claro. |

## Decisión del grupo (a completar)

| # | Decisión (Aceptado/Rechazado) | Motivo |
|---|---|---|
| 1 | Aceptado | En la implementacion JS se adjuntara el evento onblur e input en cada campo para disparar las alertas en tiempo real |
| 3 | Aceptado | Se ocultara la seccion de baja mediante una clase d-none y solo se removera dicha clase via codigo cuando el formulario reciba un id_lote en modo edicion |
| 5 | Aceptado | Se configurará el atributo max="2026" dinamicamente segun la fecha actual del sistema para restringir el selector de año de forma dura |
| 7 | Aceptado | El campo "Año de cosecha" tomara por defecto el año en curso para reducir la carga de tipeo en el campo |
| 10 | Aceptado | Se incluira un texto de ayuda con ejemplos claros "ej: vivero, intercambio, cosecha propia" |

## Ciclos adicionales

**Motivo del ajuste:** se quitó el campo de cantidad inicial y su validación (flujo A1), reemplazado por un selector "¿Hay stock? Sí/No", y se agregó el mes de recolección como campo opcional junto al año.

**Hallazgo #5 (Prevención de errores) — mejora parcialmente**: al no existir más el campo de cantidad, desaparece ese caso puntual de validación faltante; se mantiene vigente para el año futuro (A2), que sigue sin bloquearse de forma dura.

**Hallazgo nuevo:**

| # | Heurística | Evaluación | Justificación |
|---|---|---|---|
| 1 | Visibilidad del estado del sistema | Parcial | El control "Sí/No" de stock aparece con "Sí" preseleccionado sin que quede claro por qué ese es el valor por defecto al crear un lote nuevo. |

**Decisión del grupo (a completar):**

| # | Decisión (Aceptado/Rechazado) | Motivo |
|---|---|---|
| 1 (nuevo) | | |

## Ciclo adicional 2 — corrección de alcance

Se revierte el control "¿Hay stock? Sí/No" del ciclo anterior: el hallazgo #1 de esa vuelta queda sin efecto porque ese control ya no existe. Se restablece el campo "Cantidad inicial" con su validación A1 tal como en la evaluación original, y se agrega únicamente **mes de cosecha** como campo nuevo y opcional junto al año. Las filas #1, #3, #5, #7 y #10 de la tabla original vuelven a aplicar sin cambios.
