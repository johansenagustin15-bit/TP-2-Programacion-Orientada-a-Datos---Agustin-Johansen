# IMDb: 100 mejores películas

**Autor:** Agustín Johansen

## Objetivo

La aplicación permite buscar cómodamente entre las 100 mejores películas según IMDb. Está pensada para quien quiera encontrar películas para un trabajo o por curiosidad.

## Cómo usarla

Requisitos: Python 3.10 o posterior y las dependencias indicadas en `requirements.txt`. Desde la carpeta del proyecto, instalalas y ejecutá:

```powershell
python -m pip install -r requirements.txt
python Busqueda.py
```

Por defecto, el programa carga el CSV de `data`. Para usar el JSON, cambiá `FORMATO_ENTRADA` de `"csv"` a `"json"` en `Busqueda.py`. El menú ofrece dos grupos de filtros:

- **Numéricos:** ranking, año y nota IMDb.
- **De texto:** título de película, director y género.

Ingresá el valor que querés buscar. Podés hacer varias consultas; elegí `0` para terminar. Cada consulta muestra una tabla y guarda el resultado en `resultado_busqueda.csv`.

Para ejecutar las pruebas:

```powershell
python -m unittest discover -s tests -v
```

Para mostrar el flujo de ambos formatos y una búsqueda de ejemplo:

```powershell
python Demostracion.py
```

Las búsquedas por título y director aceptan coincidencias parciales sin distinguir mayúsculas y minúsculas. Por ejemplo, al buscar director con `nolan` aparecen las películas de Christopher Nolan. Para género, ingresá el nombre completo de un género (por ejemplo, `Drama`), aunque la película tenga otros géneros asociados.

## Datos, procedencia y alcance

Los archivos `data/IMDb 100 Mejores Peliculas.csv` y `data/IMDb 100 Mejores Peliculas.json` contienen los mismos 100 registros. Cada fila representa una película; se utilizan ranking, título en español, título en inglés, año, nota de IMDb, director y géneros. El JSON se generó a partir del CSV para comprobar que el programa procese los dos formatos.

La fuente indicada para el listado es [IMDb, lista ls070295830](https://www.imdb.com/es/list/ls070295830/), consultada el 9 de octubre de 2026. No se identificó una licencia abierta específica para estos datos. Según las [Condiciones de uso de IMDb](https://www.imdb.com/conditions), IMDb y sus proveedores reservan derechos sobre el contenido y sus compilaciones; el acceso se concede para uso personal y no comercial bajo condiciones limitadas, y la extracción automatizada requiere autorización expresa. Estas condiciones no deben interpretarse como una licencia abierta ni como permiso general para redistribuir la lista. Para esta demostración académica se atribuye la fuente y se describe la limitación; no se afirma que exista autorización para otros usos.

Es una muestra de 100 observaciones. El listado es una selección y no representa todas las películas ni todos los gustos; los rankings y notas pueden cambiar con el tiempo. La traducción de los títulos al español también puede variar según la fuente. La primera versión no consulta IMDb en tiempo real ni incluye el resto de las películas.

## Limpieza

El flujo lee los archivos mediante una interfaz común con implementaciones para CSV y JSON; inspecciona columnas y valida valores vacíos, duplicados y rangos. Una expresión regular comprueba que el año tenga cuatro dígitos (se admite el sufijo `.0` que puede producir una lectura numérica); la comprobación numérica adicional valida que sea entero y esté entre 1888 y 2100. La nota debe estar entre 0 y 10 y el ranking entre 1 y 100. Si hay errores, la ejecución se detiene con un mensaje que describe los problemas y, para años o números inválidos, indica las filas del archivo. No se descartan errores silenciosamente.

En los datos incluidos se validan las 100 filas y no se rechaza ninguna. Después se recortan espacios, se normaliza la separación de géneros, se convierten ranking, año y nota a tipos numéricos, se descarta el título en inglés de la tabla de resultados y se renombran las columnas. Los archivos originales no se modifican.

## Organización

- `Busqueda.py`: menú interactivo.
- `Demostracion.py`: ejemplo reproducible que compara las lecturas CSV/JSON.
- `fuentes.py`: interfaz `FuenteDatos` e implementaciones `FuenteCSV` y `FuenteJSON`.
- `peliculas.py`: validación, limpieza, búsquedas y modelo `ConsultaPeliculas`.
- `tests/`: pruebas automatizadas.
- `data/`: archivos de entrada y descripción de procedencia (`data/README.md`).

## Ejemplo de resultado

Al ejecutar la demostración, ambos formatos producen tablas equivalentes. La búsqueda de género `Drama` encuentra 73 películas en el conjunto incluido. Ese número describe esta muestra concreta, no un catálogo completo de IMDb.
