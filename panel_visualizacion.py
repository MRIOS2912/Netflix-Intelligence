
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


# ==========================================================
# NETFLIX INTELLIGENCE
# ANALISIS DE HABITOS DE VISUALIZACION
# ==========================================================

BASE = Path(__file__).resolve().parent
RUTA_DATOS = BASE / "data" / "watch_history.csv"
CARPETA_RESULTADOS = BASE / "resultados"
CARPETA_RESULTADOS.mkdir(exist_ok=True)

if not RUTA_DATOS.exists():
    raise FileNotFoundError(
        "No se encuentra data/watch_history.csv. "
        "Comprueba la carpeta del proyecto."
    )

historial = pd.read_csv(RUTA_DATOS)

# Se excluyen duplicados exactos en memoria.
# El archivo CSV original se conserva sin modificaciones.
_duplicados_exactos = int(historial.duplicated().sum())

if _duplicados_exactos:
    print(
        "Filas duplicadas exactas excluidas del analisis: "
        f"{_duplicados_exactos:,}".replace(",", ".")
    )

historial = historial.drop_duplicates().copy()


# ==========================================================
# PREPARACION DE VARIABLES NUMERICAS
# ==========================================================

columnas_numericas = [
    "watch_duration_minutes",
    "progress_percentage",
    "user_rating",
]

for columna in columnas_numericas:
    if columna in historial.columns:
        historial[columna] = pd.to_numeric(
            historial[columna], errors="coerce"
        )

if "watch_duration_minutes" not in historial.columns:
    raise ValueError(
        "Falta la columna watch_duration_minutes."
    )

if "progress_percentage" not in historial.columns:
    raise ValueError(
        "Falta la columna progress_percentage."
    )

duracion = historial["watch_duration_minutes"].dropna()
duracion = duracion[duracion >= 0]

avance = historial["progress_percentage"].dropna()
avance = avance[avance.between(0, 100)]


# ==========================================================
# PALETA VISUAL
# ==========================================================

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

fig, ejes = plt.subplots(2, 2, figsize=(16, 10))
fig.patch.set_facecolor(FONDO)

fig.suptitle(
    "NETFLIX INTELLIGENCE\n"
    "Habitos de visualizacion de los usuarios",
    fontsize=21,
    color=BLANCO,
    fontweight="bold",
    y=0.98,
)


# ==========================================================
# FUNCIONES AUXILIARES
# ==========================================================

def preparar_eje(ax, titulo):
    ax.set_facecolor(PANEL)

    ax.set_title(
        titulo,
        color=BLANCO,
        fontsize=12,
        fontweight="bold",
        loc="left",
        pad=12,
    )

    ax.tick_params(colors=GRIS, labelsize=9)

    for borde in ax.spines.values():
        borde.set_color(GRIS_OSCURO)

    ax.grid(
        axis="y",
        color=GRIS_OSCURO,
        linestyle="--",
        alpha=0.4,
    )

    ax.set_axisbelow(True)


def formato_numero(valor):
    return (
        f"{valor:,.1f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def formato_entero(valor):
    return f"{int(valor):,}".replace(",", ".")


def traducir_accion(valor):
    traducciones = {
        "started": "Iniciada",
        "completed": "Completada",
        "paused": "Pausada",
        "stopped": "Detenida",
        "abandoned": "Abandonada",
    }

    texto = str(valor).strip()
    return traducciones.get(texto.lower(), texto)


def traducir_dispositivo(valor):
    traducciones = {
        "Desktop": "Computador",
        "Laptop": "Portatil",
        "Tablet": "Tableta",
        "Mobile": "Celular",
        "Smart TV": "Televisor",
        "Gaming Console": "Consola",
    }

    texto = str(valor).strip()
    return traducciones.get(texto, texto)


def agregar_etiquetas_verticales(ax, barras):
    for barra in barras:
        altura = barra.get_height()

        ax.annotate(
            formato_entero(altura),
            (
                barra.get_x() + barra.get_width() / 2,
                altura,
            ),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            color=BLANCO,
            fontsize=8,
        )


def agregar_etiquetas_horizontales(ax, barras):
    for barra in barras:
        ancho = barra.get_width()

        ax.annotate(
            formato_entero(ancho),
            (
                ancho,
                barra.get_y() + barra.get_height() / 2,
            ),
            xytext=(4, 0),
            textcoords="offset points",
            va="center",
            color=BLANCO,
            fontsize=8,
        )


# ==========================================================
# GRAFICA 1: DISTRIBUCION DEL TIEMPO DE VISUALIZACION
# ==========================================================

ax = ejes[0, 0]

preparar_eje(
    ax,
    "Distribucion del tiempo de visualizacion",
)

if not duracion.empty:
    ax.hist(
        duracion,
        bins=20,
        color=ROJOS[3],
        edgecolor=FONDO,
        linewidth=0.8,
        rwidth=0.88,
    )

    ax.set_xlabel("Duracion (minutos)", color=GRIS)
    ax.set_ylabel("Numero de registros", color=GRIS)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
else:
    ax.text(
        0.5,
        0.5,
        "No hay duraciones validas",
        ha="center",
        va="center",
        transform=ax.transAxes,
        color=BLANCO,
    )


# ==========================================================
# GRAFICA 2: PORCENTAJE DE AVANCE
# ==========================================================

ax = ejes[0, 1]

preparar_eje(
    ax,
    "Distribucion del porcentaje de avance",
)

if not avance.empty:
    ax.hist(
        avance,
        bins=15,
        color=ROJOS[5],
        edgecolor=FONDO,
        linewidth=0.8,
        rwidth=0.88,
    )

    ax.set_xlabel("Avance de reproduccion (%)", color=GRIS)
    ax.set_ylabel("Numero de registros", color=GRIS)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
else:
    ax.text(
        0.5,
        0.5,
        "No hay porcentajes de avance validos",
        ha="center",
        va="center",
        transform=ax.transAxes,
        color=BLANCO,
    )


# ==========================================================
# GRAFICA 3: ACCIONES DE REPRODUCCION
# ==========================================================

ax = ejes[1, 0]

preparar_eje(
    ax,
    "Acciones registradas en las reproducciones",
)

if "action" in historial.columns:
    acciones = (
        historial["action"]
        .dropna()
        .astype(str)
        .str.strip()
        .value_counts()
    )

    acciones.index = [
        traducir_accion(valor)
        for valor in acciones.index
    ]

    acciones = (
        acciones.groupby(level=0)
        .sum()
        .sort_values(ascending=False)
    )

    barras = ax.bar(
        acciones.index,
        acciones.values,
        color=[
            ROJOS[i % len(ROJOS)]
            for i in range(len(acciones))
        ],
        width=0.58,
    )

    ax.set_ylabel("Numero de registros", color=GRIS)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.tick_params(axis="x", rotation=12, labelsize=8)

    agregar_etiquetas_verticales(ax, barras)

else:
    acciones = pd.Series(dtype="int64")

    ax.text(
        0.5,
        0.5,
        "No existe la columna de acciones",
        ha="center",
        va="center",
        transform=ax.transAxes,
        color=BLANCO,
    )


# ==========================================================
# GRAFICA 4: REPRODUCCIONES POR DISPOSITIVO
# ==========================================================

ax = ejes[1, 1]

preparar_eje(
    ax,
    "Reproducciones por dispositivo",
)

if "device_type" in historial.columns:
    dispositivos = (
        historial["device_type"]
        .dropna()
        .astype(str)
        .str.strip()
        .value_counts()
    )

    dispositivos.index = [
        traducir_dispositivo(valor)
        for valor in dispositivos.index
    ]

    dispositivos = (
        dispositivos.groupby(level=0)
        .sum()
        .sort_values(ascending=False)
    )

    barras = ax.barh(
        dispositivos.index,
        dispositivos.values,
        color=[
            ROJOS[i % len(ROJOS)]
            for i in range(len(dispositivos))
        ],
        height=0.52,
    )

    ax.set_xlabel("Numero de registros", color=GRIS)
    ax.set_ylabel("")
    ax.invert_yaxis()
    ax.tick_params(axis="y", labelsize=9)

    agregar_etiquetas_horizontales(ax, barras)

    maximo = dispositivos.max() if not dispositivos.empty else 0

    if maximo > 0:
        ax.set_xlim(0, maximo * 1.18)

else:
    dispositivos = pd.Series(dtype="int64")

    ax.text(
        0.5,
        0.5,
        "No existe la columna de dispositivos",
        ha="center",
        va="center",
        transform=ax.transAxes,
        color=BLANCO,
    )


# ==========================================================
# INDICADORES DESCRIPTIVOS
# ==========================================================

media_duracion = (
    duracion.mean() if not duracion.empty else float("nan")
)

mediana_duracion = (
    duracion.median() if not duracion.empty else float("nan")
)

media_avance = (
    avance.mean() if not avance.empty else float("nan")
)

total_registros = len(historial)

fig.text(
    0.05,
    0.91,
    f"Registros: {formato_entero(total_registros)}"
    f"   |   Duracion media: {formato_numero(media_duracion)} min"
    f"   |   Mediana: {formato_numero(mediana_duracion)} min"
    f"   |   Avance medio: {formato_numero(media_avance)} %",
    color=GRIS,
    fontsize=9,
)

fig.text(
    0.04,
    0.025,
    "Fuente: conjunto de datos sintetico descargado de Kaggle. "
    "Las graficas describen los registros disponibles y no "
    "representan datos oficiales de Netflix.",
    color=GRIS,
    fontsize=8,
)

plt.tight_layout(rect=[0.03, 0.06, 0.98, 0.88])


# ==========================================================
# GUARDAR RESULTADOS
# ==========================================================

fig.savefig(
    CARPETA_RESULTADOS / "habitos_visualizacion.png",
    dpi=250,
    facecolor=FONDO,
    bbox_inches="tight",
)

fig.savefig(
    CARPETA_RESULTADOS / "habitos_visualizacion.pdf",
    facecolor=FONDO,
    bbox_inches="tight",
)

plt.show()


# ==========================================================
# RESULTADOS NUMERICOS
# ==========================================================

print("=" * 55)
print("NETFLIX INTELLIGENCE")
print("ANALISIS DE HABITOS DE VISUALIZACION")
print("=" * 55)

print(f"Total de registros: {formato_entero(total_registros)}")
print(
    "Duplicados exactos excluidos: "
    f"{formato_entero(_duplicados_exactos)}"
)
print(f"Duracion media: {media_duracion:.2f} minutos")
print(f"Duracion mediana: {mediana_duracion:.2f} minutos")
print(f"Avance medio: {media_avance:.2f} %")

print("\nACCIONES REGISTRADAS:")
print(acciones)

print("\nREPRODUCCIONES POR DISPOSITIVO:")
print(dispositivos)

print("\nPanel guardado en la carpeta resultados.")
print("Archivos: habitos_visualizacion.png y habitos_visualizacion.pdf")
