/* Una observación, sin señal.
   A la izquierda, la aplicación: la página le habla a PantallaBitacora (/app/...). A la derecha, el
   mismo recorrido repetido en cámara lenta sobre el diagrama de robustez de la HU-08. Nada se mueve
   solo: todo empieza cuando alguien elige una especie o guarda una observación en el teléfono. */
(() => {
  "use strict";

  const $ = (selector) => document.querySelector(selector);
  const SVG = "http://www.w3.org/2000/svg";
  const QUIETO = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const esperar = (ms) => new Promise((listo) => setTimeout(listo, QUIETO ? 0 : ms));

  async function pedir(url, cuerpo) {
    const opciones = cuerpo === undefined ? {} : {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(cuerpo),
    };
    const respuesta = await fetch(url, opciones);
    let datos = null;
    try { datos = await respuesta.json(); } catch { datos = null; }
    return { ok: respuesta.ok, estado: respuesta.status, datos };
  }

  const hora = (fecha = new Date()) =>
    fecha.toLocaleTimeString("es-AR", { hour: "2-digit", minute: "2-digit", second: "2-digit", hourCycle: "h23" });
  const fechaLarga = (iso) => new Date(`${iso}T12:00:00`).toLocaleDateString("es-AR", {
    day: "numeric", month: "long", year: "numeric" });

  /* ------------------------------------------------- el diagrama de robustez */

  // Debajo (o encima) de cada elemento, el componente del TP3 donde vive. Las entidades son la capa de
  // dominio de «Modelos de vista». El Almacén local no es un elemento de robustez: se dibuja para ver
  // dónde termina el recorrido.
  const NODOS = {
    actor:        { x: 54,  y: 262, tipo: "actor",    titulo: ["Jardinero/a"] },
    pantalla:     { x: 194, y: 262, tipo: "boundary", titulo: ["Pantalla", "Bitacora"], componente: "Vistas", w: 132, h: 70 },
    controlador:  { x: 384, y: 262, tipo: "control",  titulo: ["Controlador", "Bitacora"], componente: "Modelos de vista", r: 62 },
    repoEspecies: { x: 598, y: 112, tipo: "control",  titulo: ["Repositorio", "Especies"], componente: "Repositorio local", r: 56 },
    especie:      { x: 800, y: 112, tipo: "entity",   titulo: ["Especie"], componente: "Modelos de vista", w: 126, h: 54 },
    entrada:      { x: 800, y: 262, tipo: "entity",   titulo: ["EntradaBitacora"], componente: "Modelos de vista", w: 152, h: 58 },
    repoBitacora: { x: 598, y: 412, tipo: "control",  titulo: ["Repositorio", "Bitacora"], componente: "Repositorio local", r: 56, etiqueta: "arriba" },
    cifrado:      { x: 800, y: 412, tipo: "control",  titulo: ["Servicio", "Cifrado"], componente: "Cifrado local", r: 56, etiqueta: "arriba" },
    almacen:      { x: 950, y: 262, tipo: "almacen",  titulo: ["Almacén", "local"], w: 88, h: 190 },
  };
  const ESTEREOTIPO = { boundary: "«boundary»", control: "«controller»", entity: "«entity»" };

  // Las conexiones del diagrama de robustez. Las dos últimas llegan al Almacén local por arriba y por abajo.
  const CABLES = [
    ["actor", "pantalla"], ["pantalla", "controlador"], ["controlador", "repoEspecies"], ["repoEspecies", "especie"],
    ["controlador", "entrada"], ["controlador", "repoBitacora"], ["repoBitacora", "cifrado"],
    ["repoBitacora", "entrada", { llegada: [732, 291] }],
    ["repoEspecies", "almacen", { ruta: [[598, 56], [598, 22], [950, 22], [950, 155]] }],
    ["repoBitacora", "almacen", { ruta: [[598, 468], [598, 500], [950, 500], [950, 369]] }],
  ];

  const mapa = $("#mapa");
  const nodosSvg = {};
  const cablesSvg = {};
  let capaEstelas;
  let capaSemillas;
  let capaGlobos;
  let capaGuardadas;
  let contadorAlmacen;

  function crear(nombre, atributos, padre) {
    const elemento = document.createElementNS(SVG, nombre);
    for (const [clave, valor] of Object.entries(atributos)) elemento.setAttribute(clave, valor);
    if (padre) padre.appendChild(elemento);
    return elemento;
  }
  function texto(contenido, x, y, clase, padre) {
    const elemento = crear("text", { x, y, class: clase, "text-anchor": "middle" }, padre);
    elemento.textContent = contenido;
    return elemento;
  }

  function semiAlto(nodo) {
    if (nodo.r) return nodo.r;
    if (nodo.tipo === "actor") return 34;
    return nodo.h / 2;
  }

  // Punto del borde del nodo en dirección a otro punto: ahí empiezan y terminan los cables.
  function borde(nodo, haciaX, haciaY) {
    const dx = haciaX - nodo.x;
    const dy = haciaY - nodo.y;
    const largo = Math.hypot(dx, dy) || 1;
    if (nodo.r || nodo.tipo === "actor") {
      const radio = nodo.r || 30;
      return [nodo.x + (dx / largo) * radio, nodo.y + (dy / largo) * radio];
    }
    const escala = Math.min((nodo.w / 2) / Math.abs(dx || 1e-9), (nodo.h / 2) / Math.abs(dy || 1e-9));
    return [nodo.x + dx * escala, nodo.y + dy * escala];
  }

  function puntosDelCable([desde, hasta, { ruta, llegada } = {}]) {
    if (ruta) return ruta;
    const a = NODOS[desde];
    const b = NODOS[hasta];
    if (llegada) return [borde(a, ...llegada), llegada];
    return [borde(a, b.x, b.y), borde(b, a.x, a.y)];
  }

  function trazoRedondeado(puntos, radio = 14) {
    let d = `M ${puntos[0][0]} ${puntos[0][1]}`;
    for (let i = 1; i < puntos.length - 1; i += 1) {
      const [px, py] = puntos[i - 1];
      const [cx, cy] = puntos[i];
      const [nx, ny] = puntos[i + 1];
      const r1 = Math.min(radio, Math.hypot(cx - px, cy - py) / 2);
      const r2 = Math.min(radio, Math.hypot(nx - cx, ny - cy) / 2);
      const u1 = [(cx - px) / Math.hypot(cx - px, cy - py), (cy - py) / Math.hypot(cx - px, cy - py)];
      const u2 = [(nx - cx) / Math.hypot(nx - cx, ny - cy), (ny - cy) / Math.hypot(nx - cx, ny - cy)];
      d += ` L ${cx - u1[0] * r1} ${cy - u1[1] * r1} Q ${cx} ${cy} ${cx + u2[0] * r2} ${cy + u2[1] * r2}`;
    }
    const ultimo = puntos[puntos.length - 1];
    return `${d} L ${ultimo[0]} ${ultimo[1]}`;
  }

  function dibujarNodo(clave, nodo) {
    const g = crear("g", { class: `nodo ${nodo.tipo}` }, mapa);
    const { x, y } = nodo;
    if (nodo.tipo === "actor") {
      crear("circle", { cx: x, cy: y - 28, r: 9, class: "figura" }, g);
      crear("path", { d: `M ${x} ${y - 19} V ${y + 8} M ${x - 15} ${y - 9} H ${x + 15} M ${x} ${y + 8} L ${x - 12} ${y + 30} M ${x} ${y + 8} L ${x + 12} ${y + 30}`, class: "figura" }, g);
      texto(nodo.titulo[0], x, y + 50, "titulo", g);
      return g;
    }
    if (nodo.tipo === "boundary") {
      crear("rect", { x: x - nodo.w / 2, y: y - nodo.h / 2, width: nodo.w, height: nodo.h, rx: nodo.h / 2, class: "forma" }, g);
    } else if (nodo.tipo === "control") {
      crear("circle", { cx: x, cy: y, r: nodo.r, class: "forma" }, g);
    } else if (nodo.tipo === "entity") {
      crear("rect", { x: x - nodo.w / 2, y: y - nodo.h / 2, width: nodo.w, height: nodo.h, rx: 3, class: "forma" }, g);
      for (const barra of [x - nodo.w / 2 + 9, x + nodo.w / 2 - 9]) {
        crear("line", { x1: barra, y1: y - nodo.h / 2, x2: barra, y2: y + nodo.h / 2, class: "barra" }, g);
      }
    } else {
      const { w, h } = nodo;
      const ry = 12;
      crear("path", {
        d: `M ${x - w / 2} ${y - h / 2} A ${w / 2} ${ry} 0 0 1 ${x + w / 2} ${y - h / 2} V ${y + h / 2} A ${w / 2} ${ry} 0 0 1 ${x - w / 2} ${y + h / 2} Z`,
        class: "forma" }, g);
      crear("path", { d: `M ${x - w / 2} ${y - h / 2} A ${w / 2} ${ry} 0 0 0 ${x + w / 2} ${y - h / 2}`, class: "forma" }, g);
      crear("title", {}, g).textContent = "Almacén local: en la aplicación es IndexedDB; en este prototipo, un archivo SQLite.";
      texto(nodo.titulo[0], x, y - 52, "titulo", g);
      texto(nodo.titulo[1], x, y - 37, "titulo", g);
      texto("SQLite", x, y - 20, "estereotipo", g);
      texto("(IndexedDB)", x, y - 7, "estereotipo", g);
      capaGuardadas = crear("g", {}, g);
      contadorAlmacen = texto("", x, y + 80, "contador", g);
      return g;
    }
    const lineas = nodo.titulo;
    const inicio = y - (lineas.length === 2 ? 14 : 4);
    lineas.forEach((linea, i) => texto(linea, x, inicio + i * 15, "titulo", g));
    texto(ESTEREOTIPO[nodo.tipo], x, inicio + lineas.length * 15 + 2, "estereotipo", g);
    const yComponente = nodo.etiqueta === "arriba" ? y - semiAlto(nodo) - 9 : y + semiAlto(nodo) + 17;
    texto(nodo.componente, x, yComponente, "componente", g);
    return g;
  }

  function dibujarMapa() {
    const defs = crear("defs", {}, mapa);
    const flecha = crear("marker", { id: "flecha", viewBox: "0 0 10 10", refX: 9, refY: 5, markerWidth: 7, markerHeight: 7, orient: "auto-start-reverse" }, defs);
    crear("path", { d: "M 0 0 L 10 5 L 0 10 z", fill: "rgba(30,43,36,0.45)" }, flecha);
    for (const cable of CABLES) {
      const clave = `${cable[0]}>${cable[1]}`;
      cablesSvg[clave] = crear("path", { class: "cable", d: trazoRedondeado(puntosDelCable(cable)), "marker-end": "url(#flecha)" }, mapa);
    }
    for (const [clave, nodo] of Object.entries(NODOS)) nodosSvg[clave] = dibujarNodo(clave, nodo);
    capaEstelas = crear("g", {}, mapa);
    capaSemillas = crear("g", {}, mapa);
    capaGlobos = crear("g", {}, mapa);
  }

  function dibujarGuardadas(cantidad) {
    if (!capaGuardadas) return;
    capaGuardadas.replaceChildren();
    const visibles = Math.min(cantidad, 24);
    for (let i = 0; i < visibles; i += 1) {
      const fila = Math.floor(i / 6);
      const columna = i % 6;
      crear("circle", { cx: NODOS.almacen.x - 25 + columna * 10, cy: NODOS.almacen.y + 14 + fila * 11, r: 3.6, class: "guardada" }, capaGuardadas);
    }
    contadorAlmacen.textContent = cantidad === 1 ? "1 entrada" : `${cantidad} entradas`;
  }

  /* ------------------------------------------------- la animación */

  const suave = (t) => (t < 0.5 ? 2 * t * t : 1 - (-2 * t + 2) ** 2 / 2);

  function animar(duracion, cadaCuadro) {
    if (QUIETO) { cadaCuadro(1); return Promise.resolve(); }
    return new Promise((listo) => {
      const inicio = performance.now();
      const paso = (ahora) => {
        const t = Math.min(1, (ahora - inicio) / duracion);
        cadaCuadro(t);
        if (t < 1) requestAnimationFrame(paso); else listo();
      };
      requestAnimationFrame(paso);
    });
  }

  function activar(clave, color, ms = 1300) {
    const g = nodosSvg[clave];
    clearTimeout(g.apagar);
    g.classList.remove("c-tierra", "c-hecho", "c-cifra", "c-helada");
    g.classList.add("activo", `c-${color}`);
    g.apagar = setTimeout(() => g.classList.remove("activo", `c-${color}`), ms);
  }

  function encenderCable(desde, hasta, color) {
    const cable = cablesSvg[`${desde}>${hasta}`] || cablesSvg[`${hasta}>${desde}`];
    clearTimeout(cable.apagar);
    cable.classList.remove("c-tierra", "c-hecho", "c-cifra", "c-helada");
    cable.classList.add("encendido", `c-${color}`);
    cable.apagar = setTimeout(() => cable.classList.remove("encendido", `c-${color}`), 2600);
  }

  // El camino de una semilla entre dos nodos: del centro de uno al centro del otro, por su cable.
  function caminoEntre(desde, hasta) {
    const directo = CABLES.find(([a, b]) => a === desde && b === hasta);
    const inverso = CABLES.find(([a, b]) => a === hasta && b === desde);
    const puntos = directo ? puntosDelCable(directo) : puntosDelCable(inverso).slice().reverse();
    return [[NODOS[desde].x, NODOS[desde].y], ...puntos, [NODOS[hasta].x, NODOS[hasta].y]];
  }

  function sembrar(clave, color) {
    return crear("circle", { cx: NODOS[clave].x, cy: NODOS[clave].y, r: 7.5, class: `semilla ${color}` }, capaSemillas);
  }
  const pintar = (semilla, color) => semilla.setAttribute("class", `semilla ${color}`);

  const LARGO_ESTELA = 52;
  async function tramo(semilla, desde, hasta, color, velocidad = 1) {
    const d = trazoRedondeado(caminoEntre(desde, hasta));
    const camino = crear("path", { d, fill: "none" }, capaSemillas);
    const estela = crear("path", { d, class: `estela ${color}` }, capaEstelas);
    const largo = camino.getTotalLength();
    encenderCable(desde, hasta, color);
    await animar(Math.max(320, largo * 2.3) / velocidad, (t) => {
      const avance = suave(t) * largo;
      const punto = camino.getPointAtLength(avance);
      estela.setAttribute("stroke-dasharray", `${Math.min(avance, LARGO_ESTELA)} ${largo + LARGO_ESTELA}`);
      estela.setAttribute("stroke-dashoffset", String(-Math.max(0, avance - LARGO_ESTELA)));
      semilla.setAttribute("cx", punto.x);
      semilla.setAttribute("cy", punto.y);
    });
    camino.remove();
    estela.remove();
  }

  async function desvanecer(semilla) {
    await animar(420, (t) => semilla.setAttribute("opacity", String(1 - t)));
    semilla.remove();
  }

  // Globos: dónde va cada uno para no tapar otros nodos ni cables.
  const LUGAR_DEL_GLOBO = { repoEspecies: "izquierda", repoBitacora: "izquierda", entrada: "arriba", cifrado: "abajo", controlador: "arriba" };
  function globo(clave, contenido, color, ms = 2200) {
    const nodo = NODOS[clave];
    const g = crear("g", { class: `globo ${color}` }, capaGlobos);
    const etiqueta = crear("text", { x: 0, y: 15 }, g);
    etiqueta.textContent = contenido;
    const ancho = etiqueta.getComputedTextLength() + 18;
    let x = nodo.x - ancho / 2;
    let y = nodo.y - semiAlto(nodo) - 32;
    const lugar = LUGAR_DEL_GLOBO[clave];
    if (lugar === "izquierda") { x = nodo.x - semiAlto(nodo) - 12 - ancho; y = nodo.y - 11; }
    if (lugar === "abajo") { y = nodo.y + semiAlto(nodo) + 5; }
    x = Math.max(4, Math.min(x, 895 - ancho));
    crear("rect", { x: 0, y: 0, width: ancho, height: 22, rx: 11 }, g);
    etiqueta.setAttribute("x", 9);
    g.appendChild(etiqueta);
    g.setAttribute("transform", `translate(${x} ${y})`);
    setTimeout(() => g.remove(), QUIETO ? 4000 : ms);
  }

  /* ------------------------------------------------- lo que se cuenta */

  const notaMapa = $("#nota-mapa");
  const traza = $("#traza");
  const REPOSO = "Sin señal. Guardá una observación en el teléfono: acá se repite su recorrido, en cámara lenta.";
  let reposo;

  function anotar(contenido, color) {
    notaMapa.innerHTML = "";
    const punto = document.createElement("span");
    punto.className = "punto";
    punto.style.background = `var(--${color})`;
    notaMapa.append(punto, contenido);
    clearTimeout(reposo);
    reposo = setTimeout(() => { notaMapa.textContent = REPOSO; }, 7000);

    traza.querySelector(".vacia")?.remove();
    const li = document.createElement("li");
    const cuando = document.createElement("time");
    cuando.textContent = hora();
    const que = document.createElement("span");
    const marca = document.createElement("span");
    marca.className = `punto ${color}`;
    que.append(marca, contenido);
    li.append(cuando, que);
    traza.append(li);
    traza.scrollTop = traza.scrollHeight;
  }

  /* ------------------------------------------------- los recorridos (secuencias A y B) */

  const fila = [];
  let ocupado = false;
  function encolar(recorrido) {
    fila.push(recorrido);
    if (!ocupado) seguir();
  }
  async function seguir() {
    ocupado = true;
    while (fila.length) await fila.shift()();
    ocupado = false;
  }

  // Secuencia B: guardar la entrada, con éxito o con rechazo.
  async function recorridoGuardar({ aceptada, motivo, especie, ms, guardadas }) {
    const semilla = sembrar("pantalla", "tierra");
    activar("actor", "tierra");
    activar("pantalla", "tierra");
    anotar("La pantalla le pasa la fecha y la nota al controlador. No decide nada.", "tierra");
    await tramo(semilla, "pantalla", "controlador", "tierra");

    anotar(`El controlador busca la especie en el catálogo local: ${especie}.`, "tierra");
    await tramo(semilla, "controlador", "repoEspecies", "tierra");
    activar("especie", "hecho");
    globo("repoEspecies", "la especie existe", "hecho");
    await esperar(450);
    await tramo(semilla, "repoEspecies", "controlador", "tierra");

    anotar("Le pide a EntradaBitacora que se cree: la entidad aplica las reglas de fecha y nota.", "tierra");
    await tramo(semilla, "controlador", "entrada", "tierra");
    if (!aceptada) {
      pintar(semilla, "helada");
      activar("entrada", "helada", 2800);
      globo("entrada", motivo, "helada", 3600);
      anotar(`EntradaBitacora la rechaza: «${motivo}» No se guarda nada.`, "helada");
      await esperar(1300);
      await tramo(semilla, "entrada", "controlador", "helada");
      await tramo(semilla, "controlador", "pantalla", "helada");
      anotar("La pantalla muestra el motivo y conserva lo que se escribió, para corregirlo.", "helada");
      await desvanecer(semilla);
      return;
    }
    activar("entrada", "hecho");
    globo("entrada", "fecha y nota válidas", "hecho");
    await esperar(550);
    await tramo(semilla, "entrada", "controlador", "tierra");

    anotar("El controlador le pide al repositorio que guarde la entrada nueva, pendiente de sincronizar.", "tierra");
    await tramo(semilla, "controlador", "repoBitacora", "tierra");
    anotar("Antes de escribir, el repositorio le pide al Cifrado local que cifre la fecha y la nota.", "cifra");
    await tramo(semilla, "repoBitacora", "cifrado", "tierra");
    pintar(semilla, "cifra");
    activar("cifrado", "cifra");
    globo("cifrado", "cifrada con AES-256-GCM", "cifra");
    await esperar(550);
    await tramo(semilla, "cifrado", "repoBitacora", "cifra");
    await tramo(semilla, "repoBitacora", "almacen", "cifra");
    activar("almacen", "cifra", 2000);
    semilla.remove();
    dibujarGuardadas(guardadas);
    anotar(`Queda en el Almacén local, cifrada y pendiente de sincronizar. En el teléfono tardó ${ms} ms, sin red.`, "cifra");
  }

  // Secuencia A: elegir la especie y ver su línea de tiempo.
  async function recorridoLeer(especie) {
    const semilla = sembrar("pantalla", "tierra");
    activar("pantalla", "tierra");
    anotar(`La pantalla pide la línea de tiempo de ${especie}.`, "tierra");
    await tramo(semilla, "pantalla", "controlador", "tierra", 1.6);
    await tramo(semilla, "controlador", "repoEspecies", "tierra", 1.6);
    await tramo(semilla, "repoEspecies", "controlador", "tierra", 1.6);
    await tramo(semilla, "controlador", "repoBitacora", "tierra", 1.6);
    await tramo(semilla, "repoBitacora", "almacen", "tierra", 1.6);
    pintar(semilla, "cifra");
    await tramo(semilla, "almacen", "repoBitacora", "cifra", 1.6);
    anotar("El repositorio lee las entradas cifradas y el Cifrado local las descifra con la clave de la sesión.", "cifra");
    await tramo(semilla, "repoBitacora", "cifrado", "cifra", 1.6);
    globo("cifrado", "descifradas", "cifra", 1500);
    pintar(semilla, "tierra");
    await tramo(semilla, "cifrado", "repoBitacora", "tierra", 1.6);
    await tramo(semilla, "repoBitacora", "controlador", "tierra", 1.6);
    globo("controlador", "la más reciente arriba", "tierra", 1600);
    await tramo(semilla, "controlador", "pantalla", "tierra", 1.6);
    anotar(`La línea de tiempo de ${especie}: solo tus entradas, de la más reciente a la más vieja.`, "tierra");
    await desvanecer(semilla);
  }

  /* ------------------------------------------------- la aplicación del teléfono */

  const estado = { especies: [], actual: null, guardadas: 0, rapidas: 0 };
  const fechaEl = $("#fecha");
  const notaEl = $("#nota");
  const errorEl = $("#error");
  const avisoEl = $("#aviso");
  const guardarEl = $("#guardar");

  function avisar(contenido) {
    avisoEl.textContent = contenido;
    avisoEl.classList.add("visible");
    clearTimeout(avisoEl.ocultar);
    avisoEl.ocultar = setTimeout(() => avisoEl.classList.remove("visible"), 2600);
  }

  function nombreDe(especieId) {
    return estado.especies.find((especie) => especie.id === especieId)?.nombre ?? "";
  }

  function dibujarEspecies() {
    const nav = $("#especies");
    nav.replaceChildren();
    for (const especie of estado.especies) {
      const boton = document.createElement("button");
      boton.type = "button";
      boton.textContent = especie.nombre;
      boton.setAttribute("aria-current", String(especie.id === estado.actual));
      boton.addEventListener("click", () => {
        if (especie.id === estado.actual) return;
        estado.actual = especie.id;
        dibujarEspecies();
        errorEl.hidden = true;
        cargarLinea({});
        encolar(() => recorridoLeer(especie.nombre));
      });
      nav.append(boton);
    }
  }

  async function cargarLinea({ recien }) {
    const { ok, datos } = await pedir(`/app/especies/${estado.actual}`);
    if (!ok) return;
    $("#app-especie").textContent = datos.especie.nombre;
    if (!fechaEl.value) fechaEl.value = datos.hoy;
    fechaEl.max = datos.hoy; // la pantalla ayuda; la regla la garantiza la entidad
    const linea = $("#linea");
    linea.replaceChildren();
    let pendientes = 0;
    if (!datos.entradas.length) {
      const li = document.createElement("li");
      li.className = "sin-entradas";
      li.textContent = `Todavía no hay observaciones de ${datos.especie.nombre}. Escribí la primera arriba.`;
      linea.append(li);
    }
    for (const entrada of datos.entradas) {
      const pendiente = entrada.estado_sync === "pendiente_sync";
      pendientes += pendiente;
      const li = document.createElement("li");
      if (entrada.id === recien) li.className = "recien";
      const tarjeta = document.createElement("article");
      tarjeta.className = "tarjeta-nota";
      const cabecera = document.createElement("header");
      const cuando = document.createElement("time");
      cuando.dateTime = entrada.fecha;
      cuando.textContent = fechaLarga(entrada.fecha);
      const pildora = document.createElement("span");
      pildora.className = `pildora ${pendiente ? "pendiente" : "sincronizada"}`;
      pildora.textContent = pendiente ? "⏳ Sin sincronizar" : "✓ Sincronizada";
      cabecera.append(cuando, pildora);
      const nota = document.createElement("p");
      nota.textContent = entrada.nota;
      tarjeta.append(cabecera, nota);
      li.append(tarjeta);
      linea.append(li);
    }
    $("#nube").textContent = pendientes ? `⏳ ${pendientes} sin sincronizar` : "✓ al día";
    $("#ayuda-sync").hidden = pendientes === 0;
  }

  function actualizarMedida(ms) {
    estado.guardadas += 1;
    estado.rapidas += ms < 1000 ? 1 : 0;
    const valor = $("#medida-tiempo");
    valor.textContent = `${ms} ms`;
    valor.classList.remove("recien");
    void valor.offsetWidth;
    valor.classList.add("recien");
    const { guardadas, rapidas } = estado;
    $("#medida-pie").textContent =
      `${rapidas} de ${guardadas} ${guardadas === 1 ? "guardada" : "guardadas"} sin red en menos de 1 s. Medida: el 100%.`;
  }

  $("#redactor").addEventListener("submit", async (evento) => {
    evento.preventDefault();
    if (guardarEl.disabled) return;
    guardarEl.disabled = true;
    const especie = nombreDe(estado.actual);
    const inicio = performance.now();
    const { ok, estado: codigo, datos } = await pedir(`/app/especies/${estado.actual}/entradas`,
      { fecha: fechaEl.value, nota: notaEl.value });
    const ms = Math.max(1, Math.round(performance.now() - inicio));
    guardarEl.disabled = false;
    if (ok) {
      errorEl.hidden = true;
      notaEl.value = "";
      $("#resultado").className = "resultado";
      $("#resultado").replaceChildren();
      avisar("Entrada guardada en tu teléfono.");
      await cargarLinea({ recien: datos.entrada.id });
      actualizarMedida(ms);
      const guardadas = await refrescarArchivo(datos.entrada.id);
      encolar(() => recorridoGuardar({ aceptada: true, especie, ms, guardadas }));
    } else if (codigo === 422) {
      errorEl.textContent = datos.motivo;
      errorEl.hidden = false;
      encolar(() => recorridoGuardar({ aceptada: false, motivo: datos.motivo, especie }));
    }
  });

  /* ------------------------------------------------- el archivo del teléfono */

  const filasEl = $("#filas");
  async function refrescarArchivo(recien) {
    const { datos } = await pedir("/demo/almacen");
    $("#ruta-archivo").textContent = datos.archivo ?? "en memoria: no hay archivo";
    filasEl.replaceChildren();
    if (!datos.filas.length) {
      const li = document.createElement("li");
      li.className = "vacia";
      li.textContent = datos.modo === "memoria"
        ? "Con el repositorio en memoria no queda nada guardado en el disco."
        : "Todavía no hay nada guardado.";
      filasEl.append(li);
    }
    for (const fila of datos.filas) {
      const li = document.createElement("li");
      if (fila.id === recien) li.className = "recien";
      const meta = document.createElement("span");
      meta.className = "meta";
      const modificada = new Date(fila.last_modified).toLocaleString("es-AR", {
        day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit", hourCycle: "h23" });
      meta.textContent = `${fila.especie}, versión ${fila.version}, modificada ${modificada}`;
      const estadoSync = document.createElement("span");
      estadoSync.className = `estado ${fila.estado_sync === "pendiente_sync" ? "pendiente" : "sincronizada"}`;
      estadoSync.textContent = fila.estado_sync;
      const cifrado = document.createElement("span");
      cifrado.className = "cifrado";
      cifrado.title = fila.datos_cifrados;
      cifrado.textContent = fila.datos_cifrados;
      li.append(meta, estadoSync, cifrado);
      filasEl.append(li);
    }
    return datos.filas.length;
  }

  $("#abrir").addEventListener("submit", async (evento) => {
    evento.preventDefault();
    const boton = evento.currentTarget.querySelector("button");
    const resultado = $("#resultado");
    boton.disabled = true;
    resultado.className = "resultado";
    resultado.textContent = "Probando…";
    const { datos } = await pedir("/demo/abrir-almacen", { contrasena: $("#contrasena").value });
    boton.disabled = false;
    if (!datos.legible) {
      resultado.className = "resultado ilegible";
      resultado.textContent = `🔒 ${datos.motivo}`;
      return;
    }
    resultado.className = "resultado legible";
    resultado.textContent = "Con esta contraseña se lee:";
    const lista = document.createElement("ul");
    for (const contenido of datos.datos.slice(0, 4)) {
      const { fecha, nota } = JSON.parse(contenido);
      const li = document.createElement("li");
      li.textContent = `${fecha}: ${nota}`;
      lista.append(li);
    }
    resultado.append(lista);
  });

  /* ------------------------------------------------- arranque */

  function actualizarReloj() {
    $("#reloj").textContent = new Date().toLocaleTimeString("es-AR", { hour: "2-digit", minute: "2-digit", hourCycle: "h23" });
  }

  async function iniciar() {
    dibujarMapa();
    notaMapa.textContent = REPOSO;
    actualizarReloj();
    setInterval(actualizarReloj, 10000);
    const { datos } = await pedir("/app/especies");
    estado.especies = datos;
    estado.actual = (datos.find((especie) => especie.nombre === "Tomate perita") ?? datos[0]).id;
    dibujarEspecies();
    await cargarLinea({});
    dibujarGuardadas(await refrescarArchivo());
  }

  iniciar();
})();
