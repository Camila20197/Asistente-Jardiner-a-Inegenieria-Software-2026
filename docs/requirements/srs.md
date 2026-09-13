# Especificación de Requerimientos de Software (SRS)

## Proyecto: Asistente de Jardinería

## 1. Visión y alcance

### 1.1 Dominio y problema
En la jardinería, los cultivadores enfrentar desorganización en el seguimiento de sus cultivos o pérdida de insumos. Actualmente esto se resuelve de forma frangmentada mediante plantillas de cálculo, libretas de papel o la memoria, lo que puede provocar la pérdida de semillas por vencimiento y la falta de registros de técnicas que funcionaron en temporadas pasadas. 

### 1.2 Datos gestionados
* **Datos botánicos:** Fichas de especie, nombres científicos con reglas de formato (género en cursiva, variedad entre comillas simples), nombres comunes y familias.
* **Datos transaccionales de inventario:** Lotes de semillas, cantidades, mes y año de cosecha.
* **Bitácora:** Notas de campo en texto libre.

### 1.3 Usuarios y Stakeholders
**Stakeholders:**
1. Ingeniero Agrónomo
2. Técnicos en Jardineria
3. Público interesado

**Usuarios:**
* Roles:
1. Administrador
2. Usuario

### 1.4 Propuesta de valor
Transforma la gestión empírica en un proceso guiado y predecible. Permite la consulta instantánea de semillas viables y consolida el historial del jardin en una visión cronologica accesible.

### 1.5 Selección justificada del alcance para el MVP
* **Procesos seleccionados para desarrollar**
1. Control de semillas: Permite controlar el inventario.
2. Gestión de bitácora y observaciones: Permite realizar un seguimiento de las especies elegidas, añadiendo controles pregerminativos, tipos, enfermedades y plagas, entre otros.
* **Procesos descartados para iteracciones futuras:**
1. *Sincronización con Google Calendar API* y *Alertas Climáticas con Estación Meteorológica*. Se posponen por depender de APIs de terceros. Aislar estos componentes permite consolidar la arquitectura de datos propia y reducir riesgos técnicos.

### 1.6 Riesgo de fracaso y mitigación
**Riesgo identificado (módulo 1):** *Incertidumbre inicial y cambio de requerimientos sobre la bitácora o gestor de semillas*
**Estrategia de mitigación:** Adopción del ciclo de vida Iterativo e Incremental para entregar un MVP funcional temprano, validando la usabilidad y reglas de negocio con el usuario antes de desarrollar módulos avanzados.

### 1.7 Datos sensibles y ética profesional (Código IEEE/ACM)
En cumplimiento con el Código de Ética IEEE/ACM sobre la protección de la privacidad, las notas de campo y ubicaciones de cultivo pertenecen exclusivamente al ámbito privado del usuario. Se aplica *privacidad por diseño*, manteniendo las bitácoras aisladas y desacopladas del catálogo base compartido.


## 2. Diagramas de Contexto (DFD)

### 2.1 DFD Nivel 0
```mermaid
flowchart TD
    P((<br/>Asistente de Jardinería<br/>))
    U[Usuario]

    U -->|Lotes de semillas, notas de campo| P
    P -->|Alertas de stock, muro cronológico y fichas| U

    A[Administrador]
    A -->|Sincronizar la BD general| P
    P -->|Reporte de estado| A
```

### 2.2 DFD Nivel 1
```mermaid
flowchart TD
    %% Entidades Externas
    U[Usuario / Jardinero]
    ADM[Administrador]
    API[API Externa]

    %% Procesos Internos
    P1((1<br/>Sincronizar y administrar BD general))
    P2((2<br/>Controlar stock de semillas))
    P3((3<br/>Registrar bitácora personal))
    P4((4<br/>Visualizar historial y estado))

    %% Almacenes de Datos
    D1[(D1 · BD General de Especies)]
    D2[(D2 · Lotes de semillas)]
    D3[(D3 · Bitácora personal)]

    %% Flujos Proceso 1: Administración BD General
    ADM -->|solicitud de sincronización| P1
    API -->|datos botánicos externos| P1
    P1 -->|guarda / actualiza catálogo| D1

    %% Flujos Proceso 2: Control de Semillas
    U -->|datos de lote| P2
    P2 -->|lote registrado| D2
    D2 -->|antigüedad de lote| P2
    P2 -->|alerta de stock crítico| U

    %% Flujos Proceso 3: Bitácora Personal
    U -->|nota de campo y foto| P3
    D1 -->|especie consultada| P3
    P3 -->|observación guardada| D3

    %% Flujos Proceso 4: Visualización
    D1 -->|fichas botánicas generales| P4
    D2 -->|stock viable| P4
    D3 -->|entradas de bitácora| P4
    P4 -->|muro cronológico y paneles| U
```

## Modelo de dominio

Diagrama de clases de dominio derivado de los RF y de la decisión de uso personal: equematiza qué entidades existen, sus atributos y cómo se relacionan, no cómo se implementan.

```mermaid
classDiagram
    class Usuario {
        +id: int
        +nombreUsuario: string
        +contraseña: string
        +rol: RolUsuario
    }

    class RolUsuario {
        <<enumeration>>
        administrador
        usuario
    }

    class Especie {
        +id: int
        +nombre: string
        +mesesSiembra: int[]
        +cuidadosBasicos: string
    }

    class LoteDeSemilla {
        +id: int
        +cantidadInicial: int
        +cantidadActual: int
        +anio: int
        +procedencia: string
        +fechaAlta: date
    }

    class EntradaBitacora {
        +id: int
        +fecha: date
        +nota: string
    }

    class ConfiguracionSistema {
        +umbralStockCritico: int
    }

    Usuario "1" --> "1" RolUsuario : tiene
    Usuario "1" --> "0..*" LoteDeSemilla : posee
    Usuario "1" --> "0..*" EntradaBitacora : es autor de
    Especie "1" --> "0..*" LoteDeSemilla : se agrupa en
    Especie "1" --> "0..*" EntradaBitacora : es objeto de

    note for ConfiguracionSistema "Constante global del sistema.\nEl stock total por especie de un\nusuario (suma de cantidadActual de\nsus LoteDeSemilla de esa especie)\nse compara contra umbralStockCritico\npara disparar RF03."
```

### Diccionario de clases

| Clase | Descripción | RF/CU que la originan |
|---|---|---|
| `Usuario` | Cuenta con la que se accede al sistema. | RF00, CU00 |
| `RolUsuario` | Enumeración de los dos roles del sistema (administrador / usuario). | Sección "Stakeholders y roles" |
| `Especie` | Ficha de especie: catálogo de referencia, **compartido** entre todos los usuarios, no depende de quién lo cargó. | RF08 |
| `LoteDeSemilla` | Un lote de semillas de una especie, con su cantidad, año y origen. **Privado**: pertenece a un único `Usuario`. | RF01, RF02, RF03, CU01 |
| `EntradaBitacora` | Una observación de campo asociada a una especie. **Privada**: pertenece a un único `Usuario` (autor). | RF05, RF06, CU02 |
| `ConfiguracionSistema` | Valor constante y global del umbral de stock crítico; no varía por especie ni por usuario en TP1. | RF03 |

### Decisiones de modelado 

- **No se modelan `Agrónomo`, `TécnicoJardinero` ni `PúblicoGeneral` como subclases de `Usuario`.** Son perfiles de stakeholder (contexto de dominio), pero desde que CU01 quedó sin restricción por perfil profesional, ninguno de los tres dispara un comportamiento distinto en el sistema: modelarlos como clases separadas sería agregar estructura que ningún RF usa.
- **`RolUsuario` se modela como enumeración de `Usuario`, no como una clase con relaciones propias**, porque RF00b (permisos diferenciados por rol) está diferido: hoy el rol es un dato descriptivo, no un objeto con comportamiento.
- **No hay una clase para "Visualización" ni "Panel".** CU03 no introduce una entidad de dominio nueva: solo lee y agrega datos que ya existen en `LoteDeSemilla` y `EntradaBitacora`. Es una vista/reporte, no un concepto de negocio persistente.
- **El "stock total por especie" no es un atributo guardado**, es un valor derivado: suma de `cantidadActual` de los `LoteDeSemilla` de esa especie que pertenecen al usuario. Se recalcula para RF03 y RF11, no se almacena aparte, para evitar inconsistencias entre el valor guardado y la suma real de lotes.

## Elección de procesos a desarrollar

- Gestor de stock (semillas)
- Bitácora personal
- Visualización

Estos procesos conforman un núcleo de negocio propio, con lógica particular del proyecto, y no dependen de servicios externos, por lo que se pueden desarrollar, probar y validar en un entorno controlado.

## Requerimientos funcionales

Cada RF indica su prioridad para la línea base de TP1: **(obligatorio)** o **(opcional)**.

### Módulo 0 — Acceso

- **RF00 (obligatorio) — Autenticación:** el sistema debe permitir iniciar sesión con una de las dos cuentas precargadas (administrador / usuario), determinando el rol activo de la sesión.

### Módulo 1 — Gestión de Stock de Semillas

- **RF01 (obligatorio) — Registro y alta de lotes de semilla:** el sistema debe permitir registrar lotes de semillas existentes por especie, capturando cantidad inicial, año y origen, asociados al usuario que los registra (stock personal, no compartido).
- **RF02 (obligatorio) — Modificación y baja de lotes:** el sistema debe permitir actualizar el stock disponible de un lote, o darlo de baja si se agotó o descartó.
- **RF03 (opcional) — Alerta de stock crítico:** el sistema debe permitir definir un umbral mínimo de stock y emitir una alerta visible dentro de la aplicación cuando la cantidad disponible **de una especie (sumando todos sus lotes)** sea menor a dicho umbral. La alerta se evalúa a nivel de especie, no de lote individual, para evitar falsos negativos cuando el stock está repartido en varios lotes pequeños.
- **RF04 (obligatorio) — Consulta de semillas:** el sistema debe permitir filtrar el catálogo de semillas disponibles cuyo período de siembra (mes, de 1 a 12) sea el mes seleccionado.
- **RF08 (obligatorio) — Alta y consulta de ficha de especie:** el sistema debe permitir registrar una ficha de especie (nombre, período de siembra en meses, cuidados básicos), cargada manualmente, para poder asociarla a los lotes de semilla. El catálogo de especies es compartido entre todos los usuarios (no es un dato personal); solo los lotes de stock y las entradas de bitácora son privados por usuario.
- **RF09 (opcional) — Trazabilidad de movimientos de stock:** el sistema debe registrar qué usuario y en qué fecha/hora dio de alta, modificó o dio de baja un lote.

### Módulo 2 — Bitácora

- **RF05 (obligatorio) — Carga de notas y observación de campo:** el sistema debe permitir a cada usuario agregar notas y registros de evolución personal para cada ficha de especie, visibles únicamente para quien las creó.
- **RF06 (obligatorio) — Edición y eliminación de entradas:** el sistema debe permitir al usuario modificar o eliminar sus registros, parcial o completamente.

### Módulo 3 — Visualización

- **RF10 (obligatorio) — Historial de bitácora:** el sistema debe permitir visualizar, para una especie dada, la línea de tiempo de las entradas de bitácora registradas (fecha, autor, notas), ordenadas cronológicamente.
- **RF11 (obligatorio) — Panel de stock:** el sistema debe permitir visualizar un resumen del stock total de semillas por especie y por lote, destacando las especies por debajo del umbral crítico.
- **RF12 (obligatorio) — Filtros de visualización:** el sistema debe permitir filtrar la información visualizada por especie, por rango de fechas y/o por usuario que la cargó.

### Diferidos a un TP posterior

- **RF00b — Control de acceso por rol:** restringir funcionalidades específicas al rol administrador (ej. configuración de umbrales).
- **RF00c — Gestión de cuentas:** alta, baja y asignación de rol a cuentas de usuario (reemplazado en TP1 por las dos cuentas precargadas).



