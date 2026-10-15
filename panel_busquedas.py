from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ==========================================================
# NETFLIX INTELLIGENCE
# Panel estadistico de busquedas de los usuarios
# ==========================================================

BASE = Path(__file__).resolve().parent
ARCHIVO = BASE / "data" / "search_logs.csv"
CARPETA_RESULTADOS = BASE / "resultados"
CARPETA_RESULTADOS.mkdir(exist_ok=True)

if not ARCHIVO.exists():
    raise FileNotFoundError(
        f"No se encontro el archivo: {ARCHIVO}\n"
        "Verifica que search_logs.csv este dentro de data."
    )

busquedas = pd.read_csv(ARCHIVO)

# Registrar duplicados antes de excluirlos.
duplicados_exactos = int(busquedas.duplicated().sum())

# Excluir duplicados exactos solo en memoria.
# El CSV original se conserva sin modificaciones.
if duplicados_exactos:
    print(
        "Filas duplicadas exactas excluidas del analisis: "
        f"{duplicados_exactos:,}".replace(",", ".")
    )

busquedas = busquedas.drop_duplicates().copy()


# ==========================================================
# COLORES Y CONFIGURACION VISUAL
# ==========================================================

ROJOS = [
    "#590D16",
    "#800D19",
    "#A30D20",
    "#C1122F",
    "#E50914",
    "#F04455",
    "#FF7180",
    "#FF9BA5",
]

FONDO = "#140B16"
PANEL = "#281A2B"
TEXTO = "#F8F2F7"
TEXTO_SUAVE = "#C8B9CA"
LINEA = "#49374B"

plt.rcParams.update({
    "figure.facecolor": FONDO,
    "axes.facecolor": PANEL,
    "axes.edgecolor": LINEA,
    "axes.labelcolor": TEXTO_SUAVE,
    "xtick.color": TEXTO_SUAVE,
    "ytick.color": TEXTO_SUAVE,
    "text.color": TEXTO,
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.titleweight": "bold",
    "axes.titlesize": 12,
})


# ==========================================================
# FUNCIONES DE TRADUCCION
# ==========================================================

def traducir_dispositivo(valor):
    traducciones = {
        "Mobile": "Celular",
        "Smart TV": "Televisor",
        "Tablet": "Tableta",
        "Laptop": "Portatil",
        "Desktop": "Computador",
        "Gaming Console": "Consola de videojuegos",
    }

    texto = str(valor).strip()
    return traducciones.get(texto, texto)


def traducir_pais(valor):
    traducciones = {
        "USA": "Estados Unidos",
        "United States": "Estados Unidos",
        "Canada": "Canada",
        "United Kingdom": "Reino Unido",
    }

    texto = str(valor).strip()
    return traducciones.get(texto, texto)


def traducir_booleano(valor):
    if pd.isna(valor):
        return "Sin dato"

    if isinstance(valor, (bool, np.bool_)):
        return "Si" if valor else "No"

    texto = str(valor).strip().lower()

    if texto in ("true", "1", "yes", "si", "sí"):
        return "Si"

    if texto in ("false", "0", "no"):
        return "No"

    return "Sin dato"


def traducir_consulta(valor):
    """
    Traduce consultas conocidas solo para mostrarlas
    en la grafica. El CSV original no se modifica.
    """
    traducciones = {
        "stand up comedy": "Comedia en vivo",
        "comedy shows": "Programas de comedia",
        "sci-fi": "Ciencia ficcion",
        "classic movies": "Peliculas clasicas",
        "superhero movies": "Peliculas de superheroes",
        "feel documentaries": "Documentales",
        "new releases": "Estrenos recientes",
        "drama series": "Series dramaticas",
        "horror movies": "Peliculas de terror",
        "family movies": "Peliculas familiares",
        "drama movies": "Peliculas dramaticas",
        "action movies": "Peliculas de accion",
        "romantic movies": "Peliculas romanticas",
        "thriller movies": "Peliculas de suspenso",
        "animated movies": "Peliculas animadas",
        "documentaries": "Documentales",
        "kids shows": "Programas infantiles",
        "crime series": "Series policiacas",
        "reality shows": "Programas de telerrealidad",
        "new movies": "Peliculas nuevas",
        "comedy movies": "Peliculas de comedia",
        "action series": "Series de accion",
        "romantic comedies": "Comedias romanticas",
        "popular movies": "Peliculas populares",
        "popular series": "Series populares",
    }

    texto = str(valor).strip()
    return traducciones.get(texto.lower(), texto)


def formato_entero(numero):
    return f"{int(numero):,}".replace(",", ".")


def estilo_ejes(ax, eje="y"):
    ax.grid(
        axis=eje,
        color=LINEA,
        linestyle="--",
        linewidth=0.6,
        alpha=0.65,
    )

    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(LINEA)
    ax.spines["bottom"].set_color(LINEA)
    ax.tick_params(axis="both", labelsize=8)


def agregar_etiquetas(ax, barras, horizontal=False):
    for barra in barras:
        valor = barra.get_width() if horizontal else barra.get_height()
        etiqueta = formato_entero(valor)

        if horizontal:
            ax.annotate(
                etiqueta,
                (valor, barra.get_y() + barra.get_height() / 2),
                xytext=(4, 0),
                textcoords="offset points",
                va="center",
                ha="left",
                fontsize=8,
                color=TEXTO,
            )
        else:
            ax.annotate(
                etiqueta,
                (barra.get_x() + barra.get_width() / 2, valor),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                fontsize=8,
                color=TEXTO,
            )


# ==========================================================
# PREPARACION DE LOS DATOS
# ==========================================================

total_registros = len(busquedas)

if "search_query" in busquedas.columns:
    consultas = (
        busquedas["search_query"]
        .dropna()
        .astype(str)
        .str.strip()
    )
    consultas = consultas[consultas != ""]
else:
    consultas = pd.Series(dtype="object")

if "search_date" in busquedas.columns:
    fechas = pd.to_datetime(
        busquedas["search_date"], errors="coerce"
    )
    busquedas["_fecha_mes"] = fechas.dt.to_period("M").astype(str)
    busquedas.loc[fechas.isna(), "_fecha_mes"] = np.nan
else:
    busquedas["_fecha_mes"] = np.nan

if "device_type" in busquedas.columns:
    dispositivos = (
        busquedas["device_type"]
        .fillna("Sin dato")
        .map(traducir_dispositivo)
        .value_counts()
    )
else:
    dispositivos = pd.Series(dtype="int64")

if "had_typo" in busquedas.columns:
    errores_escritura = (
        busquedas["had_typo"]
        .map(traducir_booleano)
        .value_counts()
        .reindex(["Si", "No", "Sin dato"], fill_value=0)
    )
else:
    errores_escritura = pd.Series(dtype="int64")

if "used_filters" in busquedas.columns:
    filtros = (
        busquedas["used_filters"]
        .map(traducir_booleano)
        .value_counts()
        .reindex(["Si", "No", "Sin dato"], fill_value=0)
    )
else:
    filtros = pd.Series(dtype="int64")

if "location_country" in busquedas.columns:
    paises = (
        busquedas["location_country"]
        .fillna("Sin dato")
        .map(traducir_pais)
        .value_counts()
    )
else:
    paises = pd.Series(dtype="int64")

if "user_id" in busquedas.columns:
    usuarios_unicos = busquedas["user_id"].nunique()
else:
    usuarios_unicos = None


# ==========================================================
# CREACION DEL PANEL
# ==========================================================

fig = plt.figure(figsize=(16, 10), facecolor=FONDO)

fig.text(
    0.5, 0.965,
    "NETFLIX INTELLIGENCE",
    ha="center",
    fontsize=22,
    fontweight="bold",
    color="#E50914",
)

fig.text(
    0.5, 0.925,
    "Habitos de busqueda y preferencias de los usuarios",
    ha="center",
    fontsize=15,
    fontweight="bold",
    color=TEXTO,
)

texto_usuarios = (
    f" | Usuarios identificados: {formato_entero(usuarios_unicos)}"
    if usuarios_unicos is not None else ""
)

fig.text(
    0.5, 0.888,
    f"Registros: {formato_entero(total_registros)}"
    + texto_usuarios
    + " | Analisis descriptivo de busquedas",
    ha="center",
    fontsize=9,
    color=TEXTO_SUAVE,
)


# ==========================================================
# GRAFICA 1: CONSULTAS MAS FRECUENTES
# ==========================================================

ax1 = fig.add_axes([0.12, 0.55, 0.35, 0.27])

if not consultas.empty:
    frecuencias_consultas = consultas.value_counts().head(10)
    frecuencias_consultas.index = [
        traducir_consulta(x)
        for x in frecuencias_consultas.index
    ]

    top_consultas = (
        frecuencias_consultas.groupby(level=0)
        .sum()
        .sort_values()
    )

    barras = ax1.barh(
        top_consultas.index,
        top_consultas.values,
        color=[
            ROJOS[i % len(ROJOS)]
            for i in range(len(top_consultas))
        ],
        height=0.62,
    )

    agregar_etiquetas(ax1, barras, horizontal=True)
    ax1.set_title(
        "Terminos de busqueda mas frecuentes",
        loc="left",
        pad=12,
    )
    ax1.set_xlabel("Cantidad de busquedas")
    ax1.set_ylabel("")
    ax1.tick_params(axis="y", labelsize=8)
    ax1.set_xlim(0, max(top_consultas.values) * 1.20)
    estilo_ejes(ax1)
else:
    ax1.text(
        0.5, 0.5, "No hay datos de busqueda disponibles",
        ha="center", va="center", transform=ax1.transAxes,
    )


# ==========================================================
# GRAFICA 2: BUSQUEDAS POR DISPOSITIVO
# ==========================================================

ax2 = fig.add_axes([0.55, 0.55, 0.38, 0.27])

if not dispositivos.empty:
    dispositivos = dispositivos.sort_values()

    barras = ax2.barh(
        dispositivos.index,
        dispositivos.values,
        color=[
            ROJOS[i % len(ROJOS)]
            for i in range(len(dispositivos))
        ],
        height=0.55,
    )

    agregar_etiquetas(ax2, barras, horizontal=True)
    ax2.set_title("Busquedas por dispositivo", loc="left", pad=12)
    ax2.set_xlabel("Cantidad de registros")
    ax2.set_ylabel("")
    ax2.set_xlim(0, max(dispositivos.values) * 1.20)
    ax2.tick_params(axis="y", labelsize=8)
    estilo_ejes(ax2)
else:
    ax2.text(
        0.5, 0.5, "No hay datos de dispositivos",
        ha="center", va="center", transform=ax2.transAxes,
    )


# ==========================================================
# GRAFICA 3: EVOLUCION MENSUAL
# ==========================================================

ax3 = fig.add_axes([0.07, 0.16, 0.39, 0.28])

evolucion = (
    busquedas["_fecha_mes"]
    .dropna()
    .value_counts()
    .sort_index()
)

if not evolucion.empty:
    posiciones = np.arange(len(evolucion))

    ax3.plot(
        posiciones,
        evolucion.values,
        color="#FF5264",
        linewidth=2,
        marker="o",
        markersize=3.5,
    )

    ax3.fill_between(
        posiciones,
        evolucion.values,
        color="#E50914",
        alpha=0.15,
    )

    paso = max(1, len(evolucion) // 8)

    ax3.set_xticks(posiciones[::paso])
    ax3.set_xticklabels(
        evolucion.index[::paso],
        rotation=35,
        ha="right",
        fontsize=8,
    )

    ax3.set_title(
        "Evolucion mensual de las busquedas",
        loc="left",
        pad=12,
    )
    ax3.set_ylabel("Cantidad de registros")
    ax3.set_xlabel("Mes")
    estilo_ejes(ax3)
else:
    ax3.text(
        0.5, 0.5, "No hay fechas validas para mostrar",
        ha="center", va="center", transform=ax3.transAxes,
    )


# ==========================================================
# GRAFICA 4: ERRORES DE ESCRITURA
# ==========================================================

ax4 = fig.add_axes([0.55, 0.16, 0.18, 0.28])

if not errores_escritura.empty:
    valores = errores_escritura[errores_escritura > 0]

    barras = ax4.bar(
        valores.index,
        valores.values,
        color=ROJOS[:len(valores)],
        width=0.55,
    )

    agregar_etiquetas(ax4, barras)
    ax4.set_title("Errores de escritura", loc="left", pad=12)
    ax4.set_ylabel("Registros")
    ax4.set_xlabel("¿Hubo errores?")
    ax4.tick_params(axis="x", rotation=0, labelsize=8)
    estilo_ejes(ax4)
else:
    ax4.text(
        0.5, 0.5, "Variable no disponible",
        ha="center", va="center", transform=ax4.transAxes,
    )


# ==========================================================
# GRAFICA 5: USO DE FILTROS
# ==========================================================

ax5 = fig.add_axes([0.78, 0.16, 0.15, 0.28])

if not filtros.empty:
    valores = filtros[filtros > 0]

    barras = ax5.bar(
        valores.index,
        valores.values,
        color=ROJOS[:len(valores)],
        width=0.55,
    )

    agregar_etiquetas(ax5, barras)
    ax5.set_title("Uso de filtros", loc="left", pad=12)
    ax5.set_ylabel("Registros")
    ax5.set_xlabel("¿Uso filtros?")
    ax5.tick_params(axis="x", rotation=0, labelsize=8)
    estilo_ejes(ax5)
else:
    ax5.text(
        0.5, 0.5, "Variable no disponible",
        ha="center", va="center", transform=ax5.transAxes,
    )


# ==========================================================
# PIE DE PAGINA
# ==========================================================

fig.text(
    0.5, 0.055,
    "Fuente: conjunto de datos sintetico descargado de Kaggle. "
    "Los resultados describen los registros disponibles y no "
    "representan datos oficiales de Netflix.",
    ha="center",
    fontsize=8,
    color=TEXTO_SUAVE,
)

fig.text(
    0.5, 0.032,
    "NETFLIX INTELLIGENCE | Proyecto academico de analisis cuantitativo",
    ha="center",
    fontsize=8,
    color="#FF5264",
)


# ==========================================================
# GUARDAR Y MOSTRAR RESULTADOS
# ==========================================================

archivo_grafica = CARPETA_RESULTADOS / "panel_busquedas.png"

fig.savefig(
    archivo_grafica,
    dpi=200,
    facecolor=FONDO,
    bbox_inches="tight",
)

plt.show()

print("\n" + "=" * 55)
print("PANEL DE BUSQUEDAS GENERADO CORRECTAMENTE")
print("=" * 55)
print(f"Registros analizados: {formato_entero(total_registros)}")
print(f"Terminos de busqueda validos: {formato_entero(len(consultas))}")
print(f"Filas duplicadas exactas excluidas: {formato_entero(duplicados_exactos)}")
print(f"Imagen guardada en: {archivo_grafica}")
print("Las traducciones se aplicaron solo a las visualizaciones.")
print("=" * 55)
