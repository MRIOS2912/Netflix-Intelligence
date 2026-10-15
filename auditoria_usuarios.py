"""
Netflix Intelligence
Auditoria inicial de usuarios y edades
Curso: Fundamentos de análisis cuantitativo

Estructura esperada:
Netflix-Intelligence/
├── data/
│   └── users.csv
├── resultados/
└── auditoria_usuarios.py
"""

from pathlib import Path
import pandas as pd

# ============================================================
# 1. CONFIGURACION DE RUTAS
# ============================================================

ruta = Path("data") / "users.csv"
carpeta_resultados = Path("resultados")
carpeta_resultados.mkdir(parents=True, exist_ok=True)

if not ruta.exists():
    raise FileNotFoundError(
        "No se encuentra el archivo data/users.csv. "
        "Verifica que la carpeta data exista y contenga users.csv."
    )

# ============================================================
# 2. CARGA Y DESCRIPCION GENERAL
# ============================================================

usuarios = pd.read_csv(ruta)

print("=" * 65)
print("NETFLIX INTELLIGENCE")
print("AUDITORIA INICIAL DE USUARIOS Y EDADES")
print("=" * 65)

print("\n1. TAMANO DEL CONJUNTO DE DATOS")
print(f"Total de registros: {usuarios.shape[0]:,}")
print(f"Total de columnas: {usuarios.shape[1]}")

print("\n2. COLUMNAS DISPONIBLES")
for columna in usuarios.columns:
    print(f"- {columna}")

# Comprobar que existe la variable necesaria.
if "age" not in usuarios.columns:
    raise KeyError(
        "No existe la columna 'age' en users.csv. "
        "Revisa el nombre de la columna de edad."
    )

# ============================================================
# 3. AUDITORIA DE LA VARIABLE EDAD
# ============================================================

edad = pd.to_numeric(usuarios["age"], errors="coerce")

edades_faltantes = int(edad.isna().sum())
edades_negativas = int((edad < 0).sum())
edades_superiores_100 = int((edad > 100).sum())

# Se consideran validas las edades entre 0 y 100, inclusive.
mascara_valida = edad.between(0, 100, inclusive="both")
mascara_invalida = edad.notna() & ~mascara_valida

# Crear una copia de las edades validas.
# Normalizar el cero para evitar la presentacion de -0.00.
edades_validas = edad[mascara_valida].copy()
edades_validas = edades_validas.mask(edades_validas == 0, 0.0)

edades_invalidas = edad[mascara_invalida]

print("\n3. AUDITORIA DE EDADES")
print(f"Edades numericas registradas: {edad.notna().sum():,}")
print(f"Edades faltantes o no numericas: {edades_faltantes:,}")
print(f"Edades negativas: {edades_negativas:,}")
print(f"Edades superiores a 100: {edades_superiores_100:,}")
print(f"Edades validas entre 0 y 100: {len(edades_validas):,}")
print(f"Edades numericas fuera del rango: {len(edades_invalidas):,}")

# ============================================================
# 4. ESTADISTICAS PRELIMINARES
# ============================================================

print("\n4. ESTADISTICAS PRELIMINARES")
print("Incluyen todos los valores numericos, incluso los atipicos.")

estadisticas_preliminares = edad.describe().round(2)
print(estadisticas_preliminares.to_string())

# ============================================================
# 5. ESTADISTICAS DE EDADES VALIDAS
# ============================================================

print("\n5. ESTADISTICAS DE EDADES VALIDAS")

if not edades_validas.empty:
    estadisticas_validas = edades_validas.describe().round(2)
    print(estadisticas_validas.to_string())
else:
    estadisticas_validas = pd.Series(dtype="float64")
    print("No hay edades validas para calcular estadisticas.")

# ============================================================
# 6. AUDITORIA DE DUPLICADOS
# ============================================================

duplicados_exactos = int(usuarios.duplicated().sum())

print("\n6. CALIDAD DE LOS DATOS")
print(f"Filas duplicadas exactas: {duplicados_exactos:,}")

ids_repetidos = 0
registros_con_id_repetido = 0

if "user_id" in usuarios.columns:
    mascara_id_repetido = usuarios["user_id"].duplicated(keep=False)

    # Repeticiones adicionales, sin contar la primera aparicion.
    ids_repetidos = int(usuarios["user_id"].duplicated().sum())

    # Total de filas pertenecientes a grupos con ID repetido.
    registros_con_id_repetido = int(mascara_id_repetido.sum())

    print(f"Repeticiones adicionales de user_id: {ids_repetidos:,}")
    print(
        "Registros que pertenecen a grupos con user_id repetido: "
        f"{registros_con_id_repetido:,}"
    )
else:
    print(
        "No existe la columna user_id; "
        "no se pudo auditar ese identificador."
    )

print(
    "Nota: los identificadores repetidos deben revisarse. "
    "Por si solos no demuestran que existan registros duplicados."
)

# ============================================================
# 7. DETALLE DE EDADES FUERA DEL RANGO
# ============================================================

archivo_edades_invalidas = (
    carpeta_resultados / "edades_fuera_de_rango.csv"
)

if mascara_invalida.any():
    columnas_detalle = []

    if "user_id" in usuarios.columns:
        columnas_detalle.append("user_id")

    detalle_edades = usuarios.loc[
        mascara_invalida, columnas_detalle
    ].copy()

    detalle_edades["edad_registrada"] = edad[mascara_invalida]

    detalle_edades["motivo_revision"] = edad[mascara_invalida].apply(
        lambda valor: (
            "Edad negativa"
            if valor < 0
            else "Edad superior a 100"
        )
    )

    detalle_edades.to_csv(
        archivo_edades_invalidas,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        "\nDetalle de edades fuera del rango guardado en: "
        f"{archivo_edades_invalidas}"
    )
else:
    # Evitar conservar un informe antiguo si ya no hay casos.
    if archivo_edades_invalidas.exists():
        archivo_edades_invalidas.unlink()

    print("\nNo se encontraron edades numericas fuera del rango.")

# ============================================================
# 8. RESUMEN DE AUDITORIA
# ============================================================

resumen = pd.DataFrame({
    "indicador": [
        "total_registros",
        "total_columnas",
        "edades_numericas_registradas",
        "edades_faltantes_o_no_numericas",
        "edades_negativas",
        "edades_superiores_a_100",
        "edades_validas_entre_0_y_100",
        "edades_numericas_fuera_de_rango",
        "filas_duplicadas_exactas",
        "repeticiones_adicionales_user_id",
        "registros_con_user_id_repetido",
    ],
    "valor": [
        len(usuarios),
        usuarios.shape[1],
        int(edad.notna().sum()),
        edades_faltantes,
        edades_negativas,
        edades_superiores_100,
        len(edades_validas),
        len(edades_invalidas),
        duplicados_exactos,
        ids_repetidos,
        registros_con_id_repetido,
    ],
})

archivo_resumen = carpeta_resultados / "auditoria_inicial.csv"

resumen.to_csv(
    archivo_resumen,
    index=False,
    encoding="utf-8-sig"
)

# ============================================================
# 9. EXPORTACION DE ESTADISTICAS
# ============================================================

if not edades_validas.empty:
    archivo_estadisticas = (
        carpeta_resultados / "estadisticas_edades_validas.csv"
    )

    estadisticas_validas.rename("valor").to_csv(
        archivo_estadisticas,
        header=True,
        encoding="utf-8-sig"
    )

    print(
        "\nEstadisticas de edades validas guardadas en: "
        f"{archivo_estadisticas}"
    )

# ============================================================
# 10. RESULTADO FINAL
# ============================================================

print("\n7. ARCHIVOS GENERADOS")
print(f"- {archivo_resumen}")

if mascara_invalida.any():
    print(f"- {archivo_edades_invalidas}")

if not edades_validas.empty:
    print(f"- {archivo_estadisticas}")

print("\nAUDITORIA TERMINADA")
print("El archivo original users.csv no fue modificado.")
print("=" * 65)