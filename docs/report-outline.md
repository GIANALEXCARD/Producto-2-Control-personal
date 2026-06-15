# Esquema breve del informe final

## 1. Portada

- Nombre del proyecto: `expense-control`
- Estudiante: **Giancarlos Cardenas Galarza**
- Curso: Construccion de Software
- Tipo de entrega: individual
- Enlace del repositorio GitHub: `https://github.com/GIANALEXCARD/expense-control`

## 2. Objetivo del proyecto

Explicar en un parrafo que `expense-control` es una aplicacion web local para control de gastos personales, desarrollada con Python, biblioteca estandar y SQLite, orientada a demostrar organizacion de codigo, pruebas y gestion del ciclo de vida con Git y GitHub.

## 3. Alcance funcional

Mencionar de forma breve:

- registro de ingresos y gastos
- dashboard o resumen de balance
- persistencia local con SQLite
- pruebas unitarias y validacion basica por CI

## 4. Herramientas y stack

- Python 3
- biblioteca estandar
- SQLite
- Git
- GitHub
- GitHub Actions

## 5. Flujo Git y GitHub aplicado

Explicar con evidencia:

- uso de `main` y `develop`
- creacion de ramas `feature/...`
- commits pequenos y descriptivos
- apertura de Pull Requests
- merge despues de aprobacion de CI

### Evidencias a insertar

- captura del repositorio en GitHub
- captura de ramas
- captura del historial de commits
- captura de un Pull Request abierto o fusionado

## 6. Aplicacion de GitFlow

Describir el flujo con ejemplos exactos:

- `feature/dashboard-resumen`
- `feature/filtro-por-fecha`
- `release/v1.0.0`
- `hotfix/correccion-balance-total`

Explicar para que sirve cada tipo de rama dentro de la entrega academica.

## 7. Evidencia de CI/CD

Explicar que el workflow `/.github/workflows/ci.yml` se ejecuta en `push` y `pull_request`.

Incluir que corre:

- `PYTHONPATH=src python3 -m unittest discover -s tests -v`
- `python3 -m compileall src tests`

### Evidencias a insertar

- captura de la carpeta `.github/workflows`
- captura del archivo `ci.yml`
- captura de GitHub Actions con ejecucion correcta
- captura del PR con check `ci` aprobado

## 8. Resolucion de conflictos

Describir un caso breve de conflicto entre dos ramas feature o entre `release` y `develop`.

### Evidencias a insertar

- captura del PR con conflicto
- captura del archivo con marcadores de conflicto
- captura del archivo resuelto
- captura del commit de resolucion

## 9. Release y hotfix

Explicar como se prepararia una entrega final y una correccion urgente:

- `release/v1.0.0` para consolidar la version academica
- `hotfix/correccion-balance-total` para corregir un error critico despues de liberar la version

### Evidencias a insertar

- captura de la rama release
- captura del PR de release a `main`
- captura de la rama hotfix
- captura del PR del hotfix

## 10. Changelog del proyecto

Referenciar `CHANGELOG.md` como evidencia de trazabilidad de versiones y cambios relevantes.

## 11. Conclusiones

Cerrar con tres ideas concretas:

- Git y GitHub ayudaron a ordenar el trabajo individual
- CI redujo el riesgo de errores antes de fusionar cambios
- GitFlow sirvio como evidencia clara del proceso de construccion del software

## Checklist final antes de entregar

- verificar que todas las capturas correspondan al repositorio real
- verificar que las ramas mostradas existan en GitHub
- verificar que los nombres de commits coincidan con la evidencia
- verificar que no se mencionen enlaces inexistentes
- verificar que el informe aclare que la entrega es individual
