# Evaluación heurística — HU-08 / HU-09 · Formulario de nueva entrada / edición

Archivo maquetado: `docs/ui/mockups/pantalla-hu08-hu09-formulario-entrada.html`

## Ciclo 1 — Generación del maquetado

**Prompt utilizado:** generar el formulario de carga de una entrada de bitácora (HU-08, HU-09 — RF05, RF06), mismo perfil y criterios técnicos, representando el flujo de excepción E1 (error de formato) de CU02.

**Respuesta obtenida (síntesis):** especie de solo lectura, selector de fecha nativo, textarea amplio para la nota de campo, y mensaje de error de ejemplo activable con un botón de demostración. Barra inferior con Cancelar/Guardar. Contenido completo en el archivo HTML citado arriba.

## Ciclo 2 — Evaluación heurística (rol: especialista en interfaz de usuario)

**Respuesta obtenida:**

| # | Heurística | Evaluación | Justificación |
|---|---|---|---|
| 1 | Visibilidad del estado del sistema | Parcial | Igual que en el formulario de lote: el error de formato solo se muestra vía botón de demostración, no automáticamente. |
| 2 | Coincidencia con el mundo real | Cumple | El campo de notas admite texto libre, tal como el usuario ya registra sus observaciones hoy en papel/planilla. |
| 3 | Control y libertad del usuario | Cumple | Botón "Cancelar" siempre disponible. |
| 4 | Consistencia y estándares | Cumple | Mismo patrón de formulario que el resto de la app. |
| 5 | Prevención de errores | Incumple | El textarea de notas no muestra ningún límite de longitud ni contador de caracteres. |
| 6 | Reconocimiento antes que recuerdo | Cumple | La especie asociada queda visible arriba del formulario. |
| 7 | Flexibilidad y eficiencia de uso | Incumple | No permite adjuntar fotos a la observación, algo que el SRS menciona como necesidad del usuario aunque no tenga HU propia todavía (queda registrado como límite de alcance, no de esta pantalla puntual). |
| 8 | Diseño estético y minimalista | Cumple | Formulario corto, un solo objetivo. |
| 9 | Ayuda a reconocer, diagnosticar y recuperarse de errores | Cumple | El mensaje de error de formato de fecha es específico y comprensible. |
| 10 | Ayuda y documentación | Incumple | No hay ningún ejemplo de qué tipo de observación registrar, para quien recién empieza a usar la bitácora. |

## Decisión del grupo (a completar)

| # | Decisión (Aceptado/Rechazado) | Motivo |
|---|---|---|
| 1 | | |
| 5 | | |
| 7 | | |
| 10 | | |

## Ciclos adicionales

*(Completar si corresponde.)*
