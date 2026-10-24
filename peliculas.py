import sys
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from fuentes import crear_fuente


COLUMNAS_ESPERADAS = [
    "Rank",
    "Titulo_ES",
    "Titulo_EN",
    "Anio",
    "Nota_IMDb",
    "Director",
    "Genero",
]
COLUMNAS_NUMERICAS = ["Rank", "Anio", "Nota_IMDb"]
COLUMNAS_TEXTO = ["Titulo_ES", "Titulo_EN", "Director", "Genero"]

OPCIONES_NUMERICAS = {
    "1": ("ranking", "Ranking"),
    "2": ("año", "Año"),
    "3": ("nota", "Nota IMDb"),
}
OPCIONES_TEXTO = {
    "1": ("titulo", "Título de película"),
    "2": ("director", "Director"),
    "3": ("genero", "Género"),
}


def cargar_peliculas(ruta):
    """Carga películas desde un archivo CSV o JSON."""
    ruta = Path(ruta)
    if not ruta.is_file():
        raise FileNotFoundError(f"No se encontró el archivo de datos: {ruta}")

    return crear_fuente(ruta).cargar(ruta)


def inspeccionar_y_validar(datos, nombre="Datos"):
    """Comprueba columnas, valores, duplicados y rangos del conjunto."""
    faltantes = [
        columna for columna in COLUMNAS_ESPERADAS if columna not in datos.columns
    ]
    if faltantes:
        raise ValueError(f"{nombre}: faltan columnas requeridas: {faltantes}")

    datos = datos[COLUMNAS_ESPERADAS].copy()
    problemas = []
    numero_fila = lambda mascara: (datos.index[mascara] + 2).tolist()
    vacios = datos[COLUMNAS_ESPERADAS].isna().sum()
    vacios_texto = datos[COLUMNAS_TEXTO].apply(
        lambda columna: columna.astype("string").str.strip().eq("").sum()
    )
    if vacios.sum() or vacios_texto.sum():
        filas_vacias = datos.isna().any(axis=1)
        filas_texto_vacio = datos[COLUMNAS_TEXTO].apply(
            lambda columna: columna.astype("string").str.strip().eq("")
        ).any(axis=1)
        problemas.append(
            f"hay valores nulos ({vacios.to_dict()}) o textos vacíos "
            f"({vacios_texto.to_dict()}); filas: "
            f"{numero_fila(filas_vacias | filas_texto_vacio)}"
        )

    anios_texto = datos["Anio"].astype("string").str.strip()
    anios_con_formato_invalido = ~anios_texto.str.fullmatch(
        r"\d{4}(?:\.0)?", na=False
    )
    if anios_con_formato_invalido.any():
        problemas.append(
            "Anio debe tener cuatro dígitos "
            f"(filas: {numero_fila(anios_con_formato_invalido)})"
        )

    for columna in COLUMNAS_NUMERICAS:
        convertidos = pd.to_numeric(datos[columna], errors="coerce")
        invalidos = convertidos.isna()
        if invalidos.any():
            problemas.append(
                f"{columna} contiene {int(invalidos.sum())} valores no numéricos "
                f"(filas: {numero_fila(invalidos)})"
            )
        if (
            columna in {"Rank", "Anio"}
            and not convertidos.dropna().mod(1).eq(0).all()
        ):
            no_enteros = convertidos.notna() & convertidos.mod(1).ne(0)
            problemas.append(
                f"{columna} debe contener números enteros "
                f"(filas: {numero_fila(no_enteros)})"
            )
        datos[columna] = convertidos

    ranking_repetido = datos["Rank"].duplicated(keep=False)
    if ranking_repetido.any():
        problemas.append(
            f"hay valores de Rank repetidos (filas: "
            f"{numero_fila(ranking_repetido)})"
        )
    if len(datos) != 100:
        problemas.append(f"se esperaban 100 filas y hay {len(datos)}")
    ranking_fuera_de_rango = ~datos["Rank"].between(1, 100)
    if ranking_fuera_de_rango.any():
        problemas.append(
            f"hay rankings fuera del rango 1–100 (filas: "
            f"{numero_fila(ranking_fuera_de_rango)})"
        )
    anio_fuera_de_rango = ~datos["Anio"].between(1888, 2100)
    if anio_fuera_de_rango.any():
        problemas.append(
            f"hay años fuera del rango razonable 1888–2100 (filas: "
            f"{numero_fila(anio_fuera_de_rango)})"
        )
    nota_fuera_de_rango = ~datos["Nota_IMDb"].between(0, 10)
    if nota_fuera_de_rango.any():
        problemas.append(
            f"hay notas fuera del rango 0–10 (filas: "
            f"{numero_fila(nota_fuera_de_rango)})"
        )
    filas_duplicadas = datos.duplicated(keep=False)
    if filas_duplicadas.any():
        problemas.append(
            f"hay filas completamente duplicadas (filas: "
            f"{numero_fila(filas_duplicadas)})"
        )

    if problemas:
        raise ValueError(
            f"{nombre}: validación fallida; se rechaza el archivo completo: "
            + "; ".join(problemas)
        )

    print(
        f"{nombre}: {len(datos)} filas validadas; 0 filas rechazadas; "
        "sin vacíos ni duplicados; rangos válidos."
    )
    return datos


def limpiar_y_transformar(datos):
    """Normaliza datos y deja los encabezados definidos para la aplicación."""
    resultado = datos.copy()
    for columna in COLUMNAS_TEXTO:
        resultado[columna] = resultado[columna].str.strip()

    resultado["Genero"] = resultado["Genero"].apply(
        lambda valor: ", ".join(genero.strip() for genero in valor.split(","))
    )
    resultado["Rank"] = resultado["Rank"].astype("int64")
    resultado["Anio"] = resultado["Anio"].astype("int64")
    resultado["Nota_IMDb"] = resultado["Nota_IMDb"].astype("float64")
    resultado = resultado.drop(columns=["Titulo_EN"]).rename(
        columns={
            "Rank": "Ranking",
            "Titulo_ES": "Titulo",
            "Anio": "Año",
            "Nota_IMDb": "Nota",
        }
    )
    return resultado.sort_values("Ranking").reset_index(drop=True)


def buscar_peliculas(datos, criterio, valor):
    """Filtra por ranking, año, nota, título, director o género."""
    columnas_texto = {
        "titulo": "Titulo",
        "director": "Director",
        "genero": "Genero",
    }
    columnas_numericas = {
        "ranking": "Ranking",
        "año": "Año",
        "nota": "Nota",
    }

    if criterio in columnas_texto:
        texto = str(valor).strip()
        if not texto:
            raise ValueError("El texto de búsqueda no puede estar vacío.")
        columna = columnas_texto[criterio]
        if criterio in {"titulo", "director"}:
            coincidencias = datos[columna].str.contains(
                texto, case=False, regex=False, na=False
            )
        else:
            coincidencias = datos[columna].apply(
                lambda generos: texto.casefold()
                in [
                    genero.strip().casefold()
                    for genero in generos.split(",")
                ]
            )
        return datos.loc[coincidencias].sort_values("Ranking").reset_index(drop=True)

    if criterio not in columnas_numericas:
        opciones = [*columnas_numericas, *columnas_texto]
        raise ValueError(f"Criterio no válido: {criterio}. Elegí uno de {opciones}.")

    columna = columnas_numericas[criterio]
    try:
        valor_numerico = float(valor) if criterio == "nota" else int(valor)
    except (TypeError, ValueError) as error:
        tipo_esperado = "número" if criterio == "nota" else "número entero"
        raise ValueError(
            f"Para buscar por {criterio}, ingresá un {tipo_esperado} válido."
        ) from error

    limites = {
        "ranking": (1, 100),
        "año": (1888, 2100),
        "nota": (0, 10),
    }
    minimo, maximo = limites[criterio]
    if not minimo <= valor_numerico <= maximo:
        raise ValueError(
            f"Para buscar por {criterio}, ingresá un valor entre {minimo} y {maximo}."
        )

    return (
        datos.loc[datos[columna] == valor_numerico]
        .sort_values("Ranking")
        .reset_index(drop=True)
    )


@dataclass(frozen=True)
class ConsultaPeliculas:
    """Representa una consulta del usuario sobre el catálogo de películas."""

    criterio: str
    valor: str | int | float

    def ejecutar(self, peliculas):
        """Devuelve las películas que cumplen el criterio de la consulta."""
        return buscar_peliculas(peliculas, self.criterio, self.valor)


def mensaje_sin_resultados(criterio, valor):
    """Describe qué filtro no produjo coincidencias y sugiere qué revisar."""
    mensajes = {
        "ranking": f"No se encontró una película con ranking {valor}.",
        "año": f"No se encontraron películas estrenadas en el año {valor}.",
        "nota": f"No se encontraron películas con nota IMDb {valor}.",
        "titulo": (
            f"No se encontraron películas cuyo título coincida con {valor!r}. "
            "Probá con otra parte del título."
        ),
        "director": (
            f"No se encontraron películas cuyo director coincida con {valor!r}. "
            "Probá con otra parte del nombre."
        ),
        "genero": (
            f"No se encontraron películas del género {valor!r}. "
            "Ingresá el nombre completo de un género, por ejemplo, Drama."
        ),
    }
    return mensajes[criterio]


def menu_busqueda(datos, ruta_resultado="resultado_busqueda.csv"):
    """Permite realizar varias búsquedas y guarda cada resultado en CSV."""
    ruta_resultado = Path(ruta_resultado)

    while True:
        print("¿Qué tipo de búsqueda querés hacer?")
        print("1. Buscar por un dato numérico")
        print("2. Buscar escribiendo texto")
        print("0. Salir")
        sys.stdout.flush()
        tipo_busqueda = input("Elegí una opción: ").strip()

        if tipo_busqueda == "0":
            print("Fin de la búsqueda.")
            break
        if tipo_busqueda == "1":
            opciones = OPCIONES_NUMERICAS
            print("Filtros numéricos:")
        elif tipo_busqueda == "2":
            opciones = OPCIONES_TEXTO
            print("Filtros de texto:")
        else:
            print("Opción no válida. Elegí 1, 2 o 0 para salir.\n")
            continue

        for numero, (_, nombre) in opciones.items():
            print(f"{numero}. {nombre}")
        sys.stdout.flush()
        opcion = input("Elegí un filtro: ").strip()
        if opcion not in opciones:
            print("Filtro no válido. Volvé a intentarlo.\n")
            continue
        criterio, nombre_criterio = opciones[opcion]
        es_texto = criterio in {"titulo", "director", "genero"}
        while True:
            sys.stdout.flush()
            valor = input(f"Ingresá {nombre_criterio.lower()}: ").strip()
            try:
                resultado = ConsultaPeliculas(criterio, valor).ejecutar(datos)
            except ValueError as error:
                print(f"Entrada no válida: {error} Volvé a intentarlo.\n")
                continue
            if es_texto and resultado.empty:
                print(mensaje_sin_resultados(criterio, valor) + "\n")
                continue
            break

        print(f"\nPelículas encontradas: {len(resultado)}")
        if resultado.empty:
            print(mensaje_sin_resultados(criterio, valor))
        else:
            print(resultado.to_string(index=False))

        resultado.to_csv(ruta_resultado, index=False, encoding="utf-8-sig")
        print(f"Resultado guardado en: {ruta_resultado.resolve()}\n")
