# Expense Control

Aplicacion academica personal para control de gastos personales de Giancarlos Cardenas Galarza.

## Objetivo

Registrar una base limpia para documentar y desarrollar un sistema simple de control de gastos personales.

## Stack

- Python 3
- Biblioteca estandar de Python
- Shell POSIX para scripts
- Git/GitHub para flujo de trabajo

## Estructura inicial

- `src/expense_control/` paquete principal
- `tests/` pruebas
- `docs/` documentacion del proyecto
- `scripts/` comandos locales
- `.github/workflows/` CI basica

## Comandos locales

```sh
./scripts/run.sh
./scripts/test.sh
```

Tambien se puede ejecutar directamente:

```sh
PYTHONPATH=src python3 -m expense_control.app
PYTHONPATH=src python3 -m unittest discover -s tests -v
python3 -m compileall src tests
```

La aplicacion web abre un servidor local en `http://127.0.0.1:8000` y guarda los datos en `data/expense-control.sqlite3` usando el repositorio SQLite del proyecto. Se puede cambiar el puerto o la ruta con `EXPENSE_CONTROL_PORT` y `EXPENSE_CONTROL_DB`.

## Demostracion GitFlow

1. Crear una rama desde `main`: `feature/registro-gastos`
2. Hacer cambios pequenos y commits atomicos
3. Abrir Pull Request hacia `main`
4. Resolver conflictos con cuidado si la rama base cambio
5. Fusionar solo cuando la verificacion pase

## Documentacion academica final

La guia breve para sustentar la entrega individual esta en:

- `docs/gitflow.md`
- `docs/ci-cd.md`
- `docs/conflict-resolution.md`
- `docs/report-outline.md`
- `CHANGELOG.md`

## Estado

Este repositorio contiene la logica de dominio, persistencia SQLite basica, pruebas unitarias y una interfaz web simple para demostracion academica.
