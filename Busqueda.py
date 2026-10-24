from pathlib import Path

from peliculas import (
    cargar_peliculas,
    inspeccionar_y_validar,
    limpiar_y_transformar,
    menu_busqueda,
)


CARPETA_PROYECTO = Path(__file__).resolve().parent
CARPETA_DATOS = CARPETA_PROYECTO / "data"
FORMATO_ENTRADA = "csv"


def main():
    rutas_datos = {
        "csv": CARPETA_DATOS / "IMDb 100 Mejores Peliculas.csv",
        "json": CARPETA_DATOS / "IMDb 100 Mejores Peliculas.json",
    }
    if FORMATO_ENTRADA not in rutas_datos:
        raise ValueError('FORMATO_ENTRADA debe ser "csv" o "json".')

    datos_originales = cargar_peliculas(rutas_datos[FORMATO_ENTRADA])
    datos_validados = inspeccionar_y_validar(
        datos_originales, FORMATO_ENTRADA.upper()
    )
    peliculas = limpiar_y_transformar(datos_validados)
    menu_busqueda(
        peliculas,
        CARPETA_PROYECTO / "resultado_busqueda.csv",
    )


if __name__ == "__main__":
    main()
