
from pathlib import Path
import pandas as pd

# ==========================================
# NETFLIX INTELLIGENCE
# INSPECCION DE BUSQUEDAS
# ==========================================

ruta = Path("data") / "search_logs.csv"
salida = Path("resultados")
salida.mkdir(exist_ok=True)

if not ruta.exists():
    raise FileNotFoundError(
        "No se encuentra data/search_logs.csv"
    )

busquedas = pd.read_csv(ruta)

# Se excluyen duplicados exactos solo en memoria; el CSV original se conserva.
_duplicados_exactos = int(busquedas.duplicated().sum())
if _duplicados_exactos:
    print(f"Filas duplicadas exactas excluidas del análisis: {_duplicados_exactos:,}")
busquedas = busquedas.drop_duplicates().copy()

print("=" * 60)
print("NETFLIX INTELLIGENCE")
print("ANALISIS INICIAL DE BUSQUEDAS")
print("=" * 60)

print("\n1. TAMANO DEL CONJUNTO DE DATOS")
print(f"Total de registros: {len(busquedas):,}".replace(",", "."))
print(f"Total de columnas: {len(busquedas.columns)}")

print("\n2. COLUMNAS DISPONIBLES")
for columna in busquedas.columns:
    print(f"- {columna}")

print("\n3. PRIMEROS CINCO REGISTROS")
print(busquedas.head().to_string(index=False))

print("\n4. TIPOS DE DATOS")
print(busquedas.dtypes.to_string())

print("\n5. DATOS FALTANTES POR COLUMNA")
faltantes = pd.DataFrame({
    "Columna": busquedas.columns,
    "Datos faltantes": busquedas.isna().sum().values,
    "Porcentaje (%)": (
        busquedas.isna().mean().values * 100
    ).round(2)
})

print(
    faltantes.sort_values(
        "Datos faltantes",
        ascending=False
    ).to_string(index=False)
)

print("\n6. CALIDAD DE LOS DATOS")
print(
    "Filas duplicadas exactas: "
    f"{busquedas.duplicated().sum()}"
)

print("\n7. ESTADISTICAS NUMERICAS")
numericas = busquedas.select_dtypes(include="number")

if not numericas.empty:
    print(numericas.describe().round(2).to_string())
else:
    print("No se encontraron variables numericas.")

print("\n8. VARIABLES CATEGORICAS")
categoricas = busquedas.select_dtypes(
    include=["object", "category", "bool"]
)

for columna in categoricas.columns:
    print(f"\nColumna: {columna}")
    print(
        "Valores diferentes: "
        f"{busquedas[columna].nunique(dropna=True)}"
    )
    print("Cinco valores mas frecuentes:")
    print(
        busquedas[columna]
        .value_counts(dropna=True)
        .head(5)
        .to_string()
    )

faltantes.to_csv(
    salida / "auditoria_busquedas.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nINSPECCION TERMINADA")
print("Resumen guardado en resultados/auditoria_busquedas.csv")
