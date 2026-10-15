from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


# ============================================================
# NETFLIX INTELLIGENCE - ANÁLISIS ESTADÍSTICO DE EDADES
# ============================================================

BASE = Path(__file__).resolve().parent
RUTA_DATOS = BASE / "data" / "users.csv"
CARPETA_RESULTADOS = BASE / "resultados"
CARPETA_RESULTADOS.mkdir(exist_ok=True)

if not RUTA_DATOS.exists():
    raise FileNotFoundError(
        f"No se encuentra el archivo: {RUTA_DATOS}\n"
        "Comprueba que users.csv esté dentro de la carpeta data."
    )

usuarios = pd.read_csv(RUTA_DATOS)

# Se excluyen duplicados exactos solo en memoria; el CSV original se conserva.
_duplicados_exactos = int(usuarios.duplicated().sum())
if _duplicados_exactos:
    print(f"Filas duplicadas exactas excluidas del análisis: {_duplicados_exactos:,}")
usuarios = usuarios.drop_duplicates().copy()

if "age" not in usuarios.columns:
    raise ValueError(
        "El archivo users.csv no contiene la columna 'age'."
    )


# ============================================================
# PREPARACIÓN Y VALIDACIÓN DE LAS EDADES
# ============================================================

edad_original = pd.to_numeric(
    usuarios["age"],
    errors="coerce"
)

edades_faltantes = int(edad_original.isna().sum())

edades_fuera_rango = int(
    (~edad_original.between(0, 100)).sum()
    - edad_original.isna().sum()
)

edades_validas = edad_original[
    edad_original.between(0, 100)
].dropna()

if edades_validas.empty:
    raise ValueError(
        "No existen edades válidas entre 0 y 100 años."
    )

total_usuarios = len(usuarios)
total_edades_validas = len(edades_validas)


# ============================================================
# ESTILO VISUAL
# ============================================================

FONDO = "#160D18"
PANEL = "#281A2B"
BLANCO = "#FFFFFF"
GRIS = "#C9C1CC"
GRIS_OSCURO = "#514153"

ROJOS = [
    "#641018",
    "#8F0710",
    "#B20710",
    "#E50914",
    "#C21835",
    "#F04452",
    "#FF6875",
]

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def formato_entero(numero):
    """Presenta cantidades con punto como separador de miles."""
    return f"{int(numero):,}".replace(",", ".")


def formato_decimal(numero, decimales=1):
    """Presenta decimales con coma."""
    return f"{numero:.{decimales}f}".replace(".", ",")


def crear_tarjeta(
    figura,
    x,
    y,
    ancho,
    alto,
    titulo,
    valor,
    detalle,
    color
):
    """Crea una tarjeta de indicadores estadísticos."""

    ax = figura.add_axes([x, y, ancho, alto])
    ax.set_facecolor(PANEL)
    ax.set_xticks([])
    ax.set_yticks([])

    for borde in ax.spines.values():
        borde.set_visible(False)

    ax.axhline(
        y=1,
        color=color,
        linewidth=4,
        clip_on=False
    )

    ax.text(
        0.06,
        0.76,
        titulo,
        transform=ax.transAxes,
        color=GRIS,
        fontsize=9
    )

    ax.text(
        0.06,
        0.39,
        valor,
        transform=ax.transAxes,
        color=color,
        fontsize=21,
        fontweight="bold"
    )

    ax.text(
        0.06,
        0.10,
        detalle,
        transform=ax.transAxes,
        color=GRIS,
        fontsize=7
    )


def preparar_grafica(ax, titulo):
    """Aplica el diseño común de las gráficas."""

    ax.set_facecolor(PANEL)

    ax.set_title(
        titulo,
        color=BLANCO,
        fontsize=12,
        fontweight="bold",
        loc="left",
        pad=12
    )

    ax.tick_params(
        colors=GRIS,
        labelsize=9
    )

    ax.xaxis.label.set_color(GRIS)
    ax.yaxis.label.set_color(GRIS)

    for borde in ax.spines.values():
        borde.set_color(GRIS_OSCURO)
        borde.set_linewidth(0.7)

    ax.grid(
        axis="y",
        color=GRIS_OSCURO,
        linestyle="--",
        linewidth=0.6,
        alpha=0.55
    )

    ax.set_axisbelow(True)


# ============================================================
# ESTADÍSTICAS DESCRIPTIVAS
# ============================================================

media = edades_validas.mean()
mediana = edades_validas.median()
modas = edades_validas.mode().tolist()
desviacion = edades_validas.std()
varianza = edades_validas.var()
edad_minima = edades_validas.min()
edad_maxima = edades_validas.max()

primer_cuartil = edades_validas.quantile(0.25)
tercer_cuartil = edades_validas.quantile(0.75)
rango_intercuartilico = tercer_cuartil - primer_cuartil


# ============================================================
# CREAR PANEL
# ============================================================

fig = plt.figure(
    figsize=(16, 10),
    facecolor=FONDO
)

fig.text(
    0.045,
    0.945,
    "NETFLIX INTELLIGENCE",
    color="#E50914",
    fontsize=25,
    fontweight="bold"
)

fig.text(
    0.045,
    0.900,
    "Análisis estadístico de las edades de los usuarios",
    color=BLANCO,
    fontsize=15
)

fig.text(
    0.955,
    0.945,
    "PROYECTO ACADÉMICO",
    color=GRIS,
    fontsize=9,
    ha="right"
)

fig.text(
    0.955,
    0.912,
    "Datos sintéticos",
    color="#FF6875",
    fontsize=9,
    ha="right"
)


# ============================================================
# TARJETAS DE INDICADORES
# ============================================================

crear_tarjeta(
    fig,
    0.045,
    0.755,
    0.21,
    0.095,
    "EDAD PROMEDIO",
    f"{formato_decimal(media)} años",
    "Media de las edades válidas",
    ROJOS[3]
)

crear_tarjeta(
    fig,
    0.275,
    0.755,
    0.21,
    0.095,
    "EDAD MEDIANA",
    f"{formato_entero(mediana)} años",
    "Valor central de la distribución",
    ROJOS[5]
)

crear_tarjeta(
    fig,
    0.505,
    0.755,
    0.21,
    0.095,
    "EDADES VÁLIDAS",
    formato_entero(total_edades_validas),
    "Incluidas en el análisis",
    ROJOS[2]
)

crear_tarjeta(
    fig,
    0.735,
    0.755,
    0.22,
    0.095,
    "EDADES FALTANTES",
    formato_entero(edades_faltantes),
    "Valores ausentes o no numéricos",
    ROJOS[6]
)


# ============================================================
# GRÁFICA 1: DISTRIBUCIÓN DE EDADES
# ============================================================

ax1 = fig.add_axes([0.07, 0.425, 0.42, 0.245])

preparar_grafica(
    ax1,
    "Distribución de edades"
)

conteos, limites, barras = ax1.hist(
    edades_validas,
    bins=15,
    edgecolor=FONDO,
    linewidth=0.8,
    rwidth=0.86
)

for i, barra in enumerate(barras):
    barra.set_facecolor(
        ROJOS[i % len(ROJOS)]
    )

ax1.set_xlabel("Edad (años)")
ax1.set_ylabel("Número de usuarios")
ax1.set_xlim(0, 100)

ax1.yaxis.set_major_locator(
    MaxNLocator(integer=True)
)


# ============================================================
# GRÁFICA 2: DIAGRAMA DE CAJA
# ============================================================

ax2 = fig.add_axes([0.55, 0.435, 0.39, 0.225])

preparar_grafica(
    ax2,
    "Dispersión y posibles valores atípicos"
)

ax2.boxplot(
    edades_validas,
    vert=False,
    patch_artist=True,
    widths=0.38,
    medianprops={
        "color": BLANCO,
        "linewidth": 2
    },
    boxprops={
        "facecolor": ROJOS[2],
        "color": ROJOS[4],
        "linewidth": 1.2
    },
    whiskerprops={
        "color": ROJOS[5],
        "linewidth": 1.2
    },
    capprops={
        "color": ROJOS[5],
        "linewidth": 1.2
    },
    flierprops={
        "marker": "o",
        "markerfacecolor": ROJOS[6],
        "markeredgecolor": ROJOS[6],
        "markersize": 2.5,
        "alpha": 0.8
    }
)

ax2.set_xlabel("Edad (años)")
ax2.set_xlim(0, 100)
ax2.set_yticks([])


# ============================================================
# GRÁFICA 3: CANTIDAD POR GRUPO DE EDAD
# ============================================================

ax3 = fig.add_axes([0.07, 0.115, 0.87, 0.225])

preparar_grafica(
    ax3,
    "Cantidad de usuarios por grupo de edad"
)

limites_grupos = [
    0, 18, 25, 35, 45, 55, 65, 101
]

etiquetas_grupos = [
    "0-17",
    "18-24",
    "25-34",
    "35-44",
    "45-54",
    "55-64",
    "65 o más"
]

grupos = pd.cut(
    edades_validas,
    bins=limites_grupos,
    labels=etiquetas_grupos,
    right=False
)

frecuencias = grupos.value_counts(
    sort=False
).reindex(
    etiquetas_grupos,
    fill_value=0
)

barras_grupos = ax3.bar(
    frecuencias.index,
    frecuencias.values,
    color=[
        ROJOS[i % len(ROJOS)]
        for i in range(len(frecuencias))
    ],
    width=0.48,
    edgecolor=FONDO,
    linewidth=0.8
)

ax3.set_xlabel("Grupo de edad (años)")
ax3.set_ylabel("Número de usuarios")

ax3.yaxis.set_major_locator(
    MaxNLocator(integer=True)
)

for barra in barras_grupos:
    altura = barra.get_height()

    ax3.annotate(
        formato_entero(altura),
        (
            barra.get_x() + barra.get_width() / 2,
            altura
        ),
        xytext=(0, 4),
        textcoords="offset points",
        ha="center",
        color=BLANCO,
        fontsize=8
    )


# ============================================================
# NOTA METODOLÓGICA
# ============================================================

fig.text(
    0.045,
    0.045,
    "Fuente: conjunto de datos sintético descargado de Kaggle. "
    "Se excluyeron las edades ausentes y las edades fuera del "
    "rango de 0 a 100 años.",
    color=GRIS,
    fontsize=8
)

fig.text(
    0.955,
    0.020,
    "NETFLIX INTELLIGENCE | ANÁLISIS CUANTITATIVO",
    color="#FF6875",
    fontsize=8,
    ha="right"
)


# ============================================================
# EXPORTAR GRÁFICAS
# ============================================================

archivo_png = (
    CARPETA_RESULTADOS / "dashboard_edades.png"
)

archivo_pdf = (
    CARPETA_RESULTADOS / "dashboard_edades.pdf"
)

fig.savefig(
    archivo_png,
    dpi=250,
    facecolor=FONDO,
    bbox_inches="tight"
)

fig.savefig(
    archivo_pdf,
    facecolor=FONDO,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# MOSTRAR RESULTADOS EN LA TERMINAL
# ============================================================

print("\n" + "=" * 55)
print("NETFLIX INTELLIGENCE")
print("ANÁLISIS ESTADÍSTICO DE LAS EDADES")
print("=" * 55)

print(
    f"Total de registros: {formato_entero(total_usuarios)}"
)

print(
    f"Edades válidas: {formato_entero(total_edades_validas)}"
)

print(
    f"Edades faltantes o no numéricas: "
    f"{formato_entero(edades_faltantes)}"
)

print(
    f"Edades fuera del rango de 0 a 100: "
    f"{formato_entero(edades_fuera_rango)}"
)

print(
    f"Edad promedio: {formato_decimal(media, 2)} años"
)

print(
    f"Edad mediana: {formato_decimal(mediana, 2)} años"
)

print(
    f"Moda: {', '.join(str(valor) for valor in modas)}"
)

print(
    f"Desviación estándar: {formato_decimal(desviacion, 2)}"
)

print(
    f"Varianza: {formato_decimal(varianza, 2)}"
)

print(
    f"Edad mínima válida: {formato_entero(edad_minima)} años"
)

print(
    f"Edad máxima válida: {formato_entero(edad_maxima)} años"
)

print(
    f"Primer cuartil: {formato_decimal(primer_cuartil, 2)}"
)

print(
    f"Tercer cuartil: {formato_decimal(tercer_cuartil, 2)}"
)

print(
    "Rango intercuartílico: "
    f"{formato_decimal(rango_intercuartilico, 2)}"
)

print("\nArchivos generados:")
print(archivo_png)
print(archivo_pdf)

print("\nAnálisis de edades terminado.")
print("=" * 55)