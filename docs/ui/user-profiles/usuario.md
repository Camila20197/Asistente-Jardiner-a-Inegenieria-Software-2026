# Perfil de usuario — Usuario 

**Actor de TP1 al que corresponde:** rol "Usuario" único actor con casos de uso e historias de usuario propias en TP1; el administrador queda documentado en el SRS sin CU ni HU propias, por lo que no tiene perfil en esta Parte B.

**Nota de alcance:** el SRS define tres stakeholders de dominio: Ingeniero Agrónomo, Técnico en Jardinería, Público interesado; pero aclara explícitamente en "Decisiones de modelado" que ninguno de los tres dispara un comportamiento distinto en el sistema  todos operan como el mismo rol "Usuario". Por eso se construye un único perfil unificado en vez de tres variantes, siguiendo la propia decisión de modelado del grupo.

---

## Perfil

- **Quién es:** una persona que lleva su propio registro botánico de su huerta o jardín personal. No es un perfil profesional diferenciado a nivel de sistema.
- **Objetivo con el sistema:** llevar de forma incremental el registro de sus especies, su stock de semillas por lote y sus observaciones de campo, reemplazando la combinación actual de planilla de cálculo + carpetas de fotos sueltas que hoy usa sin conexión entre ambas.
- **Contexto de uso:** mayoritariamente desde el celular, en el jardín, en el momento de estar frente a la planta.
- **Motivación de fondo:** hoy pierde semillas por vencimiento y no conserva registro de qué técnicas funcionaron en temporadas pasadas, por la desorganización del método actual.
- **Nivel de conocimiento técnico — supuesto declarado del grupo:** Se asume un nivel de manejo básico de aplicaciones de uso cotidiano, ya usa una planilla de cálculo desde el celular, sin experiencia previa con herramientas especializadas de gestión agrícola. Este es un supuesto para el diseño, no un dato tomado literalmente del SRS.
- **Limitaciones/frustraciones esperadas — supuesto declarado del grupo:** al usar el celular parado en el jardín, es esperable que tenga una sola mano libre la otra ocupada con la planta, la maceta o herramientas y que la pantalla esté expuesta a luz solar directa. Esto no está escrito en el SRS pero se declara como supuesto de diseño, y es la base de la decisión ya tomada por el grupo de priorizar botones grandes (48×48 mínimo) ubicados en la parte inferior de la pantalla.

## Escenario de uso

Basado en HU-02 **Registrar un nuevo lote de semillas**:

> Es sábado a la tarde y el usuario vuelve del vivero con semillas de tomate nuevas. Parado frente al canterito donde va a guardarlas, saca el celular con una mano. Abre la aplicación, busca "Tomate" en su catálogo de especies y entra a la sección de lotes. Toca "Cargar nuevo lote", completa cantidad inicial, año y procedencia con el teclado numérico del celular, y confirma. El nuevo lote aparece de inmediato en el listado, sin que haya tenido que soltar la maceta que sostenía con la otra mano.

## Flujo de navegación

```
Login (HU-01)
  └─ Panel de visualización (HU-10, HU-11)
       ├─ Catálogo de especies por mes de siembra (HU-05)
       │     ├─ Ficha de especie, consulta (RF08)
       │     └─ Alta manual de especie (HU-06) [si la especie buscada no existe]
       ├─ Listado de lotes por especie (HU-02, HU-03, HU-04)
       │     ├─ Formulario alta/edición de lote (HU-02, HU-03)
       │     └─ Alta manual de especie (HU-06) [si la especie no existe]
       └─ Bitácora — línea de tiempo por especie (HU-08, HU-09)
             └─ Formulario nueva entrada / editar entrada (HU-08, HU-09)
```

El Panel de visualización es la pantalla de entrada tras el login: desde ahí se accede a las tres áreas funcionales (stock, catálogo, bitácora). Este orden no está impuesto por ningún RF puntual — es una decisión de diseño del grupo para esta Parte B, ya que el Panel es la única pantalla que consolida las tres áreas (RF10, RF11) y es un punto de partida razonable para el usuario.
