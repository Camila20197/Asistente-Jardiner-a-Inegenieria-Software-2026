# Evaluación heurística — HU-08 / HU-09 · Bitácora, línea de tiempo

Archivo maquetado: `docs/ui/mockups/pantalla-hu08-hu09-bitacora-timeline.html`

## Ciclo 1 — Generación del maquetado

**Prompt utilizado:** generar la línea de tiempo de bitácora de una especie (HU-08, HU-09 — RF05, RF06), mismo perfil y criterios técnicos. Representar visualmente el trabajo offline (decisión del grupo documentada en el perfil de usuario) con un indicador de "sin sincronizar" en la entrada más reciente.

**Respuesta obtenida (síntesis):** línea de tiempo vertical con una tarjeta por entrada (fecha, nota, acciones de editar/eliminar), la entrada más reciente marcada con un indicador de sincronización pendiente. Botón inferior fijo para agregar una nueva entrada. Contenido completo en el archivo HTML citado arriba.

## Ciclo 2 — Evaluación heurística (rol: especialista en interfaz de usuario)

**Prompt utilizado:** el mismo que en la evaluación de HU-01 (ver `hu01-login.md`), aplicado a esta pantalla con el mismo perfil de usuario y escenario de uso.
**Respuesta obtenida:**

| # | Heurística | Evaluación | Justificación |
|---|---|---|---|
| 1 | Visibilidad del estado del sistema | Cumple | El estado "sin sincronizar" es visible directamente sobre la entrada afectada. |
| 2 | Coincidencia con el mundo real | Cumple | El formato de línea de tiempo coincide con la idea de un diario de campo cronológico. |
| 3 | Control y libertad del usuario | Incumple | El ícono de eliminar no tiene ningún paso de confirmación antes de borrar la entrada. |
| 4 | Consistencia y estándares | Cumple | Tarjetas y tipografía consistentes con el resto del sistema. |
| 5 | Prevención de errores | Incumple | Mismo problema que el punto 3: eliminar es una acción irreversible sin aviso previo. |
| 6 | Reconocimiento antes que recuerdo | Cumple | El texto completo de cada nota es visible en la tarjeta, sin truncar. |
| 7 | Flexibilidad y eficiencia de uso | Incumple | No hay forma de buscar o filtrar entradas dentro de una especie con historial extenso (esto conecta directamente con el escenario de Eficiencia de desempeño de la Parte A sobre volumen de historial acumulado). |
| 8 | Diseño estético y minimalista | Cumple | Jerarquía clara entre fecha, nota y acciones. |
| 9 | Ayuda a reconocer, diagnosticar y recuperarse de errores | Incumple | Al no existir confirmación de borrado (puntos 3 y 5), tampoco hay forma de deshacer una eliminación accidental. |
| 10 | Ayuda y documentación | Incumple | No se explica qué significa el estado "sin sincronizar" ni qué debería hacer el usuario al respecto. |

## Decisión del grupo docs/ui/heuristic-review

| # | Decisión (Aceptado/Rechazado) | Motivo |
|---|---|---|
| 3 | Aceptado | Se incorporará un diálogo de confirmación antes de eliminar cualquier registro de la línea de tiempo. |
| 5 | Aceptado | Ídem punto anterior. Previene borrados involuntarios durante el manejo del teléfono en el jardín. |
| 7 | Aceptado | Se agregará una barra de búsqueda por palabra clave dentro del historial para facilitar la consulta con varios años acumulados (cumpliendo con el RNF de desempeño). |
| 9 | Aceptado | Se implementará un toast o notificación de "Entrada eliminada - [Deshacer]" por 5 segundos tras borrar. |
| 10 | Aceptado | Al tocar la píldora "Sin sincronizar", se desplegará una ayuda contextual (tooltip) que aclara: "Guardado localmente. Se sincronizará al recuperar la conexión". |

## Ciclos adicionales

### Ciclo adicional 1 — aplicación de hallazgos aceptados

**Herramienta:** Claude
**Prompt utilizado:** a partir del maquetado original y de las decisiones del grupo sobre los hallazgos 3, 5, 9 y 10, aplicar al HTML una confirmación antes de eliminar una entrada y una explicación visible del estado "Sin sincronizar", sin modificar el resto de la pantalla.

**Cambios aplicados al maquetado:**

- **Hallazgos 3 y 5 (control y libertad del usuario, prevención de errores):** el botón de eliminar abre un diálogo de confirmación con dos salidas. La opción segura, "Conservarla", aparece primero.
- **Hallazgo 9 (recuperarse de errores):** queda cubierto por la confirmación previa, que evita el borrado accidental. El aviso de "Deshacer" durante 5 segundos no se implementó en este ciclo.
- **Hallazgo 10 (ayuda y documentación):** el grupo había aceptado un tooltip al tocar la etiqueta "Sin sincronizar". Al aplicarlo se cambió por un aviso visible arriba de la línea de tiempo, porque en un celular los tooltips no aparecen al tocar: dependen de pasar el mouse por encima. Para un usuario que opera con el dedo, la solución aceptada no habría funcionado.
- Se quitó el párrafo que remitía a una "nota de RNF en el perfil de usuario", que no existe.

**Pendiente para la próxima iteración:** hallazgo 7, búsqueda dentro del historial.