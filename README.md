# Asistente de Jardinería

**Integrantes**
* Camila Durand
* Lucía García Bode
* Milagros Morello Deppeler

### Descripción general

El **Asistente de Jardinería** es una aplicación orientada al uso móvil, pensada para técnicos y estudiantes de Jardinería de la UNER, agrónomos y público general. Centraliza las fichas botánicas, el control del stock de semillas con alertas de stock crítico y una bitácora personal de campo para documentar la evolución de los cultivos.

### Documentación

* [Especificación de Requerimientos de Software (SRS)](docs/requirements/srs.md): visión y alcance, diagramas de contexto, modelo de dominio, requerimientos funcionales, casos de uso e historias de usuario.
* [Escenarios de atributo de calidad](docs/requirements/quality-scenarios/quality-scenarios.md) (TP2, Parte A).
* [Perfil de usuario, escenario de uso y flujo de navegación](docs/ui/user-profiles/usuario.md) (TP2, Parte B).
* [Maquetados HTML](docs/ui/mockups/) y [evaluaciones heurísticas por pantalla](docs/ui/heuristic-review/) (TP2, Parte B).
* [Registro de uso de IA](docs/uso-ia.md).

### Ciclo de vida del software

Se seleccionó un **ciclo de vida iterativo e incremental**, porque los requerimientos del dominio no estaban completamente cerrados y pueden evolucionar con la interacción del usuario. Este modelo permite validar tempranamente un Producto Mínimo Viable (MVP) basado en el inventario de semillas y la bitácora personal, e incorporar funciones complejas e integraciones externas en iteraciones posteriores.

### Fuentes de descubrimiento

* **Dominio y problema:** asistente personal para el control de huerta, semillas y jardinería. Hoy los técnicos y jardineros lo llevan en cuaderno, papel o planillas.
* **Datos:** datos textuales y observaciones que provienen de la práctica y de la bibliografía.
* **Usuarios y stakeholders:** técnico jardinero, agrónomos, usuario general, administrador.
* **Alcance realista:** información de flora, stock de semillas, bitácora personal.
* **Valor:** aprovechar al máximo lo estudiado y observado, teniéndolo todo en un solo soporte.

### Stakeholders y roles

#### Stakeholders
1. Ingenieros agrónomos
2. Técnicos en jardinería
3. Público general con conocimiento en jardinería

#### Roles del sistema
1. Administrador
2. Usuario

El detalle de cada rol está en la sección 1.3 del [SRS](docs/requirements/srs.md).