# Evaluación heurística — HU-05 · Catálogo de especies por mes de siembra

Archivo maquetado: `docs/ui/mockups/pantalla-hu05-catalogo-especies.html`

## Ciclo 1 — Generación del maquetado

**Prompt utilizado:** generar el maquetado de la consulta de catálogo filtrado por mes de siembra (HU-05 — RF04), mismo perfil y criterios técnicos, representando el flujo de excepción E1 (ningún resultado para el filtro aplicado) como estado vacío informativo, no como error.

**Respuesta obtenida (síntesis):** buscador de texto, selector de mes como fila de chips horizontales, listado de especies con familia botánica y cuidados básicos, y un bloque de ejemplo mostrando el estado vacío de E1. Botón flotante para dar de alta una especie nueva. Contenido completo en el archivo HTML citado arriba.

## Ciclo 2 — Evaluación heurística (rol: especialista en interfaz de usuario)

**Respuesta obtenida:**

| # | Heurística | Evaluación | Justificación |
|---|---|---|---|
| 1 | Visibilidad del estado del sistema | Cumple | El mes seleccionado queda resaltado con color; se ve claramente qué filtro está activo. |
| 2 | Coincidencia con el mundo real | Cumple | Nombres comunes, familias botánicas y meses en formato calendario habitual. |
| 3 | Control y libertad del usuario | Cumple | Buscador y chips de mes permiten cambiar de filtro en cualquier momento sin pasos adicionales. |
| 4 | Consistencia y estándares | Incumple | Este filtro usa "chips" de mes, mientras que el Panel (HU-10/11) filtra con menús desplegables — son dos patrones distintos para la misma acción (filtrar) dentro de la misma app. |
| 5 | Prevención de errores | Cumple | No hay acciones destructivas en esta pantalla. |
| 6 | Reconocimiento antes que recuerdo | Cumple | Los resultados se listan directamente, sin requerir recordar códigos o nombres exactos. |
| 7 | Flexibilidad y eficiencia de uso | Incumple | No permite combinar el filtro de mes con otros criterios (por ejemplo, familia botánica). |
| 8 | Diseño estético y minimalista | Cumple | Jerarquía visual clara entre buscador, filtro y resultados. |
| 9 | Ayuda a reconocer, diagnosticar y recuperarse de errores | Cumple | El estado vacío sugiere una acción concreta ("probá con otro mes o dá de alta una especie nueva"). |
| 10 | Ayuda y documentación | Incumple | No se explica qué significa "período de siembra" para alguien que recién empieza. |

## Decisión del grupo docs/ui/heuristic-review

| # | Decisión (Aceptado/Rechazado) | Motivo |
|---|---|---|
| 4 | Aceptado | Se estandarizará el uso de chips interactivos horizontales en todas las vistas de filtrado rápido por ser más ergonómicos en móviles. |
| 7 | Rechazado | El alcance del MVP (TP1) exige únicamente el filtrado por mes de siembra. El filtrado avanzado por familia queda pospuesto. |
| 10 | Rechazado | El usuario objetivo (agrónomo, técnico o aficionado) conoce el concepto. No se requiere recargar la pantalla con explicaciones teóricas. |

## Ciclos adicionales

**Motivo del ajuste:** la clienta pidió que el calendario agrupe por tipo de actividad (siembra, tratamiento pregerminativo, poda, fertilización, trasplante, reproducción asexual), no solo por siembra — se agregó esa agrupación y una pestaña separada para la búsqueda libre por nombre.

**Hallazgo #4 (Consistencia) — sigue vigente** y se agrava: además de la diferencia de patrón de filtro con el Panel (chips vs. selects), ahora esta pantalla suma una pestaña "Por mes / Buscar" que no existe en ninguna otra parte del sistema.

**Hallazgo nuevo:**

| # | Heurística | Evaluación | Justificación |
|---|---|---|---|
| 2 / 10 | Coincidencia con el mundo real / Ayuda y documentación | Parcial | Los tipos de actividad se identifican con emojis (🌱 ✂️ 🌾 🌿) sin ninguna leyenda; alguien nuevo puede no asociar el emoji con el tipo de actividad de forma inequívoca. |

**Decisión del grupo docs/ui/heuristic-review:**

| # | Decisión (Aceptado/Rechazado) | Motivo |
|---|---|---|
| 4 (agravado) | Aceptado | La pestaña "Por mes / Buscar" que lo agravaba se quitó en el ciclo adicional 2. La diferencia de patrón con el Panel se resuelve con la unificación a chips aceptada en la fila 4. |
| 2/10 (nuevo) | Aceptado | Se agregará una etiqueta textual junto a cada emoji (ej. "🌱 Siembra", "✂️ Poda") para evitar ambigüedades visuales. |

## Ciclo adicional 2 — corrección de alcance

Se quitó la pestaña "Por mes / Buscar" del ciclo anterior — la búsqueda vuelve a convivir con los chips de mes en una sola vista, como en la versión original. Se conserva la agrupación por tipo de actividad debajo del selector de mes, porque es consecuencia directa de agregar el dato de "actividad" (tipo + rango de meses) que pidió la clienta, no una reestructuración de navegación. El hallazgo nuevo sobre los emojis sin leyenda (fila "2/10") sigue vigente.
