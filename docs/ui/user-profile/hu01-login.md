# Evaluación heurística — HU-01 · Iniciar sesión

Archivo maquetado: `docs/ui/mockups/pantalla-hu01-login.html`

## Ciclo 1 — Generación del maquetado

**Prompt utilizado:** generar el maquetado HTML de la pantalla de inicio de sesión (HU-01, CU00, RF00) para el perfil de usuario "Usuario/jardinero-a" (ver `docs/ui/user-profiles/usuario.md`), mobile-first, usando Bootstrap 5, la paleta de colores definida por el grupo (verde principal #1B4D3E, alerta #D9381E, fondo #F8F9FA, texto #111111), tipografía Roboto/Inter (16px cuerpo, mínimo 20px títulos) y botones principales de al menos 48×48px. Debe incluir campos de usuario y contraseña, y representar el flujo alternativo A1 (credenciales inválidas) sin necesitar backend real.

**Respuesta obtenida (síntesis):** pantalla centrada verticalmente con logo, campos de usuario/contraseña, botón "Ingresar" de ancho completo (mín. 48px de alto), y un botón secundario de demostración que despliega un `alert` de Bootstrap para simular el flujo A1. Contenido completo en el archivo HTML citado arriba.

## Ciclo 2 — Evaluación heurística (rol: especialista en interfaz de usuario)

**Prompt utilizado:** evaluar la pantalla anterior heurística por heurística, según las diez heurísticas de usabilidad de Nielsen, considerando específicamente el perfil de usuario y el escenario de uso definidos (una persona con una sola mano libre, en exterior, con posible luz solar directa) y no un usuario genérico. Indicar para cada heurística si se cumple, se cumple parcialmente o se incumple, y por qué.

**Respuesta obtenida:**

| # | Heurística | Evaluación | Justificación |
|---|---|---|---|
| 1 | Visibilidad del estado del sistema | Parcial | El error de credenciales se muestra claramente, pero no hay ningún indicador de carga al tocar "Ingresar" (falta feedback mientras se procesa la autenticación). |
| 2 | Coincidencia con el mundo real | Cumple | Lenguaje simple ("Usuario", "Contraseña"), sin jerga técnica. |
| 3 | Control y libertad del usuario | Parcial | No hay opción de recuperar contraseña; puede ser aceptable dado que TP1 solo usa dos cuentas precargadas, pero queda como carencia si se generaliza. |
| 4 | Consistencia y estándares | Cumple | Mismos colores, tipografía y estilo de botón que el resto de las pantallas del sistema. |
| 5 | Prevención de errores | Incumple | El botón "Ingresar" no valida que los campos estén completos antes de intentar enviar. |
| 6 | Reconocimiento antes que recuerdo | Cumple | No exige recordar nada de otra pantalla. |
| 7 | Flexibilidad y eficiencia de uso | Parcial | No ofrece atajos (recordar sesión, biometría); razonable para dos cuentas precargadas, pero limita la eficiencia en un uso más frecuente. |
| 8 | Diseño estético y minimalista | Cumple | Pantalla despejada, un solo objetivo por pantalla. |
| 9 | Ayuda a reconocer, diagnosticar y recuperarse de errores | Cumple | El mensaje de error es específico sobre qué hacer ("probá de nuevo"), sin revelar cuál campo falló (correcto por seguridad). |
| 10 | Ayuda y documentación | Incumple | No hay ningún acceso a ayuda o contacto visible desde esta pantalla. |

## Decisión del grupo (a completar)

Para cada fila marcada como "Parcial" o "Incumple", el grupo debe indicar si acepta el hallazgo (y qué ajuste hace) o si lo rechaza (y por qué no aplica a este proyecto). Este es el paso pedagógico central de la actividad — no debe quedar vacío en la entrega final.

| # | Decisión (Aceptado/Rechazado) | Motivo |
|---|---|---|
| 1 | | |
| 3 | | |
| 5 | | |
| 7 | | |
| 10 | | |

## Ciclos adicionales

*(Completar si, tras la revisión del grupo, se ajusta la pantalla y se vuelve a interactuar con la IA. Registrar cada ciclo con el mismo nivel de detalle.)*
