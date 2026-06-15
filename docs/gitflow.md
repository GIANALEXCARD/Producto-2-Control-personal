# GitFlow para la entrega individual

## Contexto de la entrega

Este proyecto se presenta como trabajo individual de **Giancarlos Cardenas Galarza**. El flujo debe demostrar uso ordenado de Git y GitHub, aunque la aplicacion sea personal y el repositorio tenga un solo autor.

Repositorio esperado en GitHub: `https://github.com/GIANALEXCARD/expense-control`

## Ramas recomendadas

- `main`: version estable que sirve como base de evidencia final.
- `develop`: rama de integracion para consolidar features antes de preparar una version.
- `feature/<tema>`: trabajo de una funcionalidad o mejora puntual.
- `release/<version>`: cierre previo a la entrega o version demostrable.
- `hotfix/<tema>`: correccion urgente sobre una version ya publicada o ya etiquetada.

## Flujo sugerido para demostrar GitFlow

1. Partir desde `main` y crear `develop`.
2. Crear una rama `feature/...` desde `develop`.
3. Hacer commits pequenos, claros y verificables.
4. Abrir Pull Request hacia `develop`.
5. Esperar que CI marque pruebas y compilacion en verde.
6. Fusionar el PR.
7. Cuando varias features esten integradas, crear `release/...` desde `develop`.
8. Ajustar documentacion o detalles finales dentro de la release.
9. Abrir Pull Request de `release/...` hacia `main`.
10. Fusionar a `main` y luego sincronizar cambios de vuelta en `develop`.

## Ejemplo exacto de ramas para este proyecto

- `develop`
- `feature/dashboard-resumen`
- `feature/filtro-por-fecha`
- `release/v1.0.0`
- `hotfix/correccion-balance-total`

## Ejemplo exacto de secuencia de trabajo

### 1. Feature

Ejemplo de rama:

`feature/dashboard-resumen`

Ejemplos de commits que si puedes mostrar en GitHub:

- `docs: describe flujo GitFlow para expense-control`
- `feat: agrega resumen de balance en dashboard`
- `test: cubre calculo de balance acumulado`

Ejemplo de Pull Request:

- **Titulo:** `feature/dashboard-resumen -> develop`
- **Descripcion breve:** agrega resumen visual del balance y deja evidencia de pruebas locales y CI.

### 2. Release

Ejemplo de rama:

`release/v1.0.0`

Ejemplos de commits:

- `docs: prepara evidencias academicas de la entrega`
- `chore: actualiza changelog para version v1.0.0`

Ejemplo de Pull Request:

- **Titulo:** `release/v1.0.0 -> main`
- **Descripcion breve:** consolida la version estable para entrega academica individual.

### 3. Hotfix

Ejemplo de rama:

`hotfix/correccion-balance-total`

Ejemplos de commits:

- `fix: corrige calculo del balance total en el dashboard`
- `test: valida balance total despues del hotfix`

Ejemplo de Pull Request:

- **Titulo:** `hotfix/correccion-balance-total -> main`
- **Descripcion breve:** corrige un error critico detectado despues de la release.

Despues del merge del hotfix en `main`, el mismo ajuste debe regresar a `develop` para no perder sincronizacion.

## Como explicarlo en la sustentacion o informe

Giancarlos puede decir que uso GitFlow de forma simplificada para evidenciar:

- separacion entre trabajo estable e integracion
- trazabilidad de cambios mediante commits pequenos
- revision formal con Pull Requests, aunque sea en un repositorio personal
- control de versiones para una release academica y un hotfix posterior

## Checklist de evidencia para capturas

- captura de la lista de ramas en GitHub, mostrando `main`, `develop` y al menos una `feature/...`
- captura del historial de commits de una rama feature
- captura del Pull Request abierto hacia `develop`
- captura del Pull Request de `release/v1.0.0` hacia `main`
- captura de un merge completado
- captura del arbol de archivos del repositorio `expense-control`

## Que no debes hacer en la evidencia

- no inventar enlaces de Pull Request si todavia no existen
- no mostrar ramas sin relacion con el proyecto
- no subir commits gigantes si la rubrica pide trabajo incremental
