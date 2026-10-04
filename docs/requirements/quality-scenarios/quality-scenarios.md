# Escenarios de Atributo de Calidad — Asistente de Huerta

**Taxonomía utilizada:** ISO/IEC 25010:2023, modelo de calidad del producto (Anexo A de la guía de TP2).

**Atributos seleccionados:** 2 (Eficiencia de desempeño), 4 (Capacidad de interacción), 5 (Fiabilidad), 6 (Seguridad de la información), 7 (Mantenibilidad).

**Supuesto declarado y cerrado:** el prototipo es de **uso personal**. Lo utiliza una única persona (el técnico jardinero / usuario general), que es dueña de sus datos, su stock y su bitácora. **No hay varios roles operando sobre los mismos datos**, y no hay escenarios de permisos cruzados entre usuarios. Los roles `admin` / `usuario` definidos en TP1 quedan como distinción técnica interna, pero en la práctica los ejerce la misma persona.

---

## 0. Justificación de la selección

El sistema es una herramienta de uso operativo diario para una persona que gestiona su propia huerta, hoy resuelta en papel o Excel, usada mayormente en el campo con conectividad intermitente, y desarrollada bajo un ciclo de vida iterativo-incremental que dejó fuera de alcance las integraciones externas para este incremento.

- **Capacidad de interacción** y **Fiabilidad** son imprescindibles porque son la razón de ser de RNF01 (usabilidad/responsive) y RNF02 (persistencia offline) ya definidos en el SRS.
- **Seguridad de la información** se vuelve crítica porque, aunque el uso sea personal, hay datos que no deben perderse ni quedar expuestos: la bitácora y el stock son el registro de años de trabajo, y el dispositivo puede perderse o ser accedido por terceros.
- **Mantenibilidad** es crítica porque se eligió el ciclo iterativo-incremental y se decidió postergar Calendario y Clima — el sistema tiene que poder crecer sin reescribirse.
- **Eficiencia de desempeño** se incluye por las condiciones reales de uso en campo (red lenta, historial que crece con los años, dispositivo móvil de gama media o baja).

Quedan afuera **Adecuación funcional** (sus escenarios se superponen con las pruebas de aceptación de los RF de TP1 y no arrastran decisiones de diseño propias) y **Compatibilidad** (no hay ningún sistema externo en el alcance de este incremento; se vuelve relevante recién con la integración a Calendario). **Escalabilidad y Capacidad** (subcaracterísticas de Flexibilidad y Eficiencia) tampoco son prioritarias: es una herramienta de un solo usuario, sin concurrencia.

---

## 1. Eficiencia de desempeño

### 1.1 — Comportamiento temporal

- **Estímulo:** el usuario abre la bitácora, con varios años de entradas acumuladas, y filtra por especie, mientras tiene una conexión de red lenta o intermitente.
- **Fuente del estímulo:** usuario, trabajando en el campo.
- **Artefacto:** módulo de Bitácora (consulta y filtrado del historial).
- **Entorno:** degradado — red lenta/intermitente y volumen de historial acumulado.
- **Respuesta:** el sistema resuelve el filtrado contra los datos ya disponibles localmente, sin bloquear la interfaz a la espera de la red.
- **Medida de la respuesta:** el filtrado sobre el historial local responde en menos de 2 segundos, independientemente del estado de la conexión.
- **Justificación de criticidad:** la bitácora es la herramienta de trabajo diario en el campo. Si consultarla se vuelve lenta o se traba con mala señal, el usuario vuelve al papel o Excel que el sistema busca reemplazar.


### 1.2 — Utilización de recursos

- **Estímulo:** el sistema tiene que sincronizar un lote grande de registros pendientes (varios días de carga offline acumulada) apenas se recupera la conexión, en un dispositivo móvil de gama baja.
- **Fuente del estímulo:** reconexión a la red tras un período prolongado offline.
- **Artefacto:** proceso de sincronización en segundo plano.
- **Entorno:** degradado — dispositivo de recursos limitados, volumen de sincronización acumulado.
- **Respuesta:** la sincronización se ejecuta en segundo plano por lotes pequeños, sin consumir memoria o batería al punto de volver la aplicación inutilizable mientras se sincroniza.
- **Medida de la respuesta:** la aplicación permanece usable (tiempos de respuesta a la interacción del usuario por debajo de 1 segundo) durante todo el proceso de sincronización, en un dispositivo de gama baja de referencia.
- **Justificación de criticidad:** el usuario accede desde su propio dispositivo, que puede ser de gama media o baja; si sincronizar bloquea el teléfono, la app se percibe como "se cuelga" y se deja de usar.

### 1.3 — Capacidad

- **Estímulo:** el volumen acumulado de entradas de bitácora y lotes de semillas crece de forma sostenida a lo largo de varias temporadas de cultivo (años de uso continuo por parte del mismo usuario).
- **Fuente del estímulo:** uso continuo del sistema a través del tiempo.
- **Artefacto:** capa de almacenamiento y motor de consulta de los módulos de Bitácora y Stock.
- **Entorno:** significativo — volumen de datos que crece sin límite definido de antemano.
- **Respuesta:** el sistema mantiene tiempos de consulta y filtrado estables a medida que el historial crece, sin degradación perceptible para el usuario.
- **Medida de la respuesta:** el tiempo de respuesta de una consulta filtrada no aumenta más de un 10% al pasar de 1 a 5 años de historial acumulado.
- **Justificación de criticidad:** el sistema está pensado para reemplazar años de registros en papel/Excel — si el rendimiento se degrada justo cuando más historial acumula, deja de ser viable en el momento en que más valor debería aportar.

---

## 2. Capacidad de interacción

### 2.1 — Capacidad de aprendizaje

- **Estímulo:** el usuario, sin capacitación previa ni experiencia con aplicaciones similares, intenta registrar su primer lote de semillas.
- **Fuente del estímulo:** usuario, primera interacción con el sistema.
- **Artefacto:** flujo de "Cargar nuevo lote" (CU01).
- **Entorno:** degradado — sin manual, sin capacitación previa, primer uso.
- **Respuesta:** el sistema guía el flujo con etiquetas en el lenguaje del dominio (no jerga técnica) y valida cada campo en línea, explicando el motivo del error cuando corresponde.
- **Medida de la respuesta:** al menos el 90% de los usuarios nuevos completan el alta de un lote en menos de 3 minutos sin asistencia externa.
- **Justificación de criticidad:** el usuario hoy administra su cultivo en papel o Excel. La barrera real de adopción es aprender a usar la herramienta — si el primer uso frustra, vuelve a su método anterior.

### 2.2 — Protección frente a errores del usuario

- **Estímulo:** el usuario ingresa una cantidad inicial negativa o un año de recolección posterior al actual al cargar un lote (flujos A1/A2 ya identificados en CU01).
- **Fuente del estímulo:** usuario, error de tipeo o de criterio al cargar datos.
- **Artefacto:** formulario de alta de lote (RF01).
- **Entorno:** degradado — entrada de datos inválida antes de confirmar.
- **Respuesta:** el sistema detecta el valor inválido en el momento de la carga (no después de guardar) y explica en lenguaje simple por qué no puede continuar, sin perder el resto de los datos ya ingresados.
- **Medida de la respuesta:** el 100% de los valores fuera de rango se detectan antes de confirmar el registro, y el usuario no pierde los demás campos ya completados al corregir el error.
- **Justificación de criticidad:** prevenir el error en el momento evita que datos incorrectos lleguen a afectar el stock real, y evita la frustración de recargar todo el formulario por un solo campo mal ingresado.

### 2.3 — Asistencia al usuario

- **Estímulo:** una entrada de bitácora cargada offline no logra sincronizarse automáticamente por un conflicto con otra edición del mismo registro (por ejemplo, el mismo usuario editó la entrada desde dos dispositivos distintos).
- **Fuente del estímulo:** conflicto de sincronización detectado tras la reconexión.
- **Artefacto:** interfaz de notificaciones/resolución de conflictos.
- **Entorno:** degradado — error no resuelto automáticamente, usuario sin conocimiento técnico para diagnosticarlo.
- **Respuesta:** el sistema explica, en lenguaje simple, qué pasó y qué opciones tiene el usuario (conservar su versión, descartarla, revisar ambas), sin requerir que contacte a soporte técnico.
- **Medida de la respuesta:** el 90% de los conflictos de sincronización se resuelven sin ayuda externa, en menos de 2 minutos.
- **Justificación de criticidad:** dado que el sistema asume trabajo offline con sincronización posterior (RNF02), los conflictos van a ocurrir — si el usuario no entiende qué pasó ni qué hacer, pierde confianza en la herramienta.

---

## 3. Fiabilidad

### 3.1 — Disponibilidad

- **Estímulo:** el usuario pierde la conexión a internet mientras carga una nueva entrada de bitácora en el campo.
- **Fuente del estímulo:** pérdida de conectividad (condición de red).
- **Artefacto:** módulo de Bitácora + capa de almacenamiento local.
- **Entorno:** degradado — sin conexión a internet.
- **Respuesta:** el sistema permite completar y guardar la entrada localmente sin interrumpir el flujo del usuario, marcándola como pendiente de sincronización.
- **Medida de la respuesta:** el 100% de las cargas iniciadas sin conexión se completan exitosamente en el dispositivo y quedan visibles como "pendientes de sincronizar" hasta recuperar la red.
- **Justificación de criticidad:** la conectividad intermitente en el campo es la condición de uso normal del usuario, no una excepción rara — es la razón de ser de RNF02.


### 3.2 — Capacidad de recuperación

- **Estímulo:** el usuario editó la misma entrada de bitácora desde dos dispositivos distintos sin conexión (por ejemplo, celular y tablet), y al reconectar ambas versiones entran en conflicto.
- **Fuente del estímulo:** sincronización simultánea de versiones divergentes del mismo dato, originadas por el mismo usuario.
- **Artefacto:** proceso de sincronización del módulo de Bitácora.
- **Entorno:** degradado — conflicto de datos tras reconexión.
- **Respuesta:** el sistema conserva ambas versiones y las marca para revisión, en lugar de sobrescribir silenciosamente una con la otra.
- **Medida de la respuesta:** el 0% de los conflictos de sincronización resulta en pérdida silenciosa de datos; el 100% queda visible para que el usuario decida.
- **Justificación de criticidad:** perder una observación de campo sin aviso destruye la confianza en el sistema como registro confiable del cultivo, que es su propósito central.

### 3.3 — Tolerancia a fallos

- **Estímulo:** la aplicación se cierra inesperadamente (batería, error del sistema operativo) mientras el usuario está completando una entrada de bitácora a mitad de camino.
- **Fuente del estímulo:** falla del dispositivo o del sistema operativo.
- **Artefacto:** formulario de carga de entrada, en edición.
- **Entorno:** degradado — cierre abrupto de la aplicación.
- **Respuesta:** al reabrir la app, el sistema recupera el borrador de la entrada que estaba completando, sin pérdida de los datos ya ingresados.
- **Medida de la respuesta:** el 100% de las entradas en progreso se recuperan intactas tras un cierre inesperado, siempre que se haya completado al menos un campo.
- **Justificación de criticidad:** perder una entrada a mitad de completar, después de horas de trabajo de campo, desalienta directamente el uso del sistema por el costo de tener que reintentar todo.

---

## 4. Seguridad de la información

### 4.1 — Confidencialidad

- **Estímulo:** el usuario pierde el dispositivo con la aplicación instalada y los datos de bitácora y stock ya sincronizados.
- **Fuente del estímulo:** pérdida o robo del dispositivo.
- **Artefacto:** base de datos local del dispositivo + backend de sincronización.
- **Entorno:** degradado — acceso físico al dispositivo por parte de un tercero no autorizado.
- **Respuesta:** los datos almacenados localmente están cifrados en reposo y la aplicación requiere autenticación para abrirse; sin credenciales, la información no es legible.
- **Medida de la respuesta:** sin las credenciales del usuario, el 100% de los datos personales (bitácora, stock, fichas de especie) es inaccesible tanto en el dispositivo como en el backend.
- **Justificación de criticidad:** la bitácora contiene años de observaciones personales del usuario. Que un tercero pueda leerla tras un robo del dispositivo es un daño irreversible y desproporcionado respecto del valor del equipo.

### 4.2 — Integridad

- **Estímulo:** durante la sincronización entre el dispositivo y el backend, se produce un corte de red en medio de la transferencia de un lote de entradas de bitácora.
- **Fuente del estímulo:** interrupción de red a mitad de una operación de escritura.
- **Artefacto:** proceso de sincronización y base de datos (local y remota).
- **Entorno:** degradado — transferencia incompleta.
- **Respuesta:** el sistema detecta la transferencia incompleta y la revierte o la reintenta, sin dejar registros parciales ni corromper los ya existentes.
- **Medida de la respuesta:** el 100% de las sincronizaciones interrumpidas deja la base de datos en un estado consistente (o se completa íntegra, o no se aplica).
- **Justificación de criticidad:** un registro a medias o una entrada corrupta en la bitácora es peor que una entrada faltante, porque el usuario no puede distinguir el dato válido del inválido y pierde la confianza en todo el historial.

### 4.3 — Autenticidad

- **Estímulo:** se producen múltiples solicitudes de inicio de sesión fallidas y consecutivas sobre la cuenta del usuario, desde distintos orígenes, en un lapso corto de tiempo.
- **Fuente del estímulo:** intento de acceso no autorizado (posible ataque automatizado).
- **Artefacto:** módulo de autenticación.
- **Entorno:** degradado — patrón de acceso anómalo.
- **Respuesta:** el sistema bloquea temporalmente los intentos tras un número definido de fallos consecutivos y notifica al titular de la cuenta.
- **Medida de la respuesta:** el acceso se bloquea automáticamente después de 5 intentos fallidos en menos de 1 minuto, y se libera solo mediante un mecanismo de verificación adicional.
- **Justificación de criticidad:** aunque el uso sea personal, la cuenta concentra todos los datos del usuario. Un acceso no autorizado a esa cuenta es equivalente a entregar la bitácora completa, sin necesidad de robar el dispositivo.

---

## 5. Mantenibilidad

### 5.1 — Modularidad

- **Estímulo:** el equipo de desarrollo necesita incorporar, en un incremento posterior, el módulo de integración con CropCalendar y estaciones meteorológicas.
- **Fuente del estímulo:** equipo de desarrollo, durante un incremento futuro del proyecto.
- **Artefacto:** arquitectura general del sistema — separación entre los módulos de Stock, Bitácora y el futuro módulo de Calendario/Clima.
- **Entorno:** significativo — ciclo de vida iterativo-incremental, con alcance no cerrado completamente desde el inicio.
- **Respuesta:** el nuevo módulo se integra comunicándose solo a través de interfaces ya definidas, sin requerir cambios en el código interno de Stock ni de Bitácora.
- **Medida de la respuesta:** cero regresiones en las pruebas existentes de Stock y Bitácora luego de incorporar el nuevo módulo.
- **Justificación de criticidad:** el grupo eligió el ciclo iterativo-incremental porque el alcance no estaba cerrado desde el inicio, y dejó Calendario y Clima explícitamente fuera de este incremento. Sin modularidad, cada incremento futuro arriesga romper lo ya construido.

### 5.2 — Modificabilidad

- **Estímulo:** cambia el criterio de negocio para la alerta de stock crítico: de un umbral fijo global a uno configurable por especie.
- **Fuente del estímulo:** equipo de desarrollo, en respuesta a una decisión de negocio surgida durante el ciclo iterativo.
- **Artefacto:** módulo de Gestión de Stock (lógica de alerta, RF03).
- **Entorno:** significativo — cambio de regla de negocio a mitad de un ciclo iterativo.
- **Respuesta:** el cambio se implementa modificando solo la lógica del umbral, sin tocar el resto de las funciones del módulo de Stock ni otros módulos.
- **Medida de la respuesta:** el cambio se implementa sin introducir regresiones en las pruebas existentes de Stock.
- **Justificación de criticidad:** el ciclo iterativo-incremental asume que las reglas de negocio se van a ir ajustando con la interacción con el usuario — si cada ajuste requiere tocar múltiples módulos, el costo de iterar contradice la elección metodológica de TP1.

### 5.3 — Capacidad de prueba

- **Estímulo:** el equipo necesita verificar que un cambio en el módulo de Bitácora no rompió ninguna de las reglas de validación ya existentes en Stock (RF01–RF04) antes de integrarlo.
- **Fuente del estímulo:** equipo de desarrollo, previo a integrar un cambio.
- **Artefacto:** módulos de Stock y Bitácora.
- **Entorno:** significativo — necesidad de validar un cambio antes de que llegue a producción.
- **Respuesta:** el sistema permite ejecutar un conjunto de pruebas automatizadas sobre las reglas de RF01–RF04 de forma independiente, sin depender de datos de producción ni de intervención manual.
- **Medida de la respuesta:** las pruebas de RF01–RF04 se ejecutan de punta a punta en menos de unos pocos minutos y detectan cualquier regresión antes del despliegue.
- **Justificación de criticidad:** en un proyecto de varios TP con entregas sucesivas, sin capacidad de prueba automatizada cada incremento se vuelve más riesgoso de integrar, y el costo de detectar errores tarde crece con cada entrega.
