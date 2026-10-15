
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# =====================================================
# NETFLIX INTELLIGENCE - PANEL DE RESENAS
# =====================================================

ruta = Path("data") / "reviews.csv"
salida = Path("resultados")
salida.mkdir(exist_ok=True)

if not ruta.exists():
    raise FileNotFoundError("No se encuentra data/reviews.csv")

df = pd.read_csv(ruta)

# Registrar duplicados antes de excluirlos.
duplicados = int(df.duplicated().sum())

# Se excluyen duplicados exactos solo en memoria.
# El CSV original se conserva sin modificaciones.
if duplicados:
    print(
        "Filas duplicadas exactas excluidas del análisis: "
        f"{duplicados:,}"
    )

df = df.drop_duplicates().copy()

# Preparar variables
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["sentiment_score"] = pd.to_numeric(
    df["sentiment_score"], errors="coerce"
)
df["helpful_votes"] = pd.to_numeric(
    df["helpful_votes"], errors="coerce"
)
df["total_votes"] = pd.to_numeric(
    df["total_votes"], errors="coerce"
)
df["review_date"] = pd.to_datetime(
    df["review_date"], errors="coerce"
)

# =====================================================
# TRADUCCIONES
# =====================================================

sentimientos = {
    "positive": "Positivo",
    "neutral": "Neutral",
    "negative": "Negativo"
}

dispositivos = {
    "Mobile": "Celular",
    "Smart TV": "Televisor inteligente",
    "Tablet": "Tableta",
    "Laptop": "Portatil",
    "Desktop": "Computador de mesa",
    "Gaming Console": "Consola de videojuegos"
}

df["sentimiento_es"] = (
    df["sentiment"].astype(str).str.lower().map(sentimientos)
    .fillna("Sin clasificar")
)

df["dispositivo_es"] = (
    df["device_type"].astype(str).str.strip().map(dispositivos)
    .fillna(df["device_type"].astype(str))
)

# =====================================================
# ESTILO VISUAL
# =====================================================

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

fig = plt.figure(figsize=(16, 11), facecolor=FONDO)

rejilla = fig.add_gridspec(
    3, 2,
    height_ratios=[0.65, 1.2, 1.2],
    hspace=0.48,
    wspace=0.30
)

ax1 = fig.add_subplot(rejilla[1, 0])
ax2 = fig.add_subplot(rejilla[1, 1])
ax3 = fig.add_subplot(rejilla[2, 0])
ax4 = fig.add_subplot(rejilla[2, 1])

fig.suptitle(
    "NETFLIX INTELLIGENCE\nAnalisis estadistico de resenas",
    fontsize=22,
    color=BLANCO,
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
    ax.tick_params(colors=GRIS, labelsize=9)

    for borde in ax.spines.values():
        borde.set_color("#514153")

    ax.grid(
        axis="y",
        color="#514153",
        linestyle="--",
        alpha=0.4
    )
    ax.set_axisbelow(True)


def entero(numero):
    return f"{int(numero):,}".replace(",", ".")


# =====================================================
# TARJETAS DE INDICADORES
# =====================================================

total = len(df)
promedio = df["rating"].mean()
mediana = df["rating"].median()
faltantes_texto = int(df["review_text"].isna().sum())

positivas = int((df["sentiment"].str.lower() == "positive").sum())
neutrales = int((df["sentiment"].str.lower() == "neutral").sum())
negativas = int((df["sentiment"].str.lower() == "negative").sum())

verificadas = int(df["is_verified_watch"].eq(True).sum())
no_verificadas = int(df["is_verified_watch"].eq(False).sum())

tarjetas = [
    ("TOTAL DE RESENAS", entero(total), "Registros del archivo"),
    (
        "CALIFICACION PROMEDIO",
        f"{promedio:.2f}/5".replace(".", ","),
        "Escala de 1 a 5"
    ),
    (
        "SENTIMIENTO POSITIVO",
        f"{positivas / total * 100:.1f}%".replace(".", ","),
        f"{entero(positivas)} resenas"
    ),
    (
        "REPRODUCCIONES VERIFICADAS",
        f"{verificadas / total * 100:.1f}%".replace(".", ","),
        f"{entero(verificadas)} registros"
    )
]

for i, (titulo, valor, subtitulo) in enumerate(tarjetas):
    x = 0.055 + i * 0.23

    fig.text(
        x, 0.865, titulo,
        color=GRIS, fontsize=9
    )

    fig.text(
        x, 0.817, valor,
        color=ROJOS[[3, 5, 6, 2][i]],
        fontsize=21,
        fontweight="bold"
    )

    fig.text(
        x, 0.785, subtitulo,
        color=GRIS, fontsize=8
    )

# =====================================================
# 1. DISTRIBUCION DEL SENTIMIENTO
# =====================================================

preparar_eje(ax1, "Distribucion de sentimientos")

orden = ["Positivo", "Neutral", "Negativo"]
conteo = df["sentimiento_es"].value_counts()
conteo = conteo.reindex(orden, fill_value=0)

barras = ax1.bar(
    conteo.index,
    conteo.values,
    color=[ROJOS[5], ROJOS[2], ROJOS[0]],
    width=0.48
)

ax1.set_ylabel("Cantidad de resenas", color=GRIS)
ax1.yaxis.set_major_locator(MaxNLocator(integer=True))

for barra in barras:
    ax1.annotate(
        entero(barra.get_height()),
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

# =====================================================
# 2. DISTRIBUCION DE CALIFICACIONES
# =====================================================

preparar_eje(ax2, "Distribucion de calificaciones")

calificaciones = df["rating"].dropna()
calificaciones = calificaciones[calificaciones.between(1, 5)]

conteo_rating = (
    calificaciones.astype(int)
    .value_counts()
    .reindex([1, 2, 3, 4, 5], fill_value=0)
)

barras = ax2.bar(
    conteo_rating.index.astype(str),
    conteo_rating.values,
    color=ROJOS[:5],
    width=0.48
)

ax2.set_xlabel("Calificacion (1 a 5)", color=GRIS)
ax2.set_ylabel("Cantidad de resenas", color=GRIS)
ax2.yaxis.set_major_locator(MaxNLocator(integer=True))

for barra in barras:
    ax2.annotate(
        entero(barra.get_height()),
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

# =====================================================
# 3. RESENAS POR DISPOSITIVO
# =====================================================

preparar_eje(ax3, "Resenas por dispositivo")

conteo_dispositivo = (
    df["dispositivo_es"]
    .value_counts()
    .sort_values(ascending=True)
)

barras = ax3.barh(
    conteo_dispositivo.index,
    conteo_dispositivo.values,
    color=[
        ROJOS[i % len(ROJOS)]
        for i in range(len(conteo_dispositivo))
    ],
    height=0.52
)

ax3.set_xlabel("Cantidad de resenas", color=GRIS)

for barra in barras:
    ax3.annotate(
        entero(barra.get_width()),
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

# =====================================================
# 4. EVOLUCION MENSUAL DE RESENAS
# =====================================================

preparar_eje(ax4, "Evolucion mensual de resenas")

fechas_validas = df.dropna(subset=["review_date"]).copy()

if not fechas_validas.empty:
    fechas_validas["mes"] = (
        fechas_validas["review_date"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    mensual = fechas_validas.groupby("mes").size()

    ax4.plot(
        mensual.index,
        mensual.values,
        color=ROJOS[5],
        linewidth=2,
        marker="o",
        markersize=3
    )

    ax4.fill_between(
        mensual.index,
        mensual.values,
        color=ROJOS[3],
        alpha=0.16
    )

    ax4.tick_params(axis="x", rotation=25)
    ax4.set_ylabel("Cantidad de resenas", color=GRIS)
    ax4.set_xlabel("Mes", color=GRIS)
    ax4.yaxis.set_major_locator(MaxNLocator(integer=True))
else:
    ax4.text(
        0.5, 0.5,
        "No hay fechas validas para graficar",
        color=BLANCO,
        ha="center",
        va="center",
        transform=ax4.transAxes
    )

# =====================================================
# PIE Y RESULTADOS
# =====================================================

fig.text(
    0.04, 0.025,
    "Fuente: conjunto de datos sintetico descargado de Kaggle. "
    "Los comentarios originales se conservan sin traducir.",
    color=GRIS,
    fontsize=8
)

fig.subplots_adjust(
    top=0.74,
    bottom=0.09,
    left=0.08,
    right=0.96
)

fig.savefig(
    salida / "panel_resenas.png",
    dpi=250,
    facecolor=FONDO,
    bbox_inches="tight"
)

fig.savefig(
    salida / "panel_resenas.pdf",
    facecolor=FONDO,
    bbox_inches="tight"
)

plt.show()

# =====================================================
# RESUMEN PARA EL INFORME ACADEMICO
# =====================================================

print("=" * 55)
print("RESUMEN ESTADISTICO DE RESENAS")
print("=" * 55)

print(f"Total de resenas: {entero(total)}")
print(f"Calificacion promedio: {promedio:.2f}/5")
print(f"Calificacion mediana: {mediana:.0f}/5")
print(f"Sentimiento positivo: {entero(positivas)}")
print(f"Sentimiento neutral: {entero(neutrales)}")
print(f"Sentimiento negativo: {entero(negativas)}")
print(f"Resenas verificadas: {entero(verificadas)}")
print(f"Resenas no verificadas: {entero(no_verificadas)}")
print(f"Textos faltantes: {entero(faltantes_texto)}")
print(f"Filas duplicadas exactas: {entero(duplicados)}")

print("\nArchivos generados:")
print("- resultados/panel_resenas.png")
print("- resultados/panel_resenas.pdf")
