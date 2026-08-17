---
title: Git, GitHub y Documentación
nav_order: 1
---

# Instructivo — Git, GitHub y Documentación Técnica

**Aplica a:** TP1 a TP5 y Trabajo Integrador · **Plataforma única:** GitHub (código, documentación, renderizado y publicación web)

Este instructivo es transversal a toda la materia. No se repite dentro de cada guía de TP — cada guía enlaza acá.

---

## 1. Por qué documentamos así

La documentación es un ítem de configuración más, sujeto al mismo rigor de control de versiones que el código: diffs, commits y revisión por Pull Request aplican tanto a un diagrama como a un párrafo de prosa. Esto conecta directamente con la Administración de la Configuración (Módulo 7) — solo que se empieza a practicar desde el TP1, no recién al final del cuatrimestre.

## 2. Primeros pasos con Git (antes del TP1)

```bash
git clone <url-de-este-repositorio-de-catedra>   # traer los materiales — tu primer comando
git --version                                     # verificar que Git esté instalado
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

Cuando en el TP1 creen el repositorio de su propio grupo, los primeros comandos van a ser:

```bash
git init                                          # si lo crean localmente primero
git remote add origin <url-del-repo-del-grupo>
git add .
git commit -m "chore: estructura inicial del repositorio"
git push -u origin main
```

Durante el TP1 todo el grupo trabaja sobre `main`. El trabajo con ramas (`git branch`, `git checkout -b`) se introduce recién en el TP2.

## 3. Estructura de repositorio recomendada (repo de cada grupo)

```
bio-[nombre-sistema]-2026/
├── docs/
│   ├── requirements/      ← SRS, historias de usuario, casos de uso (TP1)
│   ├── ux/                 ← wireframes, flujos (TP2)
│   ├── architecture/      ← diagramas C4, ADR (TP3)
│   └── design/             ← diseño detallado (TP4)
├── src/                    ← código (desde TP4)
├── tests/                  ← pruebas (TP5)
├── docs/uso-ia.md
└── README.md
```

## 4. Convenciones de Markdown

- Un `#` por documento (título), `##`/`###` para secciones — sin saltar niveles.
- Listas de tareas (`- [ ]`) para checklists de entrega.
- Bloques de código con el lenguaje indicado (` ```python `, ` ```bash `) para que se coloree bien.
- Nada de capturas de pantalla de diagramas: todo diagrama va en bloque ` ```mermaid ` como texto, nunca como imagen pegada.

## 5. Mermaid por etapa del proyecto

| TP | Tipo de diagrama | Bloque |
|---|---|---|
| TP1 | Contexto informal, modelo de dominio | `flowchart`, `erDiagram` |
| TP2 | Flujos de usuario | `flowchart`, `journey` |
| TP3 | C4 (contexto, contenedores) | `C4Context`, `C4Container` |
| TP4 | Clases, secuencia | `classDiagram`, `sequenceDiagram` |
| TP5 | Estados, flujo de pruebas | `stateDiagram-v2`, `flowchart` |

Prototipar un diagrama antes de commitearlo: [mermaid.live](https://mermaid.live).

## 6. Flujo de trabajo con Git para documentación

1. Commits atómicos y descriptivos: `docs: agrega HU-01 al SRS — carga de archivo FASTA`.
2. Desde el TP2: una rama por artefacto o TP (`docs/tp3-arquitectura`), Pull Request hacia `main` con revisión cruzada del grupo antes de mergear.
3. El historial de commits sobre `docs/` es parte de la evidencia evaluable — commits pequeños y frecuentes valen más que uno solo la noche anterior a la presentación.
4. Nunca reescribir historia (`rebase -i` destructivo, `push --force`) sobre ramas compartidas del equipo sin acuerdo previo.

## 7. Todo en GitHub: repositorio y sitio web con GitHub Pages

**Regla del curso: un único ecosistema.** Código, documentación, historial de decisiones y publicación web viven en el mismo repositorio — sin Google Docs, Notion, Confluence ni hosting externo.

### 7.1 Lectura rápida dentro del repositorio

GitHub renderiza Markdown y bloques ` ```mermaid ` automáticamente al navegar cualquier `.md`, sin configuración adicional. Es la forma más simple de revisar durante el cursado y en los Pull Requests.

### 7.2 Publicación como sitio con GitHub Pages

1. En el repositorio del grupo: `Settings → Pages`.
2. **Source:** `Deploy from a branch` — **Branch:** `main` — **Carpeta:** `/docs`.
3. Guardar. GitHub construye el sitio en cada push a esa rama.
4. URL resultante: `https://<usuario-u-organizacion>.github.io/<repositorio>/`.

Para que Mermaid se renderice como diagrama (no como texto) en el sitio publicado, agregar `docs/_config.yml`:

```yaml
theme: just-the-docs
title: Documentación del proyecto
description: Documentación técnica — Ingeniería de Software
mermaid:
  version: "10.9.1"
```

`just-the-docs` soporta Mermaid nativamente y genera el menú de navegación lateral a partir de la estructura de carpetas. Cada `.md` en `docs/` lleva front matter:

```markdown
---
title: Arquitectura del Sistema
nav_order: 3
---
```

### 7.3 Checklist de Pages

- [ ] `docs/_config.yml` presente con tema y versión de Mermaid.
- [ ] GitHub Pages habilitado, apuntando a `/docs`.
- [ ] Link del sitio publicado en el `README.md` del repositorio.
- [ ] El sitio se actualiza correctamente después de cada push (verificar antes de cada presentación).

---

*Instructivo de la unidad curricular Ingeniería de Software — Licenciatura en Bioinformática, FIUNER.*
