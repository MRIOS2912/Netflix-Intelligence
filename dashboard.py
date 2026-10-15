
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


# ============================================================
# NETFLIX INTELLIGENCE - PANEL GENERAL
# ============================================================

BASE = Path(__file__).resolve().parent
DATOS = BASE / "data"
RESULTADOS = BASE / "resultados"
RESULTADOS.mkdir(exist_ok=True)

ARCHIVOS = {
    "usuarios": "users.csv",
    "peliculas": "movies.csv",
    "visualizaciones": "watch_history.csv",
    "busquedas": "search_logs.csv",
    "resenas": "reviews.csv",
    "recomendaciones": "recommendation_logs.csv",
}

datos = {}

for nombre, archivo in ARCHIVOS.items():
    ruta = DATOS / archivo

    if ruta.exists():
        datos[nombre] = pd.read_csv(ruta)
        duplicados = int(datos[nombre].duplicated().sum())
        if duplicados:
            print(f"{archivo}: {duplicados:,} filas duplicadas exactas excluidas del análisis.")
            datos[nombre] = datos[nombre].drop_duplicates().copy()
    else:
        print(f"AVISO: No se encontró el archivo {archivo}")

if not datos:
    raise FileNotFoundError(
        "No se encontraron archivos CSV dentro de la carpeta data."
    )


# ============================================================
# DISEÑO VISUAL
# ============================================================

FONDO = "#160D18"
PANEL = "#281A2B"
BLANCO = "#FFFFFF"
GRIS = "#C9C1CC"
BORDE = "#514153"

ROJOS = [
    "#590D16",
    "#800D19",
    "#A30D20",
    "#C1122F",
    "#E50914",
    "#F04455",
    "#FF7180",
]

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "text.color": BLANCO,
    "axes.labelcolor": GRIS,
    "xtick.color": GRIS,
    "ytick.color": GRIS,
})


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def entero(valor):
    """Formatea cantidades enteras con punto como separador."""
    return f"{int(valor):,}".replace(",", ".")


def estilo(ax, titulo, eje_y=True):
    """Aplica el estilo visual común a las gráficas."""
    ax.set_facecolor(PANEL)

    ax.set_title(
        titulo,
        loc="left",
        color=BLANCO,
        fontsize=12,
        fontweight="bold",
        pad=12,
    )

    ax.tick_params(colors=GRIS, labelsize=8)

    for borde in ax.spines.values():
        borde.set_color(BORDE)

    ax.grid(
        axis="y" if eje_y else "x",
        color=BORDE,
        linestyle="--",
        linewidth=0.6,
        alpha=0.6,
    )

    ax.set_axisbelow(True)


def tarjeta(fig, x, titulo, valor, detalle, color):
    """Crea una tarjeta con un indicador del proyecto."""
    ax = fig.add_axes([x, 0.79, 0.17, 0.105])
    ax.set_facecolor(PANEL)
    ax.set_xticks([])
    ax.set_yticks([])

    for borde in ax.spines.values():
        borde.set_visible(False)

    ax.axhline(1, color=color, linewidth=4, clip_on=False)

    ax.text(
        0.06, 0.76, titulo,
        transform=ax.transAxes,
        color=GRIS,
        fontsize=8,
    )

    ax.text(
        0.06, 0.39, valor,
        transform=ax.transAxes,
        color=color,
        fontsize=19,
        fontweight="bold",
    )

    ax.text(
        0.06, 0.10, detalle,
        transform=ax.transAxes,
        color=GRIS,
        fontsize=7,
    )


def etiquetas_barras(ax, barras, horizontal=False):
    """Añade los valores numéricos al final de las barras."""
    for barra in barras:
        valor = barra.get_width() if horizontal else barra.get_height()

        if horizontal:
            ax.annotate(
                entero(valor),
                (valor, barra.get_y() + barra.get_height() / 2),
                xytext=(4, 0),
                textcoords="offset points",
                va="center",
                color=BLANCO,
                fontsize=8,
            )
        else:
            ax.annotate(
                entero(valor),
                (barra.get_x() + barra.get_width() / 2, valor),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                color=BLANCO,
                fontsize=8,
            )


def total(nombre):
    """Devuelve la cantidad de filas de un archivo cargado."""
    return len(datos[nombre]) if nombre in datos else 0


def traducir_categoria(valor, traducciones):
    """Traduce una categoría sin modificar el archivo CSV original."""
    texto = str(valor).strip()
    return traducciones.get(texto.casefold(), texto)


def contar_categorias(serie, traducciones):
    """Traduce y agrupa categorías equivalentes antes de contarlas."""
    serie = serie.astype("string").str.strip()
    serie = serie.replace("", pd.NA).fillna("Sin dato")

    serie = serie.map(
        lambda valor: traducir_categoria(valor, traducciones)
    )

    return serie.value_counts().sort_values()


# ============================================================
# TRADUCCIONES
# ============================================================

TRADUCCION_CONTENIDO = {
    "movie": "Película",
    "tv series": "Series de televisión",
    "tv show": "Series de televisión",
    "series": "Series de televisión",
    "documentary": "Documental",
    "stand-up comedy": "Comedia en vivo",
    "limited series": "Serie limitada",
}

TRADUCCION_DISPOSITIVOS = {
    "mobile": "Celular",
    "smart tv": "Televisor",
    "tablet": "Tableta",
    "laptop": "Portátil",
    "desktop": "Computador",
    "gaming console": "Consola",
    "unknown": "Sin identificar",
}

TRADUCCION_CALIFICACIONES = {
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
}


# ============================================================
# ENCABEZADO DEL PANEL
# ============================================================

fig = plt.figure(figsize=(17, 10), facecolor=FONDO)

fig.text(
    0.045, 0.955,
    "NETFLIX INTELLIGENCE",
    fontsize=24,
    fontweight="bold",
    color="#E50914",
)

fig.text(
    0.045, 0.915,
    "Panel general de análisis estadístico",
    fontsize=15,
    color=BLANCO,
)

fig.text(
    0.955, 0.955,
    "PROYECTO ACADÉMICO",
    fontsize=9,
    color=GRIS,
    ha="right",
)

fig.text(
    0.955, 0.925,
    "Datos sintéticos",
    fontsize=9,
    color="#FF7180",
    ha="right",
)


# ============================================================
# TARJETAS DE RESUMEN
# ============================================================

tarjetas = [
    ("USUARIOS", total("usuarios"), "Registros de usuarios"),
    ("CONTENIDOS", total("peliculas"), "Registros del catálogo"),
    ("REPRODUCCIONES", total("visualizaciones"), "Historial registrado"),
    ("RESEÑAS", total("resenas"), "Opiniones registradas"),
    ("BÚSQUEDAS", total("busquedas"), "Consultas registradas"),
]

posiciones = [0.045, 0.235, 0.425, 0.615, 0.805]

for i, (x, (titulo, cantidad, detalle)) in enumerate(
    zip(posiciones, tarjetas)
):
    tarjeta(
        fig,
        x,
        titulo,
        entero(cantidad),
        detalle,
        ROJOS[i],
    )


# ============================================================
# GRÁFICA 1: DISTRIBUCIÓN DE EDADES
# ============================================================

ax1 = fig.add_axes([0.07, 0.48, 0.39, 0.23])

if "usuarios" in datos and "age" in datos["usuarios"].columns:
    edades = pd.to_numeric(
        datos["usuarios"]["age"],
        errors="coerce",
    )

    edades = edades[edades.between(0, 100)].dropna()

    estilo(ax1, "Distribución de edades")

    if not edades.empty:
        ax1.hist(
            edades,
            bins=15,
            color="#C1122F",
            edgecolor=FONDO,
            linewidth=0.8,
            rwidth=0.88,
        )

        ax1.set_xlabel("Edad (años)")
        ax1.set_ylabel("Número de usuarios")
        ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
    else:
        ax1.text(
            0.5, 0.5,
            "No hay edades válidas para mostrar",
            ha="center",
            va="center",
            transform=ax1.transAxes,
            color=GRIS,
        )
else:
    estilo(ax1, "Distribución de edades")
    ax1.text(
        0.5, 0.5,
        "Datos de edad no disponibles",
        ha="center",
        va="center",
        transform=ax1.transAxes,
    )


# ============================================================
# GRÁFICA 2: TIPOS DE CONTENIDO
# ============================================================

ax2 = fig.add_axes([0.56, 0.48, 0.37, 0.23])

if "peliculas" in datos and "content_type" in datos["peliculas"].columns:
    tipos = contar_categorias(
        datos["peliculas"]["content_type"],
        TRADUCCION_CONTENIDO,
    )

    estilo(ax2, "Catálogo por tipo de contenido", eje_y=False)

    barras = ax2.barh(
        tipos.index,
        tipos.values,
        color=[
            ROJOS[i % len(ROJOS)]
            for i in range(len(tipos))
        ],
        height=0.52,
    )

    etiquetas_barras(ax2, barras, horizontal=True)
    ax2.set_xlabel("Cantidad de contenidos")
else:
    estilo(ax2, "Catálogo por tipo de contenido")
    ax2.text(
        0.5, 0.5,
        "Tipo de contenido no disponible",
        ha="center",
        va="center",
        transform=ax2.transAxes,
    )


# ============================================================
# GRÁFICA 3: REPRODUCCIONES POR DISPOSITIVO
# ============================================================

ax3 = fig.add_axes([0.10, 0.16, 0.36, 0.23])

if (
    "visualizaciones" in datos
    and "device_type" in datos["visualizaciones"].columns
):
    dispositivos = contar_categorias(
        datos["visualizaciones"]["device_type"],
        TRADUCCION_DISPOSITIVOS,
    )

    estilo(ax3, "Reproducciones por dispositivo", eje_y=False)

    barras = ax3.barh(
        dispositivos.index,
        dispositivos.values,
        color=[
            ROJOS[i % len(ROJOS)]
            for i in range(len(dispositivos))
        ],
        height=0.48,
    )

    ax3.tick_params(axis="y", labelsize=8, pad=7)
    etiquetas_barras(ax3, barras, horizontal=True)
    ax3.set_xlabel("Cantidad de registros")
    ax3.set_ylabel("")
    ax3.margins(x=0.12)
else:
    estilo(ax3, "Reproducciones por dispositivo")
    ax3.text(
        0.5, 0.5,
        "Dispositivos no disponibles",
        ha="center",
        va="center",
        transform=ax3.transAxes,
    )


# ============================================================
# GRÁFICA 4: DISTRIBUCIÓN DE CALIFICACIONES
# ============================================================

ax4 = fig.add_axes([0.56, 0.16, 0.37, 0.23])

if "resenas" in datos and "rating" in datos["resenas"].columns:
    calificaciones = pd.to_numeric(
        datos["resenas"]["rating"],
        errors="coerce",
    ).dropna()

    calificaciones = calificaciones[
        calificaciones.between(1, 5)
    ]

    if not calificaciones.empty:
        conteo = calificaciones.value_counts().sort_index()

        estilo(ax4, "Distribución de calificaciones")

        barras = ax4.bar(
            conteo.index.astype(int).astype(str),
            conteo.values,
            color=[
                ROJOS[i % len(ROJOS)]
                for i in range(len(conteo))
            ],
            width=0.48,
        )

        etiquetas_barras(ax4, barras)
        ax4.set_xlabel("Calificación (de 1 a 5)")
        ax4.set_ylabel("Cantidad de reseñas")
        ax4.yaxis.set_major_locator(MaxNLocator(integer=True))
    else:
        estilo(ax4, "Distribución de calificaciones")
        ax4.text(
            0.5, 0.5,
            "No hay calificaciones válidas",
            ha="center",
            va="center",
            transform=ax4.transAxes,
        )
else:
    estilo(ax4, "Distribución de calificaciones")
    ax4.text(
        0.5, 0.5,
        "Calificaciones no disponibles",
        ha="center",
        va="center",
        transform=ax4.transAxes,
    )


# ============================================================
# FUENTE Y PIE DEL PANEL
# ============================================================

fig.text(
    0.045, 0.075,
    "Fuente: conjunto de datos sintético descargado de Kaggle. "
    "Las cifras describen los archivos disponibles y no son datos oficiales de Netflix.",
    color=GRIS,
    fontsize=8,
)

fig.text(
    0.955, 0.045,
    "NETFLIX INTELLIGENCE | ANÁLISIS CUANTITATIVO",
    color="#FF7180",
    fontsize=8,
    ha="right",
)


# ============================================================
# GUARDAR RESULTADOS
# ============================================================

ruta_png = RESULTADOS / "dashboard_general.png"
ruta_pdf = RESULTADOS / "dashboard_general.pdf"

fig.savefig(
    ruta_png,
    dpi=220,
    facecolor=FONDO,
    bbox_inches="tight",
)

fig.savefig(
    ruta_pdf,
    facecolor=FONDO,
    bbox_inches="tight",
)

plt.show()


# ============================================================
# RESUMEN EN LA TERMINAL
# ============================================================

print("\n" + "=" * 55)
print("NETFLIX INTELLIGENCE - PANEL GENERAL")
print("=" * 55)

for nombre, archivo in ARCHIVOS.items():
    if nombre in datos:
        print(
            f"{archivo}: {entero(len(datos[nombre]))} registros"
        )

print("\nPanel guardado correctamente:")
print(ruta_png)
print(ruta_pdf)
print("=" * 55)
