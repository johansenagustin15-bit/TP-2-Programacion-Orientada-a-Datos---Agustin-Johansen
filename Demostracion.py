from pathlib import Path

from pandas.testing import assert_frame_equal

from peliculas import (
    ConsultaPeliculas,
    cargar_peliculas,
    inspeccionar_y_validar,
    limpiar_y_transformar,
)


CARPETA_PROYECTO = Path(__file__).resolve().parent
CARPETA_DATOS = CARPETA_PROYECTO / "data"


def main():
    rutas_datos = {
        "CSV": CARPETA_DATOS / "IMDb 100 Mejores Peliculas.csv",
        "JSON": CARPETA_DATOS / "IMDb 100 Mejores Peliculas.json",
    }
    peliculas_limpias = {}

    for formato, ruta in rutas_datos.items():
        datos_originales = cargar_peliculas(ruta)
        print(f"\n{formato}: {datos_originales.shape[0]} filas, "
              f"{datos_originales.shape[1]} columnas")
        print("Columnas de entrada:", datos_originales.columns.tolist())

        datos_validados = inspeccionar_y_validar(datos_originales, formato)
        peliculas_limpias[formato] = limpiar_y_transformar(datos_validados)

    peliculas_csv = peliculas_limpias["CSV"]
    peliculas_json = peliculas_limpias["JSON"]
    assert_frame_equal(peliculas_csv, peliculas_json, check_dtype=False)

    print("\nCSV y JSON contienen datos equivalentes después de la limpieza.")
    print("Columnas finales:", peliculas_csv.columns.tolist())
    print("\nEjemplo de películas:")
    print(peliculas_csv.head().to_string(index=False))

    resultado = ConsultaPeliculas("genero", "Drama").ejecutar(peliculas_csv)
    print("\nBúsqueda de ejemplo: género = Drama")
    print(f"Coincidencias: {len(resultado)}")
    print("Primeros 10 resultados:")
    print(resultado.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
