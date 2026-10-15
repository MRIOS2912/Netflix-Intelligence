
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# ==================================================
# NETFLIX INTELLIGENCE - ANALISIS DEL CATALOGO
# ==================================================

ruta = Path("data") / "movies.csv"
salida = Path("resultados")
salida.mkdir(exist_ok=True)

if not ruta.exists():
    raise FileNotFoundError(
        "No se encuentra data/movies.csv. "
        "Comprueba la carpeta del proyecto."
    )

peliculas = pd.read_csv(ruta)

# Se excluyen duplicados exactos solo en memoria; el CSV original se conserva.
_duplicados_exactos = int(peliculas.duplicated().sum())
if _duplicados_exactos:
    print(f"Filas duplicadas exactas excluidas del análisis: {_duplicados_exactos:,}")
peliculas = peliculas.drop_duplicates().copy()

columnas_necesarias = [
    "title",
    "content_type",
    "genre_primary",
    "release_year",
    "duration_minutes",
    "imdb_rating"
]

faltantes = [
    columna for columna in columnas_necesarias
    if columna not in peliculas.columns
]

if faltantes:
    raise ValueError(
        f"Faltan columnas necesarias: {faltantes}"
    )

# Convertir las variables numericas
for columna in [
    "release_year",
    "duration_minutes",
    "imdb_rating"
]:
    peliculas[columna] = pd.to_numeric(
        peliculas[columna],
        errors="coerce"
    )

# ==================================================
# PALETA Y ESTILO VISUAL
# ==================================================

FONDO = "#160D18"
PANEL = "#281A2B"
BLANCO = "#FFFFFF"
GRIS = "#C9C1CC"

ROJOS = [
    "#641018",
    "#8F0710",
    "#B20710",
    "#E50914",
    "#C21835",
    "#F04452",
    "#FF6875"
]

plt.rcParams["font.family"] = "DejaVu Sans"

fig = plt.figure(
    figsize=(16, 11),
    facecolor=FONDO
)

rejilla = fig.add_gridspec(
    3,
    2,
    height_ratios=[1, 1, 1.25],
    hspace=0.48,
    wspace=0.30
)

ax1 = fig.add_subplot(rejilla[0, 0])
ax2 = fig.add_subplot(rejilla[0, 1])
ax3 = fig.add_subplot(rejilla[1, 0])
ax4 = fig.add_subplot(rejilla[1, 1])
ax5 = fig.add_subplot(rejilla[2, :])

fig.suptitle(
    "NETFLIX INTELLIGENCE\n"
    "Analisis estadistico del catalogo",
    color=BLANCO,
    fontsize=21,
    fontweight="bold",
    y=0.98
)


def preparar_eje(ax, titulo):
    ax.set_facecolor(PANEL)

    ax.set_title(
        titulo,
        color=BLANCO,
        fontsize=12,
        fontweight="bold",
        loc="left",
        pad=10
    )

    ax.tick_params(
        colors=GRIS,
        labelsize=9
    )

    for borde in ax.spines.values():
        borde.set_color("#514153")

    ax.grid(
        axis="y",
        color="#514153",
        linestyle="--",
        alpha=0.4
    )

    ax.set_axisbelow(True)


def formato_entero(valor):
    return f"{int(valor):,}".replace(",", ".")


# ==================================================
# DICCIONARIO DE TIPOS DE CONTENIDO
# ==================================================

def traducir_tipo(valor):
    traducciones = {
        "movie": "Pelicula",
        "movies": "Pelicula",
        "film": "Pelicula",
        "tv show": "Serie",
        "tv series": "Serie",
        "series": "Serie",
        "documentary": "Documental",
        "stand-up comedy": "Comedia en vivo",
        "limited series": "Miniserie"
    }

    texto = str(valor).strip()
    return traducciones.get(texto.lower(), texto)


# ==================================================
# DICCIONARIO DE GENEROS
# ==================================================

traduccion_generos = {
    "Action": "Accion",
    "Adventure": "Aventura",
    "Animation": "Animacion",
    "Biography": "Biografia",
    "Comedy": "Comedia",
    "Crime": "Crimen",
    "Documentary": "Documental",
    "Drama": "Drama",
    "Family": "Familiar",
    "Fantasy": "Fantasia",
    "History": "Historia",
    "Horror": "Terror",
    "Music": "Musica",
    "Musical": "Musical",
    "Mystery": "Misterio",
    "Romance": "Romance",
    "Sci-Fi": "Ciencia ficcion",
    "Science Fiction": "Ciencia ficcion",
    "Sport": "Deportes",
    "Thriller": "Suspenso",
    "War": "Guerra",
    "Western": "Oeste",
    "Reality": "Telerrealidad",
    "Reality TV": "Telerrealidad",
    "Stand-up Comedy": "Comedia en vivo",
    "Talk Show": "Programa de entrevistas",
    "Kids": "Infantil",
    "Adventure Comedy": "Comedia de aventuras",
    "Action Comedy": "Comedia de accion"
}


def traducir_genero(valor):
    if pd.isna(valor):
        return "Sin dato"

    texto = str(valor).strip()

    # Mantener la traduccion conocida
    if texto in traduccion_generos:
        return traduccion_generos[texto]

    # Intentar reconocer variantes de mayusculas
    for original, traduccion in traduccion_generos.items():
        if texto.lower() == original.lower():
            return traduccion

    # Conservar el valor original si no se conoce
    return texto


# ==================================================
# 1. DISTRIBUCION POR TIPO DE CONTENIDO
# ==================================================

preparar_eje(
    ax1,
    "Distribucion por tipo de contenido"
)

tipos = (
    peliculas["content_type"]
    .dropna()
    .astype(str)
    .str.strip()
    .map(traducir_tipo)
    .value_counts()
)

tipos = tipos.groupby(level=0).sum().sort_values(
    ascending=False
)

barras = ax1.bar(
    tipos.index,
    tipos.values,
    color=[
        ROJOS[i % len(ROJOS)]
        for i in range(len(tipos))
    ],
    width=0.48
)

ax1.set_ylabel(
    "Cantidad de contenidos",
    color=GRIS
)

ax1.yaxis.set_major_locator(
    MaxNLocator(integer=True)
)

ax1.tick_params(axis="x", rotation=10)

for barra in barras:
    ax1.annotate(
        formato_entero(barra.get_height()),
        (
            barra.get_x() + barra.get_width() / 2,
            barra.get_height()
        ),
        xytext=(0, 4),
        textcoords="offset points",
        ha="center",
        color=BLANCO,
        fontsize=9
    )


# ==================================================
# 2. GENEROS MAS FRECUENTES EN ESPANOL
# ==================================================

preparar_eje(
    ax2,
    "Generos mas frecuentes"
)

generos_originales = (
    peliculas["genre_primary"]
    .dropna()
    .astype(str)
    .str.strip()
)

generos_espanol = generos_originales.map(
    traducir_genero
)

generos = (
    generos_espanol
    .value_counts()
    .head(8)
)

barras = ax2.barh(
    generos.index,
    generos.values,
    color=[
        ROJOS[i % len(ROJOS)]
        for i in range(len(generos))
    ],
    height=0.48
)

ax2.set_xlabel(
    "Cantidad de contenidos",
    color=GRIS
)

ax2.invert_yaxis()

for barra in barras:
    ax2.annotate(
        formato_entero(barra.get_width()),
        (
            barra.get_width(),
            barra.get_y() + barra.get_height() / 2
        ),
        xytext=(4, 0),
        textcoords="offset points",
        va="center",
        color=BLANCO,
        fontsize=8
    )


# ==================================================
# 3. DISTRIBUCION DE CALIFICACIONES IMDb
# ==================================================

preparar_eje(
    ax3,
    "Distribucion de calificaciones IMDb"
)

calificaciones = peliculas["imdb_rating"].dropna()

calificaciones = calificaciones[
    calificaciones.between(0, 10)
]

if not calificaciones.empty:
    ax3.hist(
        calificaciones,
        bins=12,
        color=ROJOS[3],
        edgecolor=FONDO,
        linewidth=0.8,
        rwidth=0.88
    )

    promedio = calificaciones.mean()

    ax3.axvline(
        promedio,
        color=ROJOS[6],
        linestyle="--",
        linewidth=2,
        label=(
            f"Promedio: {promedio:.2f}"
            .replace(".", ",")
        )
    )

    ax3.legend(
        facecolor=PANEL,
        labelcolor=BLANCO,
        frameon=False,
        fontsize=9
    )

ax3.set_xlabel(
    "Calificacion IMDb (0 a 10)",
    color=GRIS
)

ax3.set_ylabel(
    "Cantidad de contenidos",
    color=GRIS
)

ax3.yaxis.set_major_locator(
    MaxNLocator(integer=True)
)


# ==================================================
# 4. CONTENIDOS POR AÑO DE ESTRENO
# ==================================================

preparar_eje(
    ax4,
    "Contenidos por año de estreno"
)

anios = peliculas["release_year"].dropna()

anios = anios[
    anios.between(1900, 2030)
]

if not anios.empty:
    contenidos_anio = (
        anios.astype(int)
        .value_counts()
        .sort_index()
    )

    ax4.plot(
        contenidos_anio.index,
        contenidos_anio.values,
        color=ROJOS[5],
        linewidth=2,
        marker="o",
        markersize=3
    )

    ax4.fill_between(
        contenidos_anio.index,
        contenidos_anio.values,
        color=ROJOS[3],
        alpha=0.15
    )

ax4.set_xlabel(
    "Año de estreno",
    color=GRIS
)

ax4.set_ylabel(
    "Cantidad de contenidos",
    color=GRIS
)


# ==================================================
# 5. TABLA DE CONTENIDOS DESTACADOS
# LOS TITULOS ORIGINALES NO SE TRADUCEN
# ==================================================

preparar_eje(
    ax5,
    "Contenidos con mayores calificaciones IMDb"
)

tabla_datos = peliculas.loc[
    peliculas["imdb_rating"].between(0, 10),
    [
        "title",
        "content_type",
        "genre_primary",
        "release_year",
        "imdb_rating"
    ]
].copy()

tabla_datos = tabla_datos.dropna(
    subset=["title", "imdb_rating"]
)

tabla_datos["title"] = (
    tabla_datos["title"]
    .astype(str)
    .str.strip()
)

tabla_datos = tabla_datos[
    tabla_datos["title"] != ""
]

tabla_datos = tabla_datos.sort_values(
    ["imdb_rating", "title"],
    ascending=[False, True]
).head(10)

# Traducir tipo y genero, no el titulo
tabla_datos["content_type"] = (
    tabla_datos["content_type"]
    .apply(
        lambda x: traducir_tipo(x)
        if pd.notna(x)
        else "Sin dato"
    )
)

tabla_datos["genre_primary"] = (
    tabla_datos["genre_primary"]
    .apply(traducir_genero)
)

tabla_datos["release_year"] = (
    tabla_datos["release_year"]
    .apply(
        lambda x: str(int(x))
        if pd.notna(x)
        else "Sin dato"
    )
)

tabla_datos["imdb_rating"] = (
    tabla_datos["imdb_rating"]
    .apply(
        lambda x: f"{x:.1f}".replace(".", ",")
    )
)

tabla = tabla_datos.rename(
    columns={
        "title": "Titulo original",
        "content_type": "Tipo de contenido",
        "genre_primary": "Genero",
        "release_year": "Ano de estreno",
        "imdb_rating": "Calificacion IMDb"
    }
)

ax5.axis("off")

if not tabla.empty:
    tabla_grafica = ax5.table(
        cellText=tabla.values,
        colLabels=tabla.columns,
        cellLoc="left",
        colLoc="left",
        loc="center",
        colWidths=[
            0.31, 0.17, 0.19, 0.15, 0.18
        ]
    )

    tabla_grafica.auto_set_font_size(False)
    tabla_grafica.set_fontsize(8)
    tabla_grafica.scale(1, 1.55)

    for (fila, columna), celda in tabla_grafica.get_celld().items():
        celda.set_edgecolor("#514153")

        if fila == 0:
            celda.set_facecolor(ROJOS[2])
            celda.set_text_props(
                color=BLANCO,
                weight="bold"
            )
        else:
            celda.set_facecolor(
                PANEL if fila % 2 else FONDO
            )
            celda.set_text_props(
                color=BLANCO
            )
else:
    ax5.text(
        0.5,
        0.5,
        "No hay contenidos con calificaciones validas.",
        color=BLANCO,
        ha="center",
        va="center",
        transform=ax5.transAxes
    )


# ==================================================
# INDICADORES Y FUENTE
# ==================================================

total = len(peliculas)
total_calificaciones = len(calificaciones)

promedio_general = (
    calificaciones.mean()
    if not calificaciones.empty
    else float("nan")
)

texto_indicadores = (
    f"Total de contenidos: {formato_entero(total)}"
    f"    |    Con calificacion valida: "
    f"{formato_entero(total_calificaciones)}"
)

if pd.notna(promedio_general):
    texto_indicadores += (
        f"    |    Promedio IMDb: "
        f"{promedio_general:.2f}".replace(".", ",")
    )

fig.text(
    0.05,
    0.915,
    texto_indicadores,
    color=GRIS,
    fontsize=9
)

fig.text(
    0.04,
    0.015,
    "Fuente: conjunto de datos sintetico descargado de Kaggle. "
    "Los titulos se conservan en su idioma original.",
    color=GRIS,
    fontsize=8
)

fig.subplots_adjust(
    top=0.88,
    bottom=0.06,
    left=0.08,
    right=0.96
)

# Guardar grafica como imagen y PDF
fig.savefig(
    salida / "analisis_catalogo.png",
    dpi=250,
    facecolor=FONDO,
    bbox_inches="tight"
)

fig.savefig(
    salida / "analisis_catalogo.pdf",
    facecolor=FONDO,
    bbox_inches="tight"
)

plt.show()


# ==================================================
# RESUMEN EN LA TERMINAL
# ==================================================

print("=" * 55)
print("RESUMEN DEL ANALISIS DEL CATALOGO")
print("=" * 55)

print(
    f"\nTotal de contenidos: {formato_entero(total)}"
)

print(
    f"Contenidos con calificacion valida: "
    f"{formato_entero(total_calificaciones)}"
)

if pd.notna(promedio_general):
    print(
        f"Promedio de calificacion IMDb: "
        f"{promedio_general:.2f}"
    )

print("\nTipos de contenido:")
print(tipos)

print("\nGeneros mas frecuentes:")
print(generos)

print("\nDiez contenidos mejor calificados:")
if not tabla.empty:
    print(tabla.to_string(index=False))
else:
    print("No hay registros disponibles.")

print("\nArchivos guardados:")
print("- resultados/analisis_catalogo.png")
print("- resultados/analisis_catalogo.pdf")
