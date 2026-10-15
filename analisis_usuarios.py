from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# ==========================================================
# NETFLIX INTELLIGENCE
# ANALISIS ESTADISTICO DEL PERFIL DE LOS USUARIOS
# ==========================================================

# 1. CARGA Y VALIDACION DE LOS DATOS

ruta = Path("data") / "users.csv"
salida = Path("resultados")
salida.mkdir(exist_ok=True)

if not ruta.exists():
    raise FileNotFoundError(
        "No se encuentra data/users.csv. "
        "Comprueba que el archivo exista dentro de la carpeta data."
    )

usuarios = pd.read_csv(ruta)

# Se excluyen duplicados exactos solo en memoria; el CSV original se conserva.
_duplicados_exactos = int(usuarios.duplicated().sum())
if _duplicados_exactos:
    print(f"Filas duplicadas exactas excluidas del análisis: {_duplicados_exactos:,}")
usuarios = usuarios.drop_duplicates().copy()

columnas_necesarias = [
    "subscription_plan",
    "country",
    "primary_device",
    "is_active",
]

faltantes = [
    columna
    for columna in columnas_necesarias
    if columna not in usuarios.columns
]

if faltantes:
    raise ValueError(
        f"Faltan columnas necesarias en users.csv: {faltantes}"
    )

total_usuarios = len(usuarios)

# ==========================================================
# 2. PALETA VISUAL
# ==========================================================

FONDO = "#160D18"
PANEL = "#281A2B"
BLANCO = "#FFFFFF"
GRIS = "#C9C1CC"
BORDE = "#514153"

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

fig, ejes = plt.subplots(
    2,
    2,
    figsize=(15, 10),
)

fig.patch.set_facecolor(FONDO)

fig.suptitle(
    "NETFLIX INTELLIGENCE\n"
    "Perfil y características de los usuarios",
    color=BLANCO,
    fontsize=21,
    fontweight="bold",
    y=0.98,
)

# ==========================================================
# 3. FUNCIONES AUXILIARES
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

    ax.tick_params(
        colors=GRIS,
        labelsize=9,
    )

    for borde in ax.spines.values():
        borde.set_color(BORDE)
        borde.set_linewidth(0.7)

    ax.grid(
        axis="y",
        color=BORDE,
        linestyle="--",
        linewidth=0.6,
        alpha=0.5,
    )

    ax.set_axisbelow(True)


def formato_entero(numero):
    return f"{int(numero):,}".replace(",", ".")


def contar_categoria(serie):
    serie = serie.astype("string").str.strip()
    serie = serie.replace("", pd.NA).dropna()

    return serie.value_counts()


def traducir_categorias(serie, equivalencias):
    serie = serie.copy()

    serie.index = [
        equivalencias.get(
            str(valor).strip().casefold(),
            str(valor).strip(),
        )
        for valor in serie.index
    ]

    # Unificar valores que se traduzcan a la misma categoría.
    return (
        serie.groupby(level=0)
        .sum()
        .sort_values(ascending=False)
    )


def dibujar_etiquetas_verticales(ax, barras):
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
            va="bottom",
            color=BLANCO,
            fontsize=8,
        )


def dibujar_etiquetas_horizontales(ax, barras):
    for barra in barras:
        ancho = barra.get_width()

        ax.annotate(
            formato_entero(ancho),
            (
                ancho,
                barra.get_y() + barra.get_height() / 2,
            ),
            xytext=(5, 0),
            textcoords="offset points",
            va="center",
            color=BLANCO,
            fontsize=8,
        )


# ==========================================================
# 4. GRAFICA: TIPO DE SUSCRIPCION
# ==========================================================

ax = ejes[0, 0]

preparar_eje(
    ax,
    "Usuarios por tipo de suscripción",
)

suscripciones = contar_categoria(
    usuarios["subscription_plan"]
)

traduccion_suscripciones = {
    "standard": "Estándar",
    "premium": "Premium",
    "basic": "Básica",
    "premium+": "Premium Plus",
    "free": "Gratuita",
    "estandar": "Estándar",
    "básica": "Básica",
    "basica": "Básica",
}

suscripciones = traducir_categorias(
    suscripciones,
    traduccion_suscripciones,
)

barras = ax.bar(
    suscripciones.index.astype(str),
    suscripciones.values,
    color=[
        ROJOS[i % len(ROJOS)]
        for i in range(len(suscripciones))
    ],
    width=0.55,
)

ax.set_ylabel(
    "Número de usuarios",
    color=GRIS,
)

ax.yaxis.set_major_locator(
    MaxNLocator(integer=True)
)

ax.tick_params(
    axis="x",
    rotation=12,
)

dibujar_etiquetas_verticales(ax, barras)

# ==========================================================
# 5. GRAFICA: DISTRIBUCION POR PAIS
# ==========================================================

ax = ejes[0, 1]

preparar_eje(
    ax,
    "Distribución por país",
)

paises = contar_categoria(
    usuarios["country"]
)

traduccion_paises = {
    "usa": "Estados Unidos",
    "united states": "Estados Unidos",
    "us": "Estados Unidos",
    "u.s.a.": "Estados Unidos",
    "canada": "Canadá",
    "can": "Canadá",
    "ca": "Canadá",
}

paises = traducir_categorias(
    paises,
    traduccion_paises,
)

barras = ax.barh(
    paises.index.astype(str),
    paises.values,
    color=[
        ROJOS[i % len(ROJOS)]
        for i in range(len(paises))
    ],
    height=0.5,
)

ax.set_xlabel(
    "Número de usuarios",
    color=GRIS,
)

ax.invert_yaxis()

dibujar_etiquetas_horizontales(ax, barras)

# ==========================================================
# 6. GRAFICA: DISPOSITIVO PRINCIPAL
# ==========================================================

ax = ejes[1, 0]

preparar_eje(
    ax,
    "Dispositivo principal",
)

dispositivos = contar_categoria(
    usuarios["primary_device"]
)

traduccion_dispositivos = {
    "desktop": "Computador de mesa",
    "desktop computer": "Computador de mesa",
    "computer": "Computador de mesa",
    "laptop": "Portátil",
    "notebook": "Portátil",
    "tablet": "Tableta",
    "smart tv": "Televisor",
    "smart television": "Televisor",
    "television": "Televisor",
    "tv": "Televisor",
    "mobile": "Celular",
    "smartphone": "Celular",
    "phone": "Celular",
    "gaming console": "Consola de videojuegos",
    "console": "Consola de videojuegos",
}

dispositivos = traducir_categorias(
    dispositivos,
    traduccion_dispositivos,
)

barras = ax.barh(
    dispositivos.index.astype(str),
    dispositivos.values,
    color=[
        ROJOS[i % len(ROJOS)]
        for i in range(len(dispositivos))
    ],
    height=0.5,
)

ax.set_xlabel(
    "Número de usuarios",
    color=GRIS,
)

ax.invert_yaxis()

dibujar_etiquetas_horizontales(ax, barras)

# ==========================================================
# 7. GRAFICA: ESTADO DE ACTIVIDAD
# ==========================================================

ax = ejes[1, 1]

preparar_eje(
    ax,
    "Estado de actividad registrado",
)

actividad_original = usuarios["is_active"]

# Convertir los valores a categorías consistentes.
actividad_texto = (
    actividad_original.astype("string")
    .str.strip()
    .str.casefold()
)

traduccion_actividad = {
    "true": "Activo",
    "false": "Inactivo",
    "1": "Activo",
    "0": "Inactivo",
    "yes": "Activo",
    "no": "Inactivo",
    "sí": "Activo",
    "si": "Activo",
    "activo": "Activo",
    "inactivo": "Inactivo",
}

actividad_texto = actividad_texto.map(
    lambda valor: traduccion_actividad.get(
        valor,
        valor if pd.notna(valor) else pd.NA,
    )
)

actividad = actividad_texto.value_counts(
    dropna=True
)

barras = ax.bar(
    actividad.index.astype(str),
    actividad.values,
    color=[
        ROJOS[i % len(ROJOS)]
        for i in range(len(actividad))
    ],
    width=0.45,
)

ax.set_ylabel(
    "Número de usuarios",
    color=GRIS,
)

ax.yaxis.set_major_locator(
    MaxNLocator(integer=True)
)

dibujar_etiquetas_verticales(ax, barras)

# ==========================================================
# 8. INDICADORES GENERALES
# ==========================================================

usuarios_validos = usuarios["user_id"].nunique() if "user_id" in usuarios.columns else total_usuarios

fig.text(
    0.05,
    0.91,
    f"Registros: {formato_entero(total_usuarios)}"
    f"    |    Usuarios identificados: {formato_entero(usuarios_validos)}",
    color=GRIS,
    fontsize=10,
)

fig.text(
    0.04,
    0.035,
    "Fuente: conjunto de datos sintético descargado de Kaggle. "
    "Las cifras describen los archivos analizados y no son datos oficiales de Netflix.",
    color=GRIS,
    fontsize=8,
)

fig.text(
    0.96,
    0.035,
    "NETFLIX INTELLIGENCE | ANÁLISIS CUANTITATIVO",
    color=ROJOS[5],
    fontsize=8,
    ha="right",
)

plt.tight_layout(
    rect=[0.03, 0.07, 0.98, 0.88],
)

# ==========================================================
# 9. GUARDAR GRAFICAS
# ==========================================================

archivo_png = salida / "perfil_usuarios.png"
archivo_pdf = salida / "perfil_usuarios.pdf"

fig.savefig(
    archivo_png,
    dpi=250,
    facecolor=FONDO,
    bbox_inches="tight",
)

fig.savefig(
    archivo_pdf,
    facecolor=FONDO,
    bbox_inches="tight",
)

# ==========================================================
# 10. MOSTRAR RESULTADOS
# ==========================================================

print("=" * 55)
print("NETFLIX INTELLIGENCE")
print("ANÁLISIS DEL PERFIL DE LOS USUARIOS")
print("=" * 55)

print(
    f"\nTotal de registros: {formato_entero(total_usuarios)}"
)

print(
    f"Usuarios identificados: {formato_entero(usuarios_validos)}"
)

print("\nUsuarios por tipo de suscripción:")
print(suscripciones.to_string())

print("\nUsuarios por país:")
print(paises.to_string())

print("\nUsuarios por dispositivo principal:")
print(dispositivos.to_string())

print("\nEstado de actividad:")
print(actividad.to_string())

print("\nPanel guardado correctamente.")
print(f"Imagen: {archivo_png}")
print(f"Documento PDF: {archivo_pdf}")

plt.show()