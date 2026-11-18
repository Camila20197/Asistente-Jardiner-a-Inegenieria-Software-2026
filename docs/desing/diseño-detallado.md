#Diseño detallado

## Introducción y motivo de la elección
Se elige la *HU-08: Registrar una observación en la bitácora*, acotada a su flujo de captura offline, validación de reglas de negocio y visualización en linea de tiempo local.
La bitácora de campo es la herramienta diaria del jardinero para registrar las observaciones de cultivo en la huerta sin depender de la conectividad. Además, se cumple con las tres condiciones exigidas: asociación directa a escenarios de calidad (EC-01: dispoibilidad offline y EC-04: seguridad en reposo), atraviesa los componentes internos del contenedor *Aplicación móvil* (Vistas de stock y bitacora, Modelos de vista, Repositorio local y Cifrado local) y esta respaldada por la decisión de arquitectura DA-01: Local first con patrón Repository-

Siglas: C4 (Contexto, Contenedor, Componente, Código), CA (Criterio de Aceptación), CP (Caso de Prueba), DA (Decisión de Arquitectura), EC (Escenario de Calidad), GRASP (General Responsibility Assignment Software Patterns), HU (Historia de Usuario), MVVM (Model-View-ViewModel), PWA (Progressive Web App).


## Ficha de la HU
HU-08 (obligatoria) — Registrar una observación en la bitácora (Realiza: RF05, CU02)

Como usuario autenticado, quiero agregar una nota de observación de campo para una especie, para llevar un historial de la evolución de mi cultivo.

Criterios de aceptación (TP1)
CA-01 (Éxito): Given que tengo una especie seleccionada, When cargo una nueva entrada con fecha y notas y la guardo, Then aparece en la línea de tiempo de esa especie.

CA-02 (Rechazo): Given que ingreso datos en un formato inválido, When intento guardar, Then el sistema muestra un error y no guarda la entrada.

### Coherencia con la arquitectura
|Dimensión|Contenido|
|---|---|
|Funcionalidad|HU-08 Registrar observación en bitácora (CU02 / RF05); camino principal de alta offline con actualización de línea de tiempo y caminos de rechazo por datos inválidos o especie inexistente.|
|Estructura|Contenedor: Aplicación móvil (PWA) (patrones: MVVM + Repository Local). Componentes que atraviesa: Vistas de stock y bitácora (Presentación), Modelos de vista de stock y bitácora (Control / Aplicación — principal), Repositorio local (Acceso a datos), Cifrado local (Transversal) y Almacén local (IndexedDB).|
|Calidad| EC-01 (Disponibilidad): 100% de los registros iniciados sin red se almacenan exitosamente en el dispositivo local en $<1\text{ s}$. Táctica: Degradación controlada y operar offline (DA-01). EC-04 (Seguridad): Protección de datos personales en el dispositivo. Táctica: Cifrar datos en reposo (AES).|
|Dominio|Entidades del modelo del TP1 que intervienen: Usuario, Especie y EntradaBitacora (ver tabla abajo).|
|Verificación|Pruebas unitarias en pytest simulando ausencia total de red: se verifica que el guardado local complete en $<1\text{ s}$, marque la entrada como pendiente_sync, la cifre al persistir y la exponga ordenada en la línea de tiempo de la especie.|


### Entidades del Modelo de Dominio
|Entidad de modelo|Interviene|Que usa la HU| La HU la..|Motivo|
|---|---|---|---|---|
|EntradaBitacora|	Sí|	id, usuario_id, especie_id, fecha, nota, estado_sync, version, last_modified.|	Crea y consulta|	Entidad principal: valida las reglas de negocio de fecha y nota, y conforma los ítems de la línea de tiempo de la especie.|
|Especie|	Sí|	id, nombre.|	Consulta|	Verifica que la especie seleccionada exista en el catálogo local antes de asociarle la observación.|
|Usuario|Sí|	id.|	Consulta|	Identifica al autor autenticado de la observación para filtrar su línea de tiempo privada.|
|LoteDeSemilla|	No|	—|	—	|Pertenece al módulo de inventario de semillas (CU01), sin intervención en el registro de observaciones de campo.|
|RolUsuario|	No|	—|	—	|Enumeración descriptiva (admin / usuario) que no altera la lógica de carga de notas en la bitácora.|


flowchart LR
    Actor(["Jardinero / Usuario"])
    Pantalla["PantallaBitacora<br/>&lt;&lt;boundary&gt;&gt;"]
    CtrlBitacora(("ControladorBitacora<br/>&lt;&lt;control&gt;&gt;"))
    RepoEspecie(("RepositorioEspecies<br/>&lt;&lt;control&gt;&gt;"))
    RepoBitacora(("RepositorioBitacora<br/>&lt;&lt;control&gt;&gt;"))
    Cifrado(("ServicioCifrado<br/>&lt;&lt;control&gt;&gt;"))
    Especie[/"Especie<br/>&lt;&lt;entity&gt;&gt;"/]
    Entrada[/"EntradaBitacora<br/>&lt;&lt;entity&gt;&gt;"/]

    Actor --> Pantalla
    Pantalla --> CtrlBitacora
    CtrlBitacora --> RepoEspecie
    RepoEspecie --> Especie
    CtrlBitacora --> Entrada
    CtrlBitacora --> RepoBitacora
    RepoBitacora --> Cifrado
    RepoBitacora --> Entrada