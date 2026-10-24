from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd


class FuenteDatos(ABC):
    """Interfaz común para leer fuentes tabulares de películas."""

    @abstractmethod
    def cargar(self, ruta: str | Path) -> pd.DataFrame:
        """Carga una fuente y devuelve sus registros en una tabla."""


class FuenteCSV(FuenteDatos):
    """Lee registros de películas desde un archivo CSV."""

    def cargar(self, ruta: str | Path) -> pd.DataFrame:
        return pd.read_csv(ruta)


class FuenteJSON(FuenteDatos):
    """Lee una lista de objetos de películas desde un archivo JSON."""

    def cargar(self, ruta: str | Path) -> pd.DataFrame:
        return pd.read_json(ruta)


def crear_fuente(ruta: str | Path) -> FuenteDatos:
    """Selecciona la implementación adecuada según la extensión del archivo."""
    extension = Path(ruta).suffix.lower()
    fuentes = {
        ".csv": FuenteCSV,
        ".json": FuenteJSON,
    }
    try:
        return fuentes[extension]()
    except KeyError as error:
        raise ValueError(
            f"Formato no admitido para {Path(ruta).name}: {extension}"
        ) from error
