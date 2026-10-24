import unittest
from pathlib import Path

from pandas.testing import assert_frame_equal

from peliculas import (
    ConsultaPeliculas,
    cargar_peliculas,
    inspeccionar_y_validar,
    limpiar_y_transformar,
)


CARPETA_PROYECTO = Path(__file__).resolve().parents[1]
CARPETA_DATOS = CARPETA_PROYECTO / "data"


def cargar_y_limpiar(nombre_archivo, nombre_formato):
    datos = cargar_peliculas(CARPETA_DATOS / nombre_archivo)
    return limpiar_y_transformar(
        inspeccionar_y_validar(datos, nombre_formato)
    )


class PruebasPeliculas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.peliculas_csv = cargar_y_limpiar(
            "IMDb 100 Mejores Peliculas.csv", "CSV"
        )

    def test_busqueda_normal_por_genero(self):
        resultado = ConsultaPeliculas("genero", "Drama").ejecutar(
            self.peliculas_csv
        )

        self.assertEqual(len(resultado), 73)
        self.assertTrue(resultado["Genero"].str.contains("Drama").all())

    def test_rechaza_criterio_numerico_invalido(self):
        with self.assertRaisesRegex(ValueError, "número entero válido"):
            ConsultaPeliculas("ranking", "primero").ejecutar(
                self.peliculas_csv
            )

    def test_validacion_informa_fila_con_anio_mal_formado(self):
        datos = cargar_peliculas(
            CARPETA_DATOS / "IMDb 100 Mejores Peliculas.csv"
        )
        datos["Anio"] = datos["Anio"].astype("string")
        datos.loc[0, "Anio"] = "19x4"

        with self.assertRaisesRegex(
            ValueError, r"Anio debe tener cuatro dígitos \(filas: \[2\]\)"
        ):
            inspeccionar_y_validar(datos, "CSV de prueba")

    def test_lecturas_csv_y_json_son_equivalentes(self):
        peliculas_json = cargar_y_limpiar(
            "IMDb 100 Mejores Peliculas.json", "JSON"
        )

        assert_frame_equal(
            self.peliculas_csv, peliculas_json, check_dtype=False
        )
        self.assertEqual(len(self.peliculas_csv), 100)
        self.assertTrue(self.peliculas_csv["Ranking"].is_unique)


if __name__ == "__main__":
    unittest.main()
