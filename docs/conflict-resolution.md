# Resolucion de conflictos

## Objetivo academico

Esta seccion debe demostrar que Giancarlos sabe identificar y resolver conflictos de integracion dentro del flujo GitFlow del proyecto `expense-control`.

## Cuando puede aparecer un conflicto

Un conflicto es probable si dos ramas cambian la misma zona de un archivo. En este proyecto, eso puede pasar en archivos como:

- `README.md`
- `CHANGELOG.md`
- `src/expense_control/app.py`
- `src/expense_control/repository.py`
- `tests/`

Ejemplo academico realista:

- `feature/dashboard-resumen` modifica el bloque principal del dashboard
- `feature/filtro-por-fecha` modifica la misma vista
- al fusionar la segunda rama contra `develop`, Git detecta conflicto

## Flujo recomendado para resolverlo

1. Identificar en GitHub o en local que el Pull Request marca conflicto.
2. Actualizar la rama de trabajo con la base mas reciente.
3. Abrir el archivo en conflicto y localizar los marcadores:

```text
<<<<<<< HEAD
=======
>>>>>>> develop
```

4. Comparar ambas versiones y conservar el resultado correcto.
5. Eliminar los marcadores del conflicto.
6. Revisar que el archivo quede legible y coherente.
7. Ejecutar nuevamente pruebas y verificacion de compilacion.
8. Registrar la resolucion en un commit claro.
9. Confirmar en GitHub que el PR ya puede fusionarse.

## Ejemplo de commit para la resolucion

- `fix: resuelve conflicto entre dashboard y filtro por fecha`
- `docs: resuelve conflicto en changelog de release`

## Como explicarlo en el informe

Texto sugerido:

> Durante el flujo de trabajo con ramas feature, puede ocurrir que dos cambios modifiquen el mismo archivo. En ese caso, se actualiza la rama, se revisan los marcadores de conflicto, se conserva la version correcta y luego se vuelven a ejecutar las pruebas unitarias y la verificacion de compilacion. La resolucion queda trazada en un commit especifico antes de completar el Pull Request.

## Recomendaciones para que la evidencia sea creible

- usar conflictos pequenos y faciles de explicar
- mostrar el archivo antes y despues de resolverlo
- asociar el conflicto a una rama feature o release real del proyecto
- mostrar que despues de resolverlo, CI vuelve a pasar

## Checklist de capturas para evidencia

- captura del Pull Request donde GitHub indica que hay conflicto
- captura del archivo con marcadores `<<<<<<<`, `=======`, `>>>>>>>`
- captura del archivo final ya resuelto
- captura del commit usado para registrar la resolucion
- captura del check `ci` en verde despues de resolver el conflicto

## Errores que debes evitar

- no dejar marcadores de conflicto en el archivo final
- no cerrar un conflicto sin volver a correr tests y compile checks
- no decir que el conflicto se resolvio automaticamente si hubo edicion manual
