# Changelog

Este archivo sirve como evidencia academica de cambios relevantes en `expense-control`.

El formato recomendado para la entrega es simple: version, fecha, tipo de cambio y relacion con la evidencia en GitHub.

## [Unreleased]

### Documentacion

- se agregan guias academicas en `docs/gitflow.md`, `docs/ci-cd.md`, `docs/conflict-resolution.md` y `docs/report-outline.md`
- se incorpora este `CHANGELOG.md` como apoyo para la trazabilidad de versiones
- se actualiza `README.md` con referencia minima a la documentacion final de entrega

## [v1.0.0] - 2026-06-14

### Base funcional esperada

- aplicacion web local para control de gastos personales
- persistencia local con SQLite
- pruebas unitarias ejecutadas desde CI
- verificacion de compilacion con `python3 -m compileall src tests`

### Evidencia que Giancarlos debe capturar cuando cree esta version

- commit donde se cierre la rama `release/v1.0.0`
- Pull Request desde `release/v1.0.0` hacia `main`
- ejecucion correcta del workflow `ci`
- historial de commits asociado a la version

## [v1.0.1] - ejemplo de hotfix futuro

### Correccion esperada

- ajuste urgente desde `hotfix/correccion-balance-total`

### Evidencia que Giancarlos debe capturar si ocurre

- commit del hotfix
- Pull Request del hotfix hacia `main`
- sincronizacion posterior del hotfix hacia `develop`

## Notas de uso academico

- la version `v1.0.0` queda preparada para publicarse cuando el repositorio se suba a GitHub
- no inventar tags, commits o enlaces
- actualizar este archivo cada vez que una feature, release o hotfix quede registrada en GitHub
