# Evaluación heurística — Ficha de especie (vista)

Archivo maquetado: `docs/ui/mockups/pantalla-ficha-especie-vista.html`

**Nota de alcance:** esta pantalla no estaba en la primera versión de Parte B. Surge de la entrevista con la clienta, que amplió sustancialmente lo que debe contener una ficha de especie (identidad, cuidados incrementales, reproducción, calendario de actividades, problemas fitosanitarios, fotos). Todavía no tiene RF/HU formal en el SRS — ver la nota correspondiente en `docs/ui/user-profiles/usuario.md`.

## Ciclo 1 — Generación del maquetado

**Prompt utilizado:** generar la vista de consulta (solo lectura) de una ficha de especie, consolidando identidad, existencia de stock, cuidados (marcando explícitamente los campos aún sin completar), reproducción, calendario de actividades, problemas fitosanitarios con tratamientos ordenados de más suave a más fuerte, y una galería de fotos por tipo. Mismo perfil, mismos criterios técnicos (Bootstrap, paleta, tipografía, mobile-first) que el resto de las pantallas. Aplicar la regla de presentación del nombre científico (género y epíteto en cursiva, autor en texto normal, variedad entre comillas simples).

**Respuesta obtenida (síntesis):** pantalla de una sola columna organizada en secciones (Existencia, Cuidados, Reproducción, Calendario, Problemas fitosanitarios, Fotos), con accesos directos a editar la ficha, ver lotes y ver bitácora. Los campos sin completar se muestran en gris itálica en vez de ocultarse. Contenido completo en el archivo HTML citado arriba.

## Ciclo 2 — Evaluación heurística (rol: especialista en interfaz de usuario)

**Respuesta obtenida:**

| # | Heurística | Evaluación | Justificación |
|---|---|---|---|
| 1 | Visibilidad del estado del sistema | Cumple | El estado de stock y los campos "todavía sin completar" son explícitos, no ambiguos. |
| 2 | Coincidencia con el mundo real | Cumple | Formato de nombre científico correcto; vocabulario del dominio en todas las secciones. |
| 3 | Control y libertad del usuario | Cumple | Accesos directos a editar, lotes y bitácora sin callejones sin salida. |
| 4 | Consistencia y estándares | Incumple | Es la única pantalla con un patrón de "página larga por secciones"; el resto del sistema usa pantallas cortas centradas en una sola tarea. |
| 5 | Prevención de errores | Cumple | Pantalla de solo lectura, sin acciones destructivas. |
| 6 | Reconocimiento antes que recuerdo | Cumple | Toda la información de la especie está consolidada en un solo lugar. |
| 7 | Flexibilidad y eficiencia de uso | Incumple | Con seis secciones no hay forma de saltar directo a una en particular (ej. un índice); obliga a hacer scroll completo siempre. |
| 8 | Diseño estético y minimalista | Parcial | La cantidad de información condensada puede abrumar en un primer uso, pese a estar bien organizada por secciones. |
| 9 | Ayuda a reconocer, diagnosticar y recuperarse de errores | Cumple | No aplica al ser una pantalla de solo lectura. |
| 10 | Ayuda y documentación | Incumple | No se explica, por ejemplo, qué significa el orden de los tratamientos fitosanitarios (más suave a más fuerte) para alguien que lo vea por primera vez. |

## Decisión del grupo docs/ui/heuristic-review

| # | Decisión (Aceptado/Rechazado) | Motivo |
|---|---|---|
| 4 | Rechazado | Se justifica por ser la vista consolidada de consulta agronómica. Mantener toda la ficha en una sola vista continua evita tener que navegar entre pestañas en campo. |
| 7 | Aceptado | Se agregará una barra de accesos directos horizontales |
| 8 | Aceptado | Se estructurarán las secciones como paneles colapsables (accordions) dejando abiertos por defecto solo los cuidados principales y el stock. |
| 10 | Aceptado | Se incluirá una pequeña aclaración: "Tratamientos ordenados desde control biológico (suave) hasta químico (último recurso)" |
