
from pathlib import Path
import pandas as pd

# ============================================================
# NETFLIX INTELLIGENCE
# ANÁLISIS Y AUDITORÍA DE RESEÑAS
# ============================================================

BASE = Path(__file__).resolve().parent
RUTA_DATOS = BASE / "data" / "reviews.csv"
CARPETA_RESULTADOS = BASE / "resultados"
CARPETA_RESULTADOS.mkdir(parents=True, exist_ok=True)

if not RUTA_DATOS.exists():
    raise FileNotFoundError(
        "No se encuentra data/reviews.csv. "
        "Comprueba que el archivo esté dentro de la carpeta data."
    )

resenas = pd.read_csv(RUTA_DATOS, encoding="utf-8")

# Se excluyen duplicados exactos solo en memoria; el CSV original se conserva.
_duplicados_exactos = int(resenas.duplicated().sum())
if _duplicados_exactos:
    print(f"Filas duplicadas exactas excluidas del análisis: {_duplicados_exactos:,}")
resenas = resenas.drop_duplicates().copy()

if resenas.empty:
    raise ValueError("El archivo de reseñas está vacío.")

# ============================================================
# TRADUCCIONES PARA INFORMES
# Los nombres originales de las columnas no se modifican.
# ============================================================

NOMBRES_COLUMNAS = {
    "review_id": "Identificador de la reseña",
    "user_id": "Identificador del usuario",
    "movie_id": "Identificador del contenido",
    "rating": "Calificación",
    "review_date": "Fecha de la reseña",
    "device_type": "Tipo de dispositivo",
    "is_verified_watch": "Reproducción verificada",
    "helpful_votes": "Votos de utilidad",
    "total_votes": "Total de votos",
    "review_text": "Texto de la reseña",
    "sentiment": "Sentimiento",
    "sentiment_score": "Puntuación del sentimiento",
}

TRADUCCION_SENTIMIENTOS = {
    "positive": "Positivo",
    "neutral": "Neutral",
    "negative": "Negativo",
}

TRADUCCION_DISPOSITIVOS = {
    "mobile": "Celular",
    "smart tv": "Televisor inteligente",
    "tablet": "Tableta",
    "laptop": "Portátil",
    "desktop": "Computador de mesa",
    "gaming console": "Consola de videojuegos",
}

TRADUCCION_RESEÑAS = {
    "Fantastic cinematography and plot twists.":
        "Fotografía fantástica y giros inesperados en la trama.",
    "This series is a masterpiece!":
        "¡Esta serie es una obra maestra!",
    "One of the best series I've ever watched. Highly recommend!":
        "Una de las mejores series que he visto. ¡La recomiendo mucho!",
    "Mixed feelings about this one.":
        "Tengo sentimientos encontrados sobre esta producción.",
    "Outstanding direction and screenplay.":
        "Dirección y guion extraordinarios.",
    "Absolutely loved this movie. Great acting and storyline.":
        "Me encantó esta película. Tiene excelentes actuaciones y una gran historia.",
    "Amazing show! Couldn't stop watching.":
        "¡Una producción increíble! No podía dejar de verla.",
}


def nombre_es(columna):
    return NOMBRES_COLUMNAS.get(
        columna,
        columna.replace("_", " ").capitalize()
    )


def formato_entero(numero):
    return f"{int(numero):,}".replace(",", ".")


def formato_decimal(numero, decimales=2):
    return f"{numero:.{decimales}f}".replace(".", ",")


def traducir_categoria(valor, traducciones):
    if pd.isna(valor):
        return "Sin dato"

    texto = str(valor).strip()
    return traducciones.get(texto.casefold(), texto)


def traducir_valor(columna, valor):
    if pd.isna(valor):
        return "Sin dato"

    if columna == "sentiment":
        return traducir_categoria(valor, TRADUCCION_SENTIMIENTOS)

    if columna == "device_type":
        return traducir_categoria(valor, TRADUCCION_DISPOSITIVOS)

    if columna == "is_verified_watch":
        texto = str(valor).strip().casefold()

        if texto in ("true", "1", "sí", "si"):
            return "Sí"
        if texto in ("false", "0", "no"):
            return "No"

    if columna == "review_text":
        texto = str(valor).strip()
        return TRADUCCION_RESEÑAS.get(texto, texto)

    return valor


# ============================================================
# 1. INFORMACIÓN GENERAL
# ============================================================

print("=" * 65)
print("NETFLIX INTELLIGENCE")
print("ANÁLISIS DE RESEÑAS Y CALIFICACIONES")
print("=" * 65)

print("\n1. TAMAÑO DEL CONJUNTO DE DATOS")
print(f"Total de registros: {formato_entero(len(resenas))}")
print(f"Total de columnas: {len(resenas.columns)}")

# ============================================================
# 2. COLUMNAS DISPONIBLES
# ============================================================

print("\n2. COLUMNAS DISPONIBLES")

for columna in resenas.columns:
    print(f"- {nombre_es(columna)}")

# ============================================================
# 3. PRIMEROS CINCO REGISTROS EN ESPAÑOL
# ============================================================

print("\n3. PRIMEROS CINCO REGISTROS")

primeros = resenas.head().copy()

primeros = primeros.rename(
    columns={
        columna: nombre_es(columna)
        for columna in primeros.columns
    }
)

for columna_original in resenas.columns:
    columna_es = nombre_es(columna_original)

    if columna_es in primeros.columns:
        primeros[columna_es] = primeros[columna_es].map(
            lambda valor: traducir_valor(columna_original, valor)
        )

print(primeros.to_string(index=False))

# ============================================================
# 4. TIPOS DE DATOS
# ============================================================

print("\n4. TIPOS DE DATOS")

tipos = pd.DataFrame({
    "Columna": [nombre_es(c) for c in resenas.columns],
    "Tipo de dato": [str(t) for t in resenas.dtypes],
})

print(tipos.to_string(index=False))

# ============================================================
# 5. VALORES FALTANTES
# ============================================================

print("\n5. VALORES FALTANTES POR COLUMNA")

faltantes = resenas.isna().sum()

tabla_faltantes = pd.DataFrame({
    "Columna": [nombre_es(c) for c in faltantes.index],
    "Valores faltantes": faltantes.values,
    "Porcentaje (%)": (
        faltantes.values / len(resenas) * 100
    ).round(2),
})

tabla_faltantes = tabla_faltantes.sort_values(
    "Valores faltantes",
    ascending=False
)

print(tabla_faltantes.to_string(index=False))

total_faltantes = int(faltantes.sum())

print(
    "\nTotal de celdas vacías: "
    f"{formato_entero(total_faltantes)}"
)

# ============================================================
# 6. DUPLICADOS Y REPETICIÓN DE IDENTIFICADORES
# ============================================================

print("\n6. REVISIÓN DE CALIDAD DE LOS DATOS")

duplicados_exactos = int(resenas.duplicated().sum())

print(
    "Filas duplicadas exactas: "
    f"{formato_entero(duplicados_exactos)}"
)

if len(resenas) > 0:
    porcentaje_duplicados = (
        duplicados_exactos / len(resenas) * 100
    )
    print(
        "Porcentaje de filas duplicadas exactas: "
        f"{formato_decimal(porcentaje_duplicados)} %"
    )

if "review_id" in resenas.columns:
    ids_repetidos = int(
        resenas["review_id"].duplicated(keep=False).sum()
    )
    ids_duplicados_adicionales = int(
        resenas["review_id"].duplicated().sum()
    )

    print(
        "Registros que pertenecen a identificadores de reseña repetidos: "
        f"{formato_entero(ids_repetidos)}"
    )

    print(
        "Repeticiones adicionales de identificadores de reseña: "
        f"{formato_entero(ids_duplicados_adicionales)}"
    )

    print(
        "Nota: un identificador repetido requiere revisión; "
        "no demuestra por sí solo que dos filas sean idénticas."
    )

# ============================================================
# 7. ESTADÍSTICAS NUMÉRICAS
# ============================================================

print("\n7. ESTADÍSTICAS DE LAS VARIABLES NUMÉRICAS")

numericas = resenas.select_dtypes(include="number")
estadisticas = numericas.describe().round(2)

if estadisticas.empty:
    print("No se encontraron variables numéricas.")
else:
    estadisticas.index = [
        {
            "count": "Cantidad de datos",
            "mean": "Media",
            "std": "Desviación estándar",
            "min": "Mínimo",
            "25%": "Primer cuartil",
            "50%": "Mediana",
            "75%": "Tercer cuartil",
            "max": "Máximo",
        }.get(str(indice), str(indice))
        for indice in estadisticas.index
    ]

    estadisticas.columns = [
        nombre_es(columna)
        for columna in estadisticas.columns
    ]

    print(estadisticas.to_string())

    estadisticas.to_csv(
        CARPETA_RESULTADOS / "estadisticas_numericas_resenas.csv",
        encoding="utf-8-sig"
    )

# ============================================================
# 8. RESUMEN DE CATEGORÍAS
# ============================================================

print("\n8. RESUMEN DE LAS VARIABLES CATEGÓRICAS")

resumen_categorias = []

columnas_categoricas = resenas.select_dtypes(
    include=["object", "category", "bool"]
).columns

for columna in columnas_categoricas:
    serie = resenas[columna].map(
        lambda valor: traducir_valor(columna, valor)
    )

    frecuencias = serie.value_counts(dropna=False).head(5)

    print(f"\nVariable: {nombre_es(columna)}")
    print(
        "Cantidad de valores diferentes: "
        f"{resenas[columna].nunique(dropna=True)}"
    )
    print("Cinco valores más frecuentes:")

    if frecuencias.empty:
        print("No hay valores disponibles.")
    else:
        for valor, cantidad in frecuencias.items():
            print(f"- {valor}: {formato_entero(cantidad)}")

    for valor, cantidad in frecuencias.items():
        resumen_categorias.append({
            "Variable": nombre_es(columna),
            "Categoría": str(valor),
            "Frecuencia": int(cantidad),
        })

# ============================================================
# 9. ANÁLISIS DE CALIFICACIONES
# ============================================================

print("\n9. ANÁLISIS DE CALIFICACIONES")

if "rating" in resenas.columns:
    calificaciones = pd.to_numeric(
        resenas["rating"],
        errors="coerce"
    ).dropna()

    if not calificaciones.empty:
        print(
            "Calificaciones válidas: "
            f"{formato_entero(len(calificaciones))}"
        )
        print(
            "Calificación media: "
            f"{formato_decimal(calificaciones.mean())} sobre 5"
        )
        print(
            "Calificación mediana: "
            f"{formato_decimal(calificaciones.median())}"
        )
        print(
            "Calificación mínima: "
            f"{formato_decimal(calificaciones.min())}"
        )
        print(
            "Calificación máxima: "
            f"{formato_decimal(calificaciones.max())}"
        )

        fuera_rango = int(
            (
                (calificaciones < 1)
                | (calificaciones > 5)
            ).sum()
        )

        print(
            "Calificaciones fuera del rango de 1 a 5: "
            f"{formato_entero(fuera_rango)}"
        )
    else:
        print("No hay calificaciones numéricas válidas.")
else:
    print("No existe la columna de calificación.")

# ============================================================
# 10. ANÁLISIS DE SENTIMIENTOS
# ============================================================

print("\n10. DISTRIBUCIÓN DE SENTIMIENTOS")

if "sentiment" in resenas.columns:
    sentimientos = resenas["sentiment"].map(
        lambda valor: traducir_valor("sentiment", valor)
    ).value_counts()

    for sentimiento, cantidad in sentimientos.items():
        porcentaje = cantidad / len(resenas) * 100

        print(
            f"{sentimiento}: {formato_entero(cantidad)} "
            f"({formato_decimal(porcentaje)} %)"
        )

# ============================================================
# 11. EXPORTACIÓN DE INFORMES
# ============================================================

tabla_faltantes.to_csv(
    CARPETA_RESULTADOS / "auditoria_resenas.csv",
    index=False,
    encoding="utf-8-sig"
)

tipos.to_csv(
    CARPETA_RESULTADOS / "tipos_datos_resenas.csv",
    index=False,
    encoding="utf-8-sig"
)

if resumen_categorias:
    pd.DataFrame(resumen_categorias).to_csv(
        CARPETA_RESULTADOS / "resumen_categorias_resenas.csv",
        index=False,
        encoding="utf-8-sig"
    )

resumen_general = pd.DataFrame({
    "Indicador": [
        "Total de registros",
        "Total de columnas",
        "Celdas vacías",
        "Filas duplicadas exactas",
    ],
    "Resultado": [
        len(resenas),
        len(resenas.columns),
        total_faltantes,
        duplicados_exactos,
    ],
})

resumen_general.to_csv(
    CARPETA_RESULTADOS / "resumen_general_resenas.csv",
    index=False,
    encoding="utf-8-sig"
)

# ============================================================
# 12. FINALIZACIÓN
# ============================================================

print("\n" + "=" * 65)
print("ANÁLISIS DE RESEÑAS TERMINADO")
print("Los archivos originales no fueron modificados.")
print("=" * 65)
print("Informes guardados en la carpeta resultados:")
print("- auditoria_resenas.csv")
print("- tipos_datos_resenas.csv")
print("- estadisticas_numericas_resenas.csv")
print("- resumen_categorias_resenas.csv")
print("- resumen_general_resenas.csv")
print("=" * 65)
