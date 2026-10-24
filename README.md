# IMDb: 100 mejores películas

## Objetivo

La aplicación permite buscar cómodamente entre las 100 mejores películas según IMDb. Está pensada para quien quiera encontrar películas para un trabajo o por curiosidad, busca que puedas ver con mucha mas comodidad el puesto de alguna pelicula en el ranking o ver cuantas peliculas en la lista tiene un director, cuantas peliculas de cierto género hay, etc.

## Cómo usarla

Abrí `Busqueda.ipynb` en VS Code y ejecutá sus celdas en orden. El cuaderno importa las funciones de `peliculas.py`, carga y valida el archivo elegido, y luego inicia el menú con dos grupos de filtros:

- **Numéricos:** ranking, año y nota IMDb.
- **De texto:** título de película, director y género.

Ingresá el valor que querés buscar. Podés hacer varias búsquedas; elegí `0` para terminar. Cada consulta muestra una tabla y guarda sus resultados en `resultado_busqueda.csv`.

La búsqueda por título acepta coincidencias parciales sin distinguir mayúsculas y minúsculas. Para director se debe ingresar el nombre completo y para género, el nombre completo de un género (por ejemplo, `Drama`), aunque la película tenga otros géneros asociados. En ambos casos se ignoran las diferencias entre mayúsculas y minúsculas.

## Datos y alcance

Los datos se leen desde la carpeta `data`: `data/IMDb 100 Mejores Peliculas.csv` o `data/IMDb 100 Mejores Peliculas.json`. Ambos archivos contienen las mismas 100 películas; el JSON se generó a partir del CSV para probar la lectura de ambos formatos. La primera versión se limita a las 100 películas seleccionadas y no incluye las 150 restantes de IMDb.

## Limpieza

El flujo valida la estructura, los datos vacíos o inválidos, los duplicados y los rangos esperados. Luego normaliza los espacios, convierte ranking, año y nota a tipos numéricos, descarta el título en inglés y renombra las columnas de salida como `Ranking`, `Titulo`, `Año` y `Nota`. Los archivos de entrada no se modifican.
## Fuentes
https://www.imdb.com/es/list/ls070295830/
El dataset lo cree con IA basándome en la fuente, pueden llegar a variar los puestos de algunas peliculas, ya que lo cree el 9/10/2026
