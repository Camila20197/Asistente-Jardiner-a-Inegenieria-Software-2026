# Evaluación heurística — HU-10 / HU-11 · Panel de visualización

Archivo maquetado: `docs/ui/mockups/pantalla-hu10-hu11-panel.html`

## Ciclo 1 — Generación del maquetado

**Prompt utilizado:** generar el panel de visualización consolidado (HU-10, HU-11 — RF10, RF11, RF12), mismo perfil y criterios técnicos, como pantalla de entrada tras el login, con navegación inferior hacia las tres áreas funcionales (lotes, catálogo, bitácora) y filtros por especie y rango de fechas.

**Respuesta obtenida (síntesis):** tarjeta destacada con el número de especies en alerta, filtros de especie/fecha, listado de stock por especie con badges de estado, bloque de bitácora reciente, ejemplo de estado vacío, y navegación inferior fija de 4 secciones. Contenido completo en el archivo HTML citado arriba.

## Ciclo 2 — Evaluación heurística (rol: especialista en interfaz de usuario)

**Respuesta obtenida:**

| # | Heurística | Evaluación | Justificación |
|---|---|---|---|
| 1 | Visibilidad del estado del sistema | Cumple | La tarjeta superior comunica de inmediato cuántas especies están en alerta, sin necesidad de scroll. |
| 2 | Coincidencia con el mundo real | Cumple | Agrupa la información tal como el usuario la piensa: por especie, con su bitácora asociada. |
| 3 | Control y libertad del usuario | Cumple | La navegación inferior permite moverse libremente entre las cuatro áreas en cualquier momento. |
| 4 | Consistencia y estándares | Incumple | Los filtros de este panel usan menús desplegables, mientras que el catálogo (HU-05) filtra con chips de mes — dos patrones distintos para la misma acción de filtrar dentro de la misma app. |
| 5 | Prevención de errores | Cumple | No hay acciones destructivas en esta pantalla. |
| 6 | Reconocimiento antes que recuerdo | Cumple | El resumen consolida datos de stock y bitácora sin exigir recordar información de otras pantallas. |
| 7 | Flexibilidad y eficiencia de uso | Incumple | Los filtros de especie y fecha no tienen una acción de "aplicar" clara ni muestran cuántos resultados arrojan antes de aplicarlos. |
| 8 | Diseño estético y minimalista | Parcial | La pantalla acumula stock, bitácora reciente y un ejemplo de estado vacío en simultáneo — en la versión real conviviría solo uno de esos estados por vez, pero en el mockup se ven juntos y puede sentirse recargada. |
| 9 | Ayuda a reconocer, diagnosticar y recuperarse de errores | Cumple | El estado vacío es informativo y no se presenta como un error. |
| 10 | Ayuda y documentación | Incumple | No hay ninguna affordance visible que explique el ícono de estado vacío ("🪴") para un usuario que lo vea por primera vez. |

## Decisión del grupo docs/ui/heuristic-review

| # | Decisión (Aceptado/Rechazado) | Motivo |
|---|---|---|
| 4 | Aceptado | Se unificarán las barras de filtro rápido utilizando el patrón de chips de selección horizontal en toda la app. |
| 7 | Aceptado | Los filtros se aplicarán de forma reactiva/instantánea al seleccionar, mostrando dinámicamente la cantidad de registros coincidentes. |
| 8 | Rechazado | Se trata de un mockup didáctico diseñado para mostrar todos los componentes posibles a la cátedra; en ejecución real solo se renderiza el estado vacío si no existen datos. |
| 10 | Aceptado | Se acompañará el ícono con el mensaje claro: "Aún no has registrado lotes ni notas de campo. Comienza cargando una especie". |
