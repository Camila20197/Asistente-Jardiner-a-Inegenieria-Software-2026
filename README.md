# Asistente de Jardinería

**Integrantes**
* Camila Durand
* Lucia Garcia Bode
* Milagros Morello Deppeler

### Descripcion General
El **Asistente de Jardinería** es un software orientado al uso movil diseñado para Técnicos y estudiantes en Jardineria de la UNER, agrónomos y público general. La plataforma centraliza la gestion de ficas botanicas, automatiza el control predictivo de stock de semillas y proporciona una bitácora personal de campo para documentar el desarrollo de cultivos mediante notas.

Para consultar la documentación técnica completa, diagramas de contexto, dominio y casos de uso, dirigire a la [Especificacioón de Requerimientos de Softwre (SRS)](docs/requirements/srs.md)


### Ciclo de Vida del Software
Se ha seleccionado un **Ciclo de Vida Iterativo Incremental**, debido a que los requerimientos de dominio no se encuentran completamente cerrados y pueden evolucionar con la interacción del usuario, este modelo permite validar tempranamente el Producto Minimo Viable (MVP) basado en el inventario de semillas y la bitácora persona, incorporando funciones complejas e integraciones externas en interaciones posteriores.

### Fuentes de descubrimiento
* Dominio y problema: asistente personal para el control de huerta, semillas y/o jardinería. Los técnicos y jardineros son quienes administran esto lo hacen en cuaderno o papel.
* Datos: datos textuales y observaciones que provienen de la práctica y de bibliografía.
* Usuarios y stakeholders: técnico jardinero, agrónomos, usuario general, administrador.
* Alcance realista: información de flora, stock de semillas, bitácora personal.
* Valor: posibilidad de maximizar lo estudiado y observado, teniéndolo todo en un solo soporte.

### Stakeholders y roles

#### Stakeholders
1. Ingenieros agrónomos
2. Técnicos en jardinería
3. Público general con conocimiento en jardinería

#### Roles del sistema:
1. Administrador
2. Usuario

#### Administrador

Rol interno del sistema, no un perfil del dominio. La entrevista con la clienta no
mostró un segundo perfil que administre el sistema, así que el administrador no tiene
funcionalidad propia en esta primera versión.
Se lo mantiene identificado porque el catálogo de especies es un dato de referencia
compartido y no personal: alguien tiene que responder por su consistencia. Sus
responsabilidades previstas son:
- Curar el catálogo compartido de especies: altas, correcciones y unificación de duplicados.
- Validar las fichas incorporadas desde fuentes externas (Flora Argentina, GBIF)
  antes de que queden disponibles para consulta.
- Dar de alta las cuentas de usuario.
Ninguna de las tres se desarrolla en este TP: se trabaja con dos cuentas precargadas
y el catálogo se carga manualmente. El administrador queda documentado a nivel de
alcance, sin casos de uso ni historias de usuario propias.

#### Usuario

Perfil del jardinero/a que lleva su propio registro botánico. Es el usuario final del
sistema y el destinatario del valor central del prototipo: hoy resuelve esto con una
planilla de cálculo que consulta desde el celular, más carpetas de fotos sueltas en la
PC, sin conexión entre ambas.
Trabaja mayormente desde el celular, en el jardín, en el momento de estar frente a
la planta. Sus tareas son:
- Cargar fichas de especie de forma incremental: primero la identidad (nombre
  científico, nombre común, familia) y los cuidados a medida que consigue la
  información.
- Asociar fotos a cada especie, clasificadas por tipo (planta completa, hoja, flor,
  fruto, semilla).
- Registrar los lotes de semillas que tiene en stock, con año y procedencia.
- Registrar notas de campo asociadas a una especie para documentar cómo evoluciona
  el cultivo.
- Consultar el calendario mensual para ver qué especies tienen alguna actividad ese
  mes: siembra, tratamiento pregerminativo, poda, fertilización, trasplante o
  reproducción asexual.
- Consultar la ficha completa de una especie mientras trabaja con ella.
Los lotes de semillas y las notas de campo pertenecen únicamente a la cuenta que los
cargó. El catálogo de especies, en cambio, es compartido (ver Administrador).