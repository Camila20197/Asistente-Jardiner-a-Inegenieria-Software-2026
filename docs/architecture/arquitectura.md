# Arquitectura


Definir la estructura arquitectónica del sistema Asistente de Huerta, transformando los escenarios de calidad y requerimientos funcionales en decisiones de diseño estructurales (contenedores, componentes, tácticas, estilos y patrones).
La arquitectura se especifica para los procesos principales definidos en la primer y segunda parte: Gestión de Stock de Semillas y Bitácora Personal, con sincronizacion diferida. El resto de las integraciones futuras (Servicio de Clima y Calendarios) se representan como sistemas externos o cajas negras.

Siglas:
* C4: Contexto, Contenedor, Componente, Código
* DA: Desición de arquitectura
* EC: Escenario de calidad
* PWA: Progressive Web App
* REST: Representational State Transfer


## Restricciones

* Restriccion tecnológica y de despliegue: La aplicacion debe funcionar en dispositivos moviles de gama baja/media, priorizando la ejecucion cliente (PWA/LocalFirst) usando IndexBD/SQLite Local y comunicacion por HTTPS/JSON con el backend.
* Restriccion del dominio/operación: Intermitencia o ausencia total de señal de internet en el campo. El núcleo operativo no puede depender de llamadas sincronas al servidor para la captura de datos.


## Contexto

Se recupera la visión de nivel 0 (Contexto) definida anteriormente. El usuario interactua con el sistema, y este se vincula con servicios externos de clima y notificaciones.


```mermaid
%%{init: {"wrap": true}}%%
C4Context
    title Diagrama de Contexto - Asistente de Huerta

    Person(jardinero, "Jardinero / Usuario", "Gestiona su huerta, su stock de semillas y su bitácora.")
    System(asistente, "Asistente de Huerta", "Catálogo de especies, lotes de semillas y bitácora de campo, con soporte offline.")

    System_Ext(servicioClima, "Servicio Meteorológico (futuro)", "API externa de clima y alertas de heladas.")
    System_Ext(servicioNotif, "Servicio de Notificaciones Push", "Envío de alertas móviles.")

    Rel(jardinero, asistente, "Registra especies, lotes y notas", "HTTPS")
    Rel(asistente, servicioClima, "Consulta pronóstico (diferido)", "JSON/HTTPS")
    Rel(asistente, servicioNotif, "Envía alertas de stock y siembra", "HTTPS")

    UpdateRelStyle(jardinero, asistente, $textColor="#F59E0B", $lineColor="#F59E0B", $offsetY="-115")
    UpdateRelStyle(asistente, servicioClima, $textColor="#F59E0B", $lineColor="#F59E0B", $offsetX="-70")
    UpdateRelStyle(asistente, servicioNotif, $textColor="#F59E0B", $lineColor="#F59E0B")
    UpdateLayoutConfig($c4ShapeInRow="2", $c4BoundaryInRow="1")
```


## Drivers Arquitectonicos
A partir de los escenarios de calidad y en el marco de las restricciones del proyecto, se identificaron los siguientes drivers que condicionan la estructura del sistema: 

* **EC-01 - Registro de datos en campo sin conectividad - Disponibilidad (Fiabilidad):** 100% de los registrs en la bitácora y lotes iniciados sin red se almacenan exitosamente en el dispositivo loca. Condiciona el estilo global del sistema, obliga a descartar una arquitectura web síncrona convencional e icorporar una arquitectura Cliente - Servidor Local - First, requiriendo un contenedor de Almacen Local (IndexDB) en la PWA del cliente.

* **EC-02 - Sincronizacion masiva en segundo plano - Eficiendia de Desempeño:** La interfaz maniene una respuesta fluida (<1s) mientras los datos acumulados se envial al resrvidor al recuperar conectividad. Obluga a incorporar un estilo Orientado a Eventos en la zona de sincronizacion, exigiendo la creacion de un contenedor de Cola de Tareas / Broker y componentes de procesamiento asincrono para no congelar el hilo principal del móvil.

* **EC-03: Tolerancia a conflictos de datos en sincronización - Capaciad de recuperación (Fiabilidad):** 0% de pérdida silenciosa de información ante divergencias de datos cargados en modo offline Obliga a diseñar un componente específico en el servidor (Motor de Resolución de Conflictos) y a estructurar las tablas de la base de datos central con esquemas de versionado y marcas de tiempo (timestamps).

* **EC-04 — Cifrado en tránsito y transaccionalidad de datos - Confidencialidad e Integridad (Seguridad):** 100% del tráfico de sincronización cifrado; las operaciones de actualización en base de datos son atómicas 100% completadas o revertidas por completo. Restringe los protocolos de comunicación entre el cliente y el servidor al uso exclusivo de HTTPS/TLS y condiciona la Capa de Acceso a Datos del servidor para implementar transacciones SQL atómicas mediante un ORM.

* **EC-05 — Extensibilidad modular para futuras integraciones -  Modularidad (Mantenibilidad):** Incorporación de nuevos módulos diferidos (Clima o Calendario Agrícola) con 0 modificaciones o regresiones sobre los módulos de Stock y Bitácora. Define la estructura interna del contenedor de la API Backend, obligando a adoptar el Patrón de Capas con dependencias unidireccionales y separación estricta entre controladores, servicios de negocio y persistencia.


## Estrategia de solución

### Selección de tácticas por driver

| Driver | Atributo libro (Bass) | Tácticas | Tácticas descartadas |
|---|---|---|---|
| EC-01 | Disponibilidad | Degradación controlada, operar offline localmente y manejo de excepciones | Redundancia activa: Descartada por complejidad y costo innecesario para uso personal |
|EC-02|Desempeño|Introducir concurrencia, ejecuta el proceso de sincronizacion en un hilo separado, y limita la cantidad de registros que se envian para no saturar la red|Aumentar recursos de hardware: Descartado por ser cliente movil de recurosos limitados|
|EC-03|Disponibilidad/Fiabilidad|Rolllback (vuelve al ultimo estado seguro), Transacciones y Mantenimiento de copias (versionado)|Ping y Eco: No resuelve la divergencia de datos ya guardados|
|EC-04|Seguridad|Cifrar datos (reposo/transitorio) y Transacciones atómicas|Detectar intrusion (IDS): Fuera del alcance del MVP de uso personal|
|EC-05|Modificabilidad|Encapsular, usar un intermediario y restringir dependencias|Diferir el enlace (Plugins dinamicos): Complejidad excesiva para la escala actual|


### Estilos arquitectónicos adaptados

**Estilo base global: *Cliente-Servidor desacoplado con persistencia local (Local-First)***
El Cliente (móvil/PWA) gestiona su propia interfaz y almacenamiento interno (IndexDB), garantizando respuest inmediata si red (EC-01). El Servidor actúa como punto central de sincronización y respaldo. 
Se sacrifican consistencias eventuales, los datos locales del cliente pueden diferir temporalmente de la base de datos remota hasta que se complete la sincronizacion.

**Estilo secundario: *por zona orientada a eventos (Broker)***
Aplica unicamente a la zona de sincronizacion en segundo plano. Se tiene mayor complejidad operativa al sumar un contenedor intermediario de cola (Redis). La PWA deposita el paquete de sincronizacion en el broker sin esperar el procesamiento sincrono bloqueante.


### Estilos por Contenedor

* En el contenedor Cliente (Aplicacion movil / PWA): 
    *   Patron MVVM (Modelo-vista-vista-modelo): Aisla la logica de interaccion de la UI y gestiona el estado reactivo local
    *   Patron repository local: Encapsula las lecturas y escrituras hacia IndexBD/SQLite local.

* En el Contenedor Servidor (API de Backend):
    *   Patrón Capas (o Hexagonal/Puertos y Adaptadores): Separa Presentación/Controladores, Servicios de Aplicación, Dominio (Stock/Bitácora) y Adaptadores de Acceso a Datos.
    *   Patrón Broker / Cola de Mensajes: Para encolar y procesar cambios pendientes o notificaciones pesadas de forma asincrónica.


### Aspectos transeversales

*   Autenticación y Autorización: Tokens JWT sobre HTTPS para validar la identidad en cada sincronización.
*   Manejo de Transacciones e Integridad: Transacciones locales y remotas (si la sincronización de un lote falla a la mitad, se ejecuta Rollback).
*   Auditoría y Registro: Campo last_modified y marcado de versión para resolución de conflictos (EC-03).
*   Gestión de excepciones: el Procesador de sincronización reintenta los lotes que fallan y registra como fallido el que no se puede aplicar, sin perderlo (EC-03).
*   Notificaciones: alertas push de stock bajo y de conflictos de sincronización, mediante un servicio externo.
*   Interoperabilidad: API REST con JSON sobre HTTPS.

**Aspectos transversales descartados:**

*   Instrumentación y monitoreo del servidor: descartado para el MVP de uso personal; los lotes fallidos quedan registrados y alcanzan para diagnosticar.
*   Auditoría completa de acciones por usuario: descartada porque cada usuario gestiona solo sus propios datos; el versionado con last_modified cubre lo que exige EC-03.

### Tabla de coberturas y sacrificios

|Driver|	Tácticas y Estilo/Patrón|	¿Cómo se cubre?	|Sacrificio Asumido|
|---|---|---|---|
|EC-01|	Degradación controlada / Cliente-Servidor LocalFirst|	La PWA lee y escribe en la base de datos local (IndexedDB) si no hay red.|	Complejidad de mantener lógica de almacenamiento duplicada (cliente y servidor).
|EC-02|	Introducir concurrencia / Broker y Web Workers|	El proceso de sincronización corre en un hilo secundario (Background Sync).	|Ligera latencia antes de que los cambios se reflejen en el servidor remoto.|
|EC-03|	Rollback y Versionado / Transacciones|	Servidor detecta timestamp/versiones y genera registros de revisión si hay conflicto.|	Requiere espacio adicional para guardar estados de conflicto para revisión del usuario.|
|EC-04|	Cifrado y Transacciones / HTTPS + AES|	Datos sensibles en el cliente se cifran en reposo y se transmiten vía HTTPS.|	Leve consumo adicional de CPU en el dispositivo móvil para cifrar/descifrar.|
|EC-05|	Encapsular / Arquitectura en Capas|	Cada módulo (Stock, Bitácora, Calendario futuro) expone interfaces limpias.|	Mayor cantidad de archivos y capas de indirección de código.|


## Vista de Contenedores
Vista global y única del sistema. Implementa el estilo base **cliente-servidor con persistencia local (Local-First)** y, solo en la zona de sincronización, el estilo **orientado a eventos** con patrón broker (DA-01, DA-02). El Servicio Meteorológico se mantiene como caja negra (integración futura).
### Diagrama de contenedores
```mermaid
%%{init: {"wrap": true}}%%
C4Container
    title Vista de Contenedores - Asistente de Huerta

    Person(jardinero, "Jardinero / Usuario", "Gestiona su huerta, stock y bitácora desde el celular.")
    System_Ext(servicioClima, "Servicio Meteorológico (futuro)", "API externa de clima.")

    System_Boundary(asistenteBoundary, "Asistente de Huerta") {
        Container(app, "Aplicación móvil", "PWA / React", "Interfaz táctil; opera sin conexión y sincroniza en segundo plano.")
        ContainerDb(dbLocal, "Almacén local", "IndexedDB", "Datos locales y cambios pendientes de sincronizar.")
        Container(api, "API de sincronización", "Python / FastAPI", "Autentica, entrega datos y encola lotes de cambios.")
        ContainerQueue(colaSync, "Cola de sincronización", "Redis durable (AOF)", "Retiene los lotes hasta procesarlos.")
        ContainerDb(dbCentral, "Base de datos central", "PostgreSQL", "Catálogo, lotes, bitácora, versiones y conflictos.")
        Container(procesador, "Procesador de sincronización", "Python / RQ", "Resuelve conflictos y aplica cada lote.")
    }

    Boundary(externos, "Sistemas externos") {
        System_Ext(servicioNotif, "Servicio de Notificaciones Push", "Alertas al celular.")
    }

    Rel(jardinero, app, "Registra y consulta", "HTTPS")
    Rel(app, dbLocal, "Lee y escribe", "IndexedDB")
    Rel(app, api, "Envía lotes y descarga datos", "JSON/HTTPS")
    Rel(api, dbCentral, "Lee datos y registra lotes", "SQL")
    Rel(api, colaSync, "Publica lotes", "Redis")
    Rel(procesador, colaSync, "Consume lotes", "Redis")
    Rel(procesador, dbCentral, "Aplica cambios (transacción)", "SQL")
    Rel(procesador, servicioNotif, "Pide alertas", "HTTPS")
    Rel(api, servicioClima, "Consulta pronóstico", "JSON/HTTPS")

    UpdateRelStyle(jardinero, app, $textColor="#F59E0B", $lineColor="#F59E0B", $offsetY="-45")
    UpdateRelStyle(app, dbLocal, $textColor="#F59E0B", $lineColor="#F59E0B", $offsetY="-95")
    UpdateRelStyle(app, api, $textColor="#F59E0B", $lineColor="#F59E0B")
    UpdateRelStyle(api, dbCentral, $textColor="#F59E0B", $lineColor="#F59E0B", $offsetX="-70")
    UpdateRelStyle(api, colaSync, $textColor="#F59E0B", $lineColor="#F59E0B", $offsetY="75", $offsetX="25")
    UpdateRelStyle(procesador, colaSync, $textColor="#F59E0B", $lineColor="#F59E0B")
    UpdateRelStyle(procesador, dbCentral, $textColor="#F59E0B", $lineColor="#F59E0B", $offsetY="55")
    UpdateRelStyle(procesador, servicioNotif, $textColor="#F59E0B", $lineColor="#F59E0B")
    UpdateRelStyle(api, servicioClima, $textColor="#F59E0B", $lineColor="#F59E0B", $offsetY="-150", $offsetX="30")
    UpdateLayoutConfig($c4ShapeInRow="2", $c4BoundaryInRow="1")
```
**Comprobación de restricciones de los estilos (Tabla 4):**

* Cliente-servidor: la Aplicación móvil siempre inicia la comunicación; no hay flechas desde la API ni desde la Base de datos central hacia el cliente; el cliente no accede a la Base de datos central (solo a su Almacén local). El aviso al usuario sale por el Servicio de Notificaciones Push, que es la excepción permitida (notificaciones).
* Orientada a eventos (zona de sincronización): la API (productor) y el Procesador de sincronización (consumidor) no se llaman entre sí; los dos se conectan solo a la Cola de sincronización. La API no espera el procesamiento: responde "202 Aceptado" apenas encola. Si un lote no se procesa, se reintenta (ver aspectos transversales).
* La cola es durable (persistencia en disco) porque EC-03 exige 0% de pérdida: un lote recibido no puede perderse si Redis se reinicia.
### Catalogo de la Vista de Contenedores

#### Catalogo de contenedores
| Contenedor | Tecnología | Responsabilidad |
|---|---|---|
| Aplicación móvil | PWA / React | Interfaz táctil. Permite registrar lotes y notas sin conexión y sincroniza en segundo plano al recuperar la red. |
| Almacén local | IndexedDB (en el dispositivo) | Guarda la copia local del catálogo, el stock y las notas, y los cambios marcados como pendientes de sincronizar. |
| API de sincronización | Python / FastAPI | Autentica al usuario, entrega datos consolidados al dispositivo y recibe los lotes de cambios para encolarlos. |
| Cola de sincronización | Redis con persistencia en disco | Retiene los lotes de cambios hasta que el Procesador los toma y confirma que terminó. |
| Procesador de sincronización | Python / RQ | Toma cada lote de la cola, resuelve conflictos de versión, aplica las reglas de negocio y guarda en una transacción. |
| Base de datos central | PostgreSQL | Almacenamiento persistente de catálogo, lotes, bitácora, versiones, estado de cada lote recibido y conflictos pendientes. |


#### Catalogo de Relaciones entre Contenedores
| Origen | Destino | Qué se comunica | Tipo | Protocolo |
|---|---|---|---|---|
| Jardinero / Usuario | Aplicación móvil | Uso de la interfaz: registro de lotes y notas, consultas | Persona hacia contenedor | HTTPS |
| Aplicación móvil | Almacén local | Lectura y escritura de datos y cambios pendientes | Acceso a datos (local) | IndexedDB API |
| Aplicación móvil | API de sincronización | Envío de lotes de cambios; descarga de datos consolidados y del estado de cada lote | Síncrona | JSON sobre HTTPS |
| API de sincronización | Base de datos central | Lectura de datos consolidados; registro y consulta del estado de los lotes recibidos | Acceso a datos | SQL |
| API de sincronización | Cola de sincronización | Publicación de lotes de cambios | Asincrónica | Protocolo Redis |
| Procesador de sincronización | Cola de sincronización | Toma de lotes pendientes y confirmación de procesamiento | Asincrónica | Protocolo Redis |
| Procesador de sincronización | Base de datos central | Escritura de cambios y conflictos en una transacción | Acceso a datos | SQL |
| Procesador de sincronización | Servicio de Notificaciones Push | Pedido de alertas de stock bajo y de conflictos | Integración externa | HTTPS |
| API de sincronización | Servicio Meteorológico | Consulta de pronóstico (futuro, caja negra) | Integración externa | JSON sobre HTTPS |

## Vista de Componentes
Se realiza un zoom sobre el contenedor princial de logica se servidor: API Backend de Sincronizacion

```mermaid
%%{init: {"wrap": true}}%%
C4Component
    title Vista de Componentes - Aplicación móvil

    Person(jardinero, "Jardinero / Usuario", "Usa la aplicación en la huerta.")

    Container_Boundary(appBoundary, "Aplicación móvil") {
        Component(vistas, "Vistas de stock y bitácora", "Componentes React", "Pantallas táctiles: formularios, listados y alertas.")
        Component(cifrado, "Cifrado local", "Web Crypto API (AES)", "Cifra y descifra los datos sensibles guardados.")
        Component(modelosVista, "Modelos de vista de stock y bitácora", "Estado React", "Validan lotes y notas, calculan stock bajo y exponen el estado.")
        Component(gestorSync, "Gestor de sincronización", "Service Worker", "Envía los cambios pendientes en segundo plano.")
        Component(repoLocal, "Repositorio local", "JavaScript", "Encapsula el almacén local y marca cambios pendientes.")
        Component(clienteApi, "Cliente de la API", "fetch + JWT", "Envía y recibe JSON por HTTPS con el token.")
    }

    Boundary(vecinos, "Contenedores vecinos") {
        ContainerDb(dbLocal, "Almacén local", "IndexedDB")
        Container(api, "API de sincronización", "Python / FastAPI")
    }

    Rel(jardinero, vistas, "Usa", "HTTPS")
    Rel(vistas, modelosVista, "Enlaza datos y acciones")
    Rel(modelosVista, repoLocal, "Lee y guarda lotes y notas")
    Rel(repoLocal, cifrado, "Cifra y descifra")
    Rel(repoLocal, dbLocal, "Lee y escribe", "IndexedDB")
    Rel(gestorSync, repoLocal, "Lee pendientes y actualiza estado")
    Rel(gestorSync, clienteApi, "Envía lotes y consulta estado")
    Rel(clienteApi, api, "Envía lotes y descarga datos", "JSON/HTTPS")

    UpdateRelStyle(jardinero, vistas, $textColor="#F59E0B", $lineColor="#F59E0B", $offsetY="-40")
    UpdateRelStyle(vistas, modelosVista, $textColor="#F59E0B", $lineColor="#F59E0B")
    UpdateRelStyle(modelosVista, repoLocal, $textColor="#F59E0B", $lineColor="#F59E0B")
    UpdateRelStyle(repoLocal, cifrado, $textColor="#F59E0B", $lineColor="#F59E0B", $offsetX="-90")
    UpdateRelStyle(repoLocal, dbLocal, $textColor="#F59E0B", $lineColor="#F59E0B")
    UpdateRelStyle(gestorSync, repoLocal, $textColor="#F59E0B", $lineColor="#F59E0B", $offsetY="-45")
    UpdateRelStyle(gestorSync, clienteApi, $textColor="#F59E0B", $lineColor="#F59E0B")
    UpdateRelStyle(clienteApi, api, $textColor="#F59E0B", $lineColor="#F59E0B")
    UpdateElementStyle(vistas, $bgColor="#1F5FAD", $borderColor="#174A87")
    UpdateElementStyle(cifrado, $bgColor="#1F5FAD", $borderColor="#174A87")
    UpdateElementStyle(modelosVista, $bgColor="#1F5FAD", $borderColor="#174A87")
    UpdateElementStyle(gestorSync, $bgColor="#1F5FAD", $borderColor="#174A87")
    UpdateElementStyle(repoLocal, $bgColor="#1F5FAD", $borderColor="#174A87")
    UpdateElementStyle(clienteApi, $bgColor="#1F5FAD", $borderColor="#174A87")
    UpdateLayoutConfig($c4ShapeInRow="2", $c4BoundaryInRow="1")
```

### Catalogo de la Vista de Componentes
|Componente| Tecnología| Responsabilidad| 
|---|---|---|
|Controladores REST| FastAPI Routers| Expone los endpoints HTTPS, procesa el cuerpo JSON de las solicitudes y retorna respuestas.|
|Módulo de Autenticación| JWT / Security Middleware| Valida la identidad del usuario y protege las rutas de la API.|
|Servicio de Gestión de Stock| Python| Ejecuta la lógica del módulo de Stock (RF01–RF04): alertas de stock crítico y bajas.|
|Servicio de Bitácora| Python| Administra el historial de notas de campo (RF05–RF06) y el versionado de entradas.|
|Motor de Resolución de Conflictos| Python| Detecta colisiones de fechas/versiones entre el cliente y el servidor (EC-03).|
|Capa de Acceso a Datos| SQLAlchemy ORM| Encapsula el acceso a la Base de Datos Central con soporte de transacciones atómicas.|
|Publicador de Eventos| Redis Client| Envía mensajes asincrónicos hacia la Cola de Tareas cuando se requieren procesamientos diferidos.|

#### Catálogo de componentes de la Aplicación móvil

| Componente | Tecnología | Responsabilidad | Origen (trazabilidad) |
|---|---|---|---|
| Vistas de stock y bitácora | Componentes React | Mostrar formularios, listados y alertas; capturar las acciones del usuario. | RF01–RF06 |
| Modelos de vista de stock y bitácora | Estado React | Validar lotes y notas, calcular la alerta de stock bajo, ordenar las notas y exponer el estado a las Vistas. | RF01–RF06 |
| Repositorio local | JavaScript | Encapsular el acceso al Almacén local y marcar cada cambio como "pendiente_sync". | DA-01 (EC-01) |
| Cifrado local | Web Crypto API (AES) | Aspecto transversal: cifrar los datos sensibles en reposo. | EC-04 |
| Gestor de sincronización | Service Worker / Background Sync | Enviar los cambios pendientes en lotes acotados, en segundo plano, y reintentar si falla la red. | DA-02 (EC-02) |
| Cliente de la API | fetch + JWT | Aspecto transversal de autenticación del lado cliente: adjuntar el token y comunicarse por HTTPS. | EC-04 |

#### Catálogo de relaciones de la Aplicación móvil

| Origen | Destino | Qué se comunica | Tipo | Protocolo |
|---|---|---|---|---|
| Jardinero / Usuario | Vistas de stock y bitácora | Uso de la interfaz | Persona hacia componente | HTTPS |
| Vistas de stock y bitácora | Modelos de vista de stock y bitácora | Enlace de datos y acciones del usuario | Llamada interna | — |
| Modelos de vista de stock y bitácora | Repositorio local | Lectura y guardado de lotes y notas | Llamada interna | — |
| Repositorio local | Cifrado local | Cifrado y descifrado de datos sensibles | Llamada interna | — |
| Repositorio local | Almacén local | Lectura y escritura | Acceso a datos | IndexedDB API |
| Gestor de sincronización | Repositorio local | Lectura de pendientes y actualización de estado | Llamada interna | — |
| Gestor de sincronización | Cliente de la API | Envío de lotes y consulta de estado | Llamada interna | — |
| Cliente de la API | API de sincronización | Lotes de cambios, descarga de datos y estado de lotes | Síncrona | JSON sobre HTTPS |


### 2. Componentes de la API de sincronización

Patrón: **Capas** (presentación → servicios → acceso a datos). Aspecto transversal: autenticación y autorización.

Las escrituras del usuario no se aplican en la API: llegan como lotes de cambios y se encolan (DA-02). La API solo lee datos consolidados y registra el estado de cada lote recibido.

```mermaid
%%{init: {"wrap": true}}%%
C4Component
    title Vista de Componentes - API de sincronización

    Container(app, "Aplicación móvil", "PWA / React")

    Container_Boundary(apiBoundary, "API de sincronización") {
        Component(controladores, "Controladores REST", "Routers FastAPI", "Presentación: reciben solicitudes HTTPS y responden JSON.")
        Component(auth, "Autenticación y autorización", "Middleware JWT", "Transversal: valida el token y el acceso a datos propios.")
        Component(servConsultas, "Servicio de consultas de stock y bitácora", "Python", "Servicios: entrega lotes, catálogo y notas consolidados.")
        Component(receptor, "Receptor de sincronización", "Python", "Servicios: valida formato y versiones del lote, lo registra y lo encola.")
        Component(accesoDatos, "Acceso a datos", "SQLAlchemy", "Datos: consultas sobre la base central.")
        Component(publicador, "Publicador de lotes", "Cliente Redis", "Datos: publica los lotes en la cola.")
    }

    Boundary(vecinos, "Contenedores vecinos") {
        ContainerDb(dbCentral, "Base de datos central", "PostgreSQL")
        ContainerQueue(colaSync, "Cola de sincronización", "Redis")
    }

    Rel(app, controladores, "Envía lotes y solicita datos", "JSON/HTTPS")
    Rel(controladores, auth, "Verifica token")
    Rel(controladores, servConsultas, "Invoca consultas")
    Rel(controladores, receptor, "Entrega lote")
    Rel(servConsultas, accesoDatos, "Lee datos")
    Rel(receptor, accesoDatos, "Registra y consulta estado")
    Rel(receptor, publicador, "Encola lote validado")
    Rel(accesoDatos, dbCentral, "Lee y escribe", "SQL")
    Rel(publicador, colaSync, "Publica lote", "Redis")

    UpdateRelStyle(app, controladores, $textColor="#F59E0B", $lineColor="#F59E0B", $offsetY="-50")
    UpdateRelStyle(controladores, auth, $textColor="#F59E0B", $lineColor="#F59E0B", $offsetX="-25")
    UpdateRelStyle(controladores, servConsultas, $textColor="#F59E0B", $lineColor="#F59E0B")
    UpdateRelStyle(controladores, receptor, $textColor="#F59E0B", $lineColor="#F59E0B")
    UpdateRelStyle(servConsultas, accesoDatos, $textColor="#F59E0B", $lineColor="#F59E0B")
    UpdateRelStyle(receptor, accesoDatos, $textColor="#F59E0B", $lineColor="#F59E0B")
    UpdateRelStyle(receptor, publicador, $textColor="#F59E0B", $lineColor="#F59E0B")
    UpdateRelStyle(accesoDatos, dbCentral, $textColor="#F59E0B", $lineColor="#F59E0B")
    UpdateRelStyle(publicador, colaSync, $textColor="#F59E0B", $lineColor="#F59E0B")
    UpdateElementStyle(controladores, $bgColor="#1F5FAD", $borderColor="#174A87")
    UpdateElementStyle(auth, $bgColor="#1F5FAD", $borderColor="#174A87")
    UpdateElementStyle(servConsultas, $bgColor="#1F5FAD", $borderColor="#174A87")
    UpdateElementStyle(receptor, $bgColor="#1F5FAD", $borderColor="#174A87")
    UpdateElementStyle(accesoDatos, $bgColor="#1F5FAD", $borderColor="#174A87")
    UpdateElementStyle(publicador, $bgColor="#1F5FAD", $borderColor="#174A87")
    UpdateLayoutConfig($c4ShapeInRow="2", $c4BoundaryInRow="1")
```

**Comprobación del patrón Capas (Tabla 6):** todas las flechas entre capas van hacia abajo (Controladores → Servicios → Acceso a datos / Publicador). Ninguna capa inferior llama a una superior y no se saltean capas: los Controladores no acceden directamente a los datos. La autenticación es un aspecto transversal que usan los Controladores.

#### Catálogo de componentes de la API de sincronización

| Componente | Tecnología | Responsabilidad | Origen (trazabilidad) |
|---|---|---|---|
| Controladores REST | Routers FastAPI | Exponer los endpoints HTTPS; recibir lotes y solicitudes de datos; responder "202 Aceptado" al encolar. | DA-03 |
| Autenticación y autorización | Middleware JWT | Validar la identidad del usuario y restringir el acceso a sus propios datos. | EC-04 |
| Servicio de consultas de stock y bitácora | Python | Entregar al dispositivo los lotes, el catálogo y el historial de notas consolidados. | RF01–RF06 |
| Receptor de sincronización | Python | Validar formato y versiones de cada lote, registrarlo como "recibido" y encolarlo; informar su estado. | DA-02 (EC-02, EC-03) |
| Acceso a datos | SQLAlchemy | Encapsular las consultas sobre la Base de datos central. | DA-03 (EC-05) |
| Publicador de lotes | Cliente Redis | Publicar los lotes validados en la Cola de sincronización. | DA-02 (EC-02) |

#### Catálogo de relaciones de la API de sincronización

| Origen | Destino | Qué se comunica | Tipo | Protocolo |
|---|---|---|---|---|
| Aplicación móvil | Controladores REST | Lotes de cambios y solicitudes de datos | Síncrona | JSON sobre HTTPS |
| Controladores REST | Autenticación y autorización | Verificación de token y permisos | Llamada interna | — |
| Controladores REST | Servicio de consultas de stock y bitácora | Consultas de datos consolidados | Llamada interna | — |
| Controladores REST | Receptor de sincronización | Lote de cambios recibido | Llamada interna | — |
| Servicio de consultas de stock y bitácora | Acceso a datos | Lectura de lotes, catálogo y notas | Llamada interna | — |
| Receptor de sincronización | Acceso a datos | Registro y consulta del estado del lote | Llamada interna | — |
| Receptor de sincronización | Publicador de lotes | Lote validado para encolar | Llamada interna | — |
| Acceso a datos | Base de datos central | Consultas y escrituras | Acceso a datos | SQL |
| Publicador de lotes | Cola de sincronización | Publicación del lote | Asincrónica | Protocolo Redis |


### 3. Componentes del Procesador de sincronización

Patrón: **Broker** (lado consumidor). Aspectos transversales: gestión de excepciones con reintento y notificaciones. Aquí se aplican las tácticas de rollback, transacciones y versionado de EC-03 y EC-04.

```mermaid
%%{init: {"wrap": true}}%%
C4Component
    title Vista de Componentes - Procesador de sincronización

    ContainerQueue(colaSync, "Cola de sincronización", "Redis")

    Container_Boundary(procBoundary, "Procesador de sincronización") {
        Component(consumidor, "Consumidor de lotes", "RQ worker", "Toma cada lote y confirma al terminar.")
        Component(excepciones, "Manejo de excepciones", "Python", "Transversal: reintenta y registra lotes fallidos.")
        Component(motorConflictos, "Motor de resolución de conflictos", "Python", "Compara versiones y separa los conflictos para revisión.")
        Component(aplicador, "Aplicador de cambios", "Python", "Aplica reglas de lotes y notas; detecta stock bajo.")
        Component(accesoTx, "Acceso a datos transaccional", "SQLAlchemy", "Una transacción por lote: todo o nada.")
        Component(notificador, "Notificador", "Python", "Transversal: pide alertas push.")
    }

    Boundary(vecinos, "Contenedores y sistemas vecinos") {
        ContainerDb(dbCentral, "Base de datos central", "PostgreSQL")
        System_Ext(servicioNotif, "Servicio de Notificaciones Push", "Alertas móviles")
    }

    Rel(consumidor, colaSync, "Consume y confirma lotes", "Redis")
    Rel(consumidor, excepciones, "Delega fallos")
    Rel(consumidor, motorConflictos, "Entrega lote")
    Rel(motorConflictos, aplicador, "Pasa cambios sin conflicto")
    Rel(motorConflictos, accesoTx, "Lee versiones y registra conflictos")
    Rel(motorConflictos, notificador, "Pide aviso de conflicto")
    Rel(aplicador, accesoTx, "Escribe cambios")
    Rel(aplicador, notificador, "Pide alerta de stock bajo")
    Rel(accesoTx, dbCentral, "Lee y escribe", "SQL")
    Rel(notificador, servicioNotif, "Envía alerta", "HTTPS")

    UpdateRelStyle(consumidor, colaSync, $textColor="#F59E0B", $lineColor="#F59E0B", $offsetY="-50")
    UpdateRelStyle(consumidor, excepciones, $textColor="#F59E0B", $lineColor="#F59E0B", $offsetX="-12")
    UpdateRelStyle(consumidor, motorConflictos, $textColor="#F59E0B", $lineColor="#F59E0B")
    UpdateRelStyle(motorConflictos, aplicador, $textColor="#F59E0B", $lineColor="#F59E0B", $offsetY="-105")
    UpdateRelStyle(motorConflictos, accesoTx, $textColor="#F59E0B", $lineColor="#F59E0B", $offsetX="-60")
    UpdateRelStyle(motorConflictos, notificador, $textColor="#F59E0B", $lineColor="#F59E0B", $offsetY="-25")
    UpdateRelStyle(aplicador, accesoTx, $textColor="#F59E0B", $lineColor="#F59E0B", $offsetY="30")
    UpdateRelStyle(aplicador, notificador, $textColor="#F59E0B", $lineColor="#F59E0B")
    UpdateRelStyle(accesoTx, dbCentral, $textColor="#F59E0B", $lineColor="#F59E0B")
    UpdateRelStyle(notificador, servicioNotif, $textColor="#F59E0B", $lineColor="#F59E0B")
    UpdateElementStyle(consumidor, $bgColor="#1F5FAD", $borderColor="#174A87")
    UpdateElementStyle(excepciones, $bgColor="#1F5FAD", $borderColor="#174A87")
    UpdateElementStyle(motorConflictos, $bgColor="#1F5FAD", $borderColor="#174A87")
    UpdateElementStyle(aplicador, $bgColor="#1F5FAD", $borderColor="#174A87")
    UpdateElementStyle(accesoTx, $bgColor="#1F5FAD", $borderColor="#174A87")
    UpdateElementStyle(notificador, $bgColor="#1F5FAD", $borderColor="#174A87")
    UpdateLayoutConfig($c4ShapeInRow="2", $c4BoundaryInRow="1")
```

**Comprobación del patrón Broker (Tabla 6):** el Consumidor de lotes se conecta solo a la Cola de sincronización, nunca a la API. Los mensajes tienen formato definido (lote JSON con usuario, entidad, operación, versión y marca de tiempo). La entrega es "al menos una vez": el lote se elimina de la cola recién cuando el Consumidor confirma; por eso el procesamiento es idempotente (aplicar dos veces el mismo lote no duplica datos, gracias al identificador y la versión de cada cambio).

#### Catálogo de componentes del Procesador de sincronización

| Componente | Tecnología | Responsabilidad | Origen (trazabilidad) |
|---|---|---|---|
| Consumidor de lotes | RQ worker | Tomar lotes de la cola y confirmar al terminar. | DA-02 (EC-02) |
| Manejo de excepciones | Python | Aspecto transversal: reintentar hasta 3 veces y registrar como fallido el lote que no se pudo aplicar, sin perderlo. | EC-03 |
| Motor de resolución de conflictos | Python | Detectar divergencias de versión entre lo cargado offline y lo guardado, y registrarlas para revisión. | EC-03 |
| Aplicador de cambios | Python | Aplicar reglas de negocio de lotes (RF01–RF04) y notas (RF05–RF06); detectar stock bajo (RF03). | RF01–RF06 |
| Acceso a datos transaccional | SQLAlchemy | Ejecutar cada lote en una única transacción con rollback completo ante error; mantener versión y last_modified. | EC-03, EC-04 |
| Notificador | Python | Aspecto transversal: pedir al servicio externo las alertas de stock bajo y de conflictos. | RF03, EC-03 |

#### Catálogo de relaciones del Procesador de sincronización

| Origen | Destino | Qué se comunica | Tipo | Protocolo |
|---|---|---|---|---|
| Consumidor de lotes | Cola de sincronización | Toma y confirmación de lotes | Asincrónica | Protocolo Redis |
| Consumidor de lotes | Manejo de excepciones | Fallos durante el procesamiento | Llamada interna | — |
| Consumidor de lotes | Motor de resolución de conflictos | Lote a procesar | Llamada interna | — |
| Motor de resolución de conflictos | Acceso a datos transaccional | Lectura de versiones y registro de conflictos | Llamada interna | — |
| Motor de resolución de conflictos | Aplicador de cambios | Cambios sin conflicto | Llamada interna | — |
| Motor de resolución de conflictos / Aplicador de cambios | Notificador | Pedido de aviso de conflicto o de stock bajo | Llamada interna | — |
| Aplicador de cambios | Acceso a datos transaccional | Escritura de cambios | Llamada interna | — |
| Acceso a datos transaccional | Base de datos central | Consultas y escrituras en transacción | Acceso a datos | SQL |
| Notificador | Servicio de Notificaciones Push | Alertas | Integración externa | HTTPS |


## Recorrido de Historias de Usuario sobre las Vistas

Para cada historia de usuario se indica por qué contenedores y componentes pasa cada paso de su criterio de aceptación (Given-When-Then).

| Historia de usuario | Paso del criterio de aceptación | Contenedores | Componentes |
|---|---|---|---|
| `HU-02` Registrar un nuevo lote de semillas (offline) | **Given** el jardinero está en el campo sin conexión y abre el formulario de lote | Aplicación móvil | Vistas de stock y bitácora |
| | **When** completa cantidad y año de cosecha y presiona "Guardar" | Aplicación móvil → Almacén local | Vistas → Modelos de vista de stock y bitácora (validan) → Repositorio local → Cifrado local; el cambio queda como "pendiente_sync" |
| | **Then** la interfaz confirma el guardado en menos de 1 segundo, sin usar la red | Aplicación móvil | Modelos de vista de stock y bitácora → Vistas |
| `HU-08.B1` Sincronización diferida de notas de bitácora | **Given** se restableció la conexión y hay 5 notas pendientes en el Almacén local | Aplicación móvil → Almacén local | Gestor de sincronización → Repositorio local (lee pendientes) |
| | **When** se activa la sincronización en segundo plano: el lote se envía y se encola | Aplicación móvil → API de sincronización → Cola de sincronización | Gestor de sincronización → Cliente de la API → Controladores REST → Autenticación y autorización → Receptor de sincronización → Publicador de lotes. La API responde "202 Aceptado" y la nota pasa a "en_proceso" |
| | **When** el lote se procesa | Cola de sincronización → Procesador de sincronización → Base de datos central | Consumidor de lotes → Motor de resolución de conflictos → Aplicador de cambios → Acceso a datos transaccional (una transacción) |
| | **Then** el usuario ve las notas como "sincronizado" | Aplicación móvil → API de sincronización → Base de datos central | Gestor de sincronización → Cliente de la API → Controladores REST → Receptor de sincronización (consulta estado) → Acceso a datos; Repositorio local actualiza el estado |
| `HU-xx` *(completar con el resto de las HU del SRS que implementan Stock y Bitácora)* | Given / When / Then de su criterio de aceptación | … | … |


## Recorrido de Historias de Usuario sobre las Vistas

Se demuestra el recorrido de dos Historias de Usuario clave del TP1 a través de la arquitectura definida (pasos Given-When-Then):

**HU-02: Registrar un nuevo lote de semillas (en modo offline)**
* Given (Dado que): El jardinero se encuentra en el campo sin conexión a internet y abre el formulario de lote.
* When (Cuando): Completa la cantidad y el año de cosecha y presiona "Guardar":
    * La Aplicación PWA valida los campos en el componente local.
    * La PWA escribe la transacción en el Almacén Local (IndexedDB) de forma síncrona.
    * La entrada queda marcada con estado "pendiente_sync".
* Then (Entonces): La UI confirma el guardado al usuario en $<1\text{ segundo}$, sin requerir llamadas de red.

**HU-08.B1: Sincronización diferida de notas de bitácora**
* Given (Dado que): La PWA detecta que se restableció la conexión a internet y existen 5 notas pendientes en el Almacén Local.
* When (Cuando): El proceso de sincronización en segundo plano se activa:
    * La PWA envía un lote HTTPS REST a los Controladores REST de la API.
    * Los Controladores invocan al Módulo de Autenticación para validar la sesión.
    * El Servicio de Bitácora pasa las notas al Motor de Resolución de Conflictos.
    * La Capa de Acceso a Datos abre una transacción SQL en la Base de Datos Central.
* Then (Entonces): La API responde 200 OK, la PWA actualiza el estado local a "sincronizado" y el usuario ve reflejado el estado en su pantalla.


## Desiciones de arquitectura (ADR/DA)

**DA-01 — Adopción de Arquitectura Local-First (PWA) para Persistencia Offline**
* Escenario que la motiva: EC-01 (Disponibilidad / Operación sin red en el campo).
* Contexto: El usuario opera en la huerta donde la señal 4G/Wi-Fi es nula o intermitente. Guardar datos no puede depender del servidor.
* Decisión:
    * Tácticas: Degradación controlada y Manejo de excepciones.
    * Estilo: Cliente-Servidor Desacoplado con almacén local en el cliente (Local-First).
    * Patrón: Repository Pattern en el cliente PWA sobre IndexedDB.
* Alternativas consideradas:
    * Aplicación Web Síncrona Tradicional: Descartada porque se bloquea totalmente al perder señal en el campo.
    * Desarrollo Nativo Móvil (Android/iOS): Descartado por costos y tiempo de desarrollo del equipo universitario.
* Consecuencias:
    * A favor: Garantiza el $100\%$ de disponibilidad para lecturas y escrituras en el jardín.
    * En contra: Requiere programar lógica de almacenamiento y sincronización duplicada en el cliente y servidor.
* Elementos afectados: Contenedores Aplicación PWA y Almacén Local.


**DA-02 — Desacoplamiento de la Sincronización mediante Cola de Tareas**
* Escenario que la motiva: EC-02 (Desempeño / Sincronización masiva en dispositivos de gama baja).
* Contexto: Al recuperar red tras días offline, la PWA puede enviar decenas de registros acumulados. Sincronizarlos de forma síncrona puede congelar la UI.
* Decisión:
    * Tácticas: Introducir concurrencia y Acotar colas.
    * Estilo: Orientado a Eventos / Procesamiento Asincrónico.
    * Patrón: Broker (Cola de mensajes con Redis).
* Alternativas consideradas:
    * Procesamiento Síncrono en el Endpoint HTTP: Descartado porque causa timeouts de red y congela la aplicación móvil.
* Consecuencias:
    * A favor: La PWA recupera el control de inmediato; la API responde rápido al usuario.
    * En contra: Se suma un contenedor de cola (Redis) a la infraestructura operativa.
* Elementos afectados: Contenedores API Backend y Cola de Tareas.


**DA-03 — Arquitectura en Capas en el Backend para Mantenibilidad Modular**
* Escenario que la motiva: EC-05 (Mantenibilidad / Incorporación modular de Calendario y Clima).
* Contexto: El proyecto utiliza un ciclo iterativo y sumará nuevos módulos en el futuro sin reescribir Stock o Bitácora.
* Decisión:
    * Tácticas: Encapsular y Restringir dependencias.
    * Estilo: Cliente-Servidor; Patrón: Capas (o Hexagonal) en la API Backend.
* Alternativas consideradas:
    * Arquitectura de Microservicios: Descartada por complejidad operativa excesiva para un equipo acotado.
* Consecuencias:
    * A favor: Permite agregar el módulo de Clima o Calendario agregando nuevos servicios/adaptadores sin modificar el código de Stock.
    * En contra: Agrega clases/interfaces intermedias (indirección).
* Elementos afectados: Componentes internos de la API Backend



## Trazabilidad 
|Escenario (TP2)| Atributo (ISO)| Tácticas Aplicadas| Estilo / Patrón| Decisión de Arquitectura| Elementos C4 Afectados|
|---|---|---|---|---|---|
|EC-01| Fiabilidad (3.1)| Degradación controlada| Local-First / Repository Local| DA-01| Contenedores: Aplicación PWA, Almacén Local.|
|EC-02| Eficiencia (1.2)| Concurrencia, acotar colas| Orientada a eventos / Broker| DA-02| Contenedores: API Backend, Cola de Tareas|
|EC-03| Fiabilidad (3.2)| Rollback, versionado| Repositorio / Transacciones| DA-01 / DA-02| Componente: Motor de Resolución de Conflictos.|
|EC-04| Seguridad (4.1)| Cifrado, transacciones| Capas / Cifrado reposo| DA-01 / DA-03| Componentes: Módulo Auth, Acceso a Datos.|
|EC-05| Mantenibilidad (5.1)| Encapsular, intermediario| Capas / Hexagonal| DA-03| Componentes: Servicios de Negocio (Stock/Bitácora).|