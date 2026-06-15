# CI/CD para expense-control

## Objetivo academico

La evidencia de CI/CD debe mostrar que el repositorio valida automaticamente la calidad minima del proyecto cada vez que hay cambios en GitHub. En este caso, el proyecto usa **GitHub Actions** como Integracion Continua.

## Pipeline real del proyecto

Archivo usado por el repositorio:

`/.github/workflows/ci.yml`

El workflow se ejecuta en:

- cada `push`
- cada `pull_request`

## Validaciones que ejecuta CI

El workflow actual corre exactamente estas dos verificaciones:

1. **Pruebas unitarias**

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

2. **Revision de compilacion de fuentes**

```sh
python3 -m compileall src tests
```

Esto permite afirmar, sin exagerar, que CI revisa:

- comportamiento esperado mediante tests
- ausencia de errores basicos de sintaxis o compilacion en archivos Python

## Como explicarlo en el informe

Texto sugerido:

> El proyecto expense-control usa GitHub Actions para ejecutar Integracion Continua. Cada push y cada Pull Request disparan un workflow que corre pruebas unitarias y una verificacion de compilacion de los modulos Python. De esta forma, antes de fusionar una rama, se confirma que los cambios no rompen el comportamiento principal ni introducen errores de sintaxis.

## Relacion con GitFlow

El punto importante para la rubrica no es solo que exista CI, sino que se vea integrado al flujo de ramas:

- una rama `feature/...` abre PR hacia `develop`
- GitHub Actions corre tests y compile checks
- solo si CI pasa, el PR queda listo para merge
- una rama `release/...` tambien debe pasar CI antes de llegar a `main`
- un `hotfix/...` debe volver a ejecutar CI antes de corregir produccion o la version final

## Ejemplo de evidencia esperada

### Pull Request de feature

- Rama origen: `feature/filtro-por-fecha`
- Rama destino: `develop`
- Evidencia clave: estado del check `ci` en verde

### Pull Request de release

- Rama origen: `release/v1.0.0`
- Rama destino: `main`
- Evidencia clave: mismo workflow `ci` ejecutado correctamente antes del merge

## Sobre CD en este proyecto

Por ahora **no hay despliegue automatico**. Eso no invalida la entrega. La forma correcta de documentarlo es indicar que:

- si hay CI implementada
- no hay CD automatica porque la app se ejecuta localmente como tablero web con Python y SQLite
- una evolucion futura podria publicar una version empaquetada o desplegada en otro entorno

## Checklist de capturas para CI/CD

- captura del archivo `.github/workflows/ci.yml` en GitHub
- captura de la pestaña **Actions** mostrando una ejecucion correcta
- captura de un Pull Request con el check `ci` aprobado
- captura del detalle del job donde se vean las etapas de tests y compilacion
- captura del merge final solo despues de que CI marque estado correcto

## Limites que debes declarar

- no afirmar que existe despliegue continuo si no esta implementado
- no afirmar cobertura de pruebas si no se ha medido
- no afirmar integraciones externas, porque el proyecto usa biblioteca estandar y SQLite
