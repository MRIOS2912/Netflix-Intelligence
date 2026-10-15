from pathlib import Path
import pandas as pd

# ==========================================
# CARGA Y VALIDACION DE DATOS
# ==========================================

ruta = Path("data") / "movies.csv"
salida = Path("resultados")
salida.mkdir(exist_ok=True)

if not ruta.exists():
    raise FileNotFoundError(
        "No se encuentra el archivo data/movies.csv. "
        "Comprueba la carpeta del proyecto."
    )

peliculas = pd.read_csv(ruta)

# Se excluyen duplicados exactos solo en memoria; el CSV original se conserva.
_duplicados_exactos = int(peliculas.duplicated().sum())
if _duplicados_exactos:
    print(f"Filas duplicadas exactas excluidas del análisis: {_duplicados_exactos:,}")
peliculas = peliculas.drop_duplicates().copy()

# ==========================================
# MOSTRAR INFORMACION DEL CATALOGO
# ==========================================

print("=" * 55)
print("NETFLIX INTELLIGENCE")
print("INSPECCIÓN DEL CATÁLOGO DE PELÍCULAS")
print("=" * 55)

print(
    f"\nTotal de registros del catálogo: "
    f"{len(peliculas):,}".replace(",", ".")
)

print(f"Total de columnas: {len(peliculas.columns)}")

print("\nCOLUMNAS DISPONIBLES:")
for columna in peliculas.columns:
    print("-", columna)

print("\nPRIMEROS CINCO REGISTROS:")
print(peliculas.head().to_string(index=False))

print("\nTIPOS DE DATOS:")
print(peliculas.dtypes.to_string())

print("\nVALORES FALTANTES POR COLUMNA:")
print(peliculas.isna().sum().to_string())

# ==========================================
# CREAR INFORME DE CALIDAD DE DATOS
# ==========================================

informe = pd.DataFrame({
    "columna": peliculas.columns,
    "tipo_de_dato": [
        str(tipo) for tipo in peliculas.dtypes
    ],
    "valores_faltantes": [
        int(peliculas[columna].isna().sum())
        for columna in peliculas.columns
    ]
})

archivo_informe = salida / "inspeccion_peliculas.csv"

informe.to_csv(
    archivo_informe,
    index=False,
    encoding="utf-8-sig"
)

# ==========================================
# RESUMEN FINAL
# ==========================================

print("\n" + "=" * 55)
print("RESUMEN DE LA INSPECCIÓN")
print("=" * 55)

print(
    f"Registros analizados: "
    f"{len(peliculas):,}".replace(",", ".")
)

print(f"Columnas revisadas: {len(peliculas.columns)}")

print(
    "Valores faltantes en todo el archivo: "
    f"{peliculas.isna().sum().sum():,}".replace(",", ".")
)

print(
    "\nInforme guardado en: "
    "resultados/inspeccion_peliculas.csv"
)

print("Inspección terminada correctamente.")