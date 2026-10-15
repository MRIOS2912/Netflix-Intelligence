from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


# ============================================================
# NETFLIX INTELLIGENCE
# ANÁLISIS ESTADÍSTICO DE LAS EDADES
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
# PREPARACIÓN Y VALIDACIÓN DE LOS DATOS
# ============================================================

edad_original = pd.to_numeric(
    usuarios["age"],
    errors="coerce"
)

total_registros = len(usuarios)

edades_faltantes = int(edad_original.isna().sum())

edades_fuera_rango = int(
    (
        ~edad_original.between(0, 100)
        & edad_original.notna()
    ).sum()
)

edades_validas = edad_original[
    edad_original.between(0, 100)
].dropna()

if edades_validas.empty:
    raise ValueError(
        "No hay edades válidas entre 0 y 100 años."
    )


# ============================================================
# ESTADÍSTICAS DESCRIPTIVAS
# ============================================================

cantidad_validas = int(edades_validas.count())

media = edades_validas.mean()
mediana = edades_validas.median()
modas = edades_validas.mode().tolist()
varianza = edades_validas.var()
desviacion = edades_validas.std()
minimo = edades_validas.min()
maximo = edades_validas.max()

primer_cuartil = edades_validas.quantile(0.25)
tercer_cuartil = edades_validas.quantile(0.75)

rango = maximo - minimo
rango_intercuartilico = tercer_cuartil - primer_cuartil

coeficiente_variacion = (
    desviacion / media * 100
    if media != 0
    else float("nan")
)


# ============================================================
# FUNCIONES DE FORMATO
# ============================================================

def formato_entero(numero):
    """Formato entero con punto como separador de miles."""
    return f"{int(numero):,}".replace(",", ".")


def formato_decimal(numero, decimales=2):
    """Formato decimal con coma."""
    return f"{numero:,.{decimales}f}".replace(
        ",", "X"
    ).replace(
        ".", ","
    ).replace(
        "X", "."
    )


# ============================================================
# PALETA VISUAL
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
# GRÁFICA 1: HISTOGRAMA DE EDADES
# ============================================================

fig1, ax1 = plt.subplots(figsize=(11, 6))

fig1.patch.set_facecolor(FONDO)
ax1.set_facecolor(PANEL)

conteos, limites, barras = ax1.hist(
    edades_validas,
    bins=15,
    edgecolor=FONDO,
    linewidth=0.8,
    rwidth=0.88
)

for i, barra in enumerate(barras):
    barra.set_facecolor(
        ROJOS[i % len(ROJOS)]
    )

ax1.set_title(
    "Distribución de edades de los usuarios",
    color=BLANCO,
    fontsize=15,
    fontweight="bold",
    loc="left",
    pad=15
)

ax1.set_xlabel(
    "Edad (años)",
    color=GRIS
)

ax1.set_ylabel(
    "Número de usuarios",
    color=GRIS
)

ax1.tick_params(
    colors=GRIS,
    labelsize=10
)

ax1.yaxis.set_major_locator(
    MaxNLocator(integer=True)
)

for borde in ax1.spines.values():
    borde.set_color(GRIS_OSCURO)

ax1.grid(
    axis="y",
    color=GRIS_OSCURO,
    linestyle="--",
    alpha=0.5
)

ax1.set_axisbelow(True)

fig1.text(
    0.03,
    0.025,
    "Fuente: conjunto de datos sintético. "
    "Se excluyeron las edades ausentes y las edades "
    "fuera del rango de 0 a 100 años.",
    color=GRIS,
    fontsize=8
)

fig1.tight_layout(rect=[0.02, 0.06, 0.98, 0.98])

fig1.savefig(
    CARPETA_RESULTADOS / "01_distribucion_edades.png",
    dpi=300,
    facecolor=FONDO,
    bbox_inches="tight"
)


# ============================================================
# GRÁFICA 2: DIAGRAMA DE CAJA
# ============================================================

fig2, ax2 = plt.subplots(figsize=(11, 5))

fig2.patch.set_facecolor(FONDO)
ax2.set_facecolor(PANEL)

ax2.boxplot(
    edades_validas,
    vert=False,
    patch_artist=True,
    widths=0.45,
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
        "markersize": 3,
        "alpha": 0.8
    }
)

ax2.set_title(
    "Dispersión y posibles valores atípicos",
    color=BLANCO,
    fontsize=15,
    fontweight="bold",
    loc="left",
    pad=15
)

ax2.set_xlabel(
    "Edad (años)",
    color=GRIS
)

ax2.set_yticks([])

ax2.tick_params(
    colors=GRIS,
    labelsize=10
)

for borde in ax2.spines.values():
    borde.set_color(GRIS_OSCURO)

ax2.grid(
    axis="x",
    color=GRIS_OSCURO,
    linestyle="--",
    alpha=0.5
)

ax2.set_axisbelow(True)

fig2.tight_layout()

fig2.savefig(
    CARPETA_RESULTADOS / "02_diagrama_caja_edades.png",
    dpi=300,
    facecolor=FONDO,
    bbox_inches="tight"
)


# ============================================================
# GRÁFICA 3: FRECUENCIA POR GRUPOS DE EDAD
# ============================================================

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

fig3, ax3 = plt.subplots(figsize=(12, 6))

fig3.patch.set_facecolor(FONDO)
ax3.set_facecolor(PANEL)

barras_grupos = ax3.bar(
    frecuencias.index.astype(str),
    frecuencias.values,
    color=[
        ROJOS[i % len(ROJOS)]
        for i in range(len(frecuencias))
    ],
    width=0.55,
    edgecolor=FONDO,
    linewidth=0.8
)

ax3.set_title(
    "Cantidad de usuarios por grupo de edad",
    color=BLANCO,
    fontsize=15,
    fontweight="bold",
    loc="left",
    pad=15
)

ax3.set_xlabel(
    "Grupo de edad (años)",
    color=GRIS
)

ax3.set_ylabel(
    "Número de usuarios",
    color=GRIS
)

ax3.tick_params(
    colors=GRIS,
    labelsize=9
)

ax3.yaxis.set_major_locator(
    MaxNLocator(integer=True)
)

for borde in ax3.spines.values():
    borde.set_color(GRIS_OSCURO)

ax3.grid(
    axis="y",
    color=GRIS_OSCURO,
    linestyle="--",
    alpha=0.5
)

ax3.set_axisbelow(True)

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
        fontsize=9
    )

fig3.tight_layout()

fig3.savefig(
    CARPETA_RESULTADOS / "03_grupos_edad.png",
    dpi=300,
    facecolor=FONDO,
    bbox_inches="tight"
)


# ============================================================
# GUARDAR ESTADÍSTICAS EN CSV
# ============================================================

estadisticas = pd.DataFrame({
    "medida": [
        "Total de registros",
        "Edades válidas",
        "Edades faltantes o no numéricas",
        "Edades fuera del rango de 0 a 100",
        "Media",
        "Mediana",
        "Moda",
        "Varianza",
        "Desviación estándar",
        "Edad mínima válida",
        "Edad máxima válida",
        "Rango",
        "Primer cuartil",
        "Tercer cuartil",
        "Rango intercuartílico",
        "Coeficiente de variación (%)"
    ],
    "valor": [
        total_registros,
        cantidad_validas,
        edades_faltantes,
        edades_fuera_rango,
        media,
        mediana,
        ", ".join(str(valor) for valor in modas),
        varianza,
        desviacion,
        minimo,
        maximo,
        rango,
        primer_cuartil,
        tercer_cuartil,
        rango_intercuartilico,
        coeficiente_variacion
    ]
})

estadisticas.to_csv(
    CARPETA_RESULTADOS / "estadisticas_edades.csv",
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# MOSTRAR RESULTADOS EN LA TERMINAL
# ============================================================

print("\n" + "=" * 60)
print("NETFLIX INTELLIGENCE")
print("ANÁLISIS ESTADÍSTICO DE LAS EDADES")
print("=" * 60)

print(f"Total de registros: {formato_entero(total_registros)}")
print(f"Edades válidas: {formato_entero(cantidad_validas)}")
print(f"Edades faltantes: {formato_entero(edades_faltantes)}")
print(f"Edades fuera del rango: {formato_entero(edades_fuera_rango)}")

print(f"\nMedia: {formato_decimal(media)} años")
print(f"Mediana: {formato_decimal(mediana)} años")
print(f"Moda: {', '.join(str(valor) for valor in modas)}")
print(f"Varianza: {formato_decimal(varianza)}")
print(f"Desviación estándar: {formato_decimal(desviacion)}")
print(f"Edad mínima válida: {formato_entero(minimo)} años")
print(f"Edad máxima válida: {formato_entero(maximo)} años")
print(f"Rango: {formato_decimal(rango)} años")
print(f"Primer cuartil: {formato_decimal(primer_cuartil)}")
print(f"Tercer cuartil: {formato_decimal(tercer_cuartil)}")
print(f"Rango intercuartílico: {formato_decimal(rango_intercuartilico)}")
print(
    "Coeficiente de variación: "
    f"{formato_decimal(coeficiente_variacion)} %"
)

print("\nFrecuencia por grupo de edad:")
print(frecuencias.to_string())

print("\nArchivos guardados en la carpeta resultados:")
print("- 01_distribucion_edades.png")
print("- 02_diagrama_caja_edades.png")
print("- 03_grupos_edad.png")
print("- estadisticas_edades.csv")

print("\nAnálisis terminado correctamente.")
print("=" * 60)

plt.show()