"""
Netflix Intelligence
Inspeccion y auditoria del historial de visualizacion
Curso: Fundamentos de analisis cuantitativo

El archivo original watch_history.csv no se modifica.
"""

from pathlib import Path
import pandas as pd

# ============================================================
# 1. CONFIGURACION DE RUTAS
# ============================================================

RUTA_DATOS = Path("data") / "watch_history.csv"
CARPETA_RESULTADOS = Path("resultados")
CARPETA_RESULTADOS.mkdir(parents=True, exist_ok=True)

if not RUTA_DATOS.exists():
    raise FileNotFoundError(
        "No se encuentra data/watch_history.csv. "
        "Verifica que el archivo exista en la carpeta data."
    )

# ============================================================
# 2. CARGA DE DATOS
# ============================================================

historial = pd.read_csv(RUTA_DATOS)

# Se excluyen duplicados exactos solo en memoria; el CSV original se conserva.
_duplicados_exactos = int(historial.duplicated().sum())
if _duplicados_exactos:
    print(f"Filas duplicadas exactas excluidas del análisis: {_duplicados_exactos:,}")
historial = historial.drop_duplicates().copy()

total_registros = len(historial)
total_columnas = len(historial.columns)

print("=" * 68)
print("NETFLIX INTELLIGENCE")
print("INSPECCION Y AUDITORIA DEL HISTORIAL DE VISUALIZACION")
print("=" * 68)

print("\n1. TAMANO DEL CONJUNTO DE DATOS")
print(f"Total de registros: {total_registros:,}".replace(",", "."))
print(f"Total de columnas: {total_columnas}")

# ============================================================
# 3. NOMBRES DESCRIPTIVOS DE LAS COLUMNAS
# ============================================================

traducciones_columnas = {
    "session_id": "Identificador de la sesion",
    "user_id": "Identificador del usuario",
    "movie_id": "Identificador del contenido",
    "watch_date": "Fecha de visualizacion",
    "device_type": "Tipo de dispositivo",
    "watch_duration_minutes": "Duracion de visualizacion (minutos)",
    "progress_percentage": "Porcentaje de reproduccion",
    "action": "Accion de visualizacion",
    "quality": "Calidad de reproduccion",
    "location_country": "Pais de ubicacion",
    "is_download": "Contenido descargado",
    "user_rating": "Calificacion del usuario",
}

print("\n2. COLUMNAS DISPONIBLES")

for columna in historial.columns:
    nombre = traducciones_columnas.get(columna, columna)
    print(f"- {nombre} ({columna})")

# ============================================================
# 4. PRIMEROS CINCO REGISTROS
# ============================================================

print("\n3. PRIMEROS CINCO REGISTROS")

muestra = historial.head().copy()

muestra.rename(
    columns={
        columna: traducciones_columnas.get(columna, columna)
        for columna in muestra.columns
    },
    inplace=True,
)

# Traducciones para la presentacion.
# No modifican los valores del archivo CSV original.
traducciones_valores = {
    "device_type": {
        "Tablet": "Tableta",
        "Laptop": "Portatil",
        "Desktop": "Computador de escritorio",
        "Mobile": "Celular",
        "Smart TV": "Televisor inteligente",
    },
    "action": {
        "completed": "Completado",
        "started": "Iniciado",
        "paused": "Pausado",
        "stopped": "Detenido",
        "downloaded": "Descargado",
    },
    "quality": {
        "HD": "Alta definicion",
        "SD": "Definicion estandar",
        "UHD": "Ultra alta definicion",
        "4K": "Resolucion 4K",
    },
}

for columna, mapa in traducciones_valores.items():
    if columna in historial.columns:
        nombre_traducido = traducciones_columnas.get(
            columna, columna
        )
        muestra[nombre_traducido] = (
            muestra[nombre_traducido].replace(mapa)
        )

if "is_download" in historial.columns:
    nombre = traducciones_columnas["is_download"]
    muestra[nombre] = muestra[nombre].map(
        {True: "Si", False: "No"}
    ).fillna(muestra[nombre])

print(muestra.to_string(index=False))

# ============================================================
# 5. TIPOS DE DATOS Y VALORES FALTANTES
# ============================================================

print("\n4. TIPOS DE DATOS Y VALORES FALTANTES")

faltantes = historial.isna().sum()
porcentajes_faltantes = (
    faltantes / total_registros * 100
    if total_registros > 0
    else pd.Series(0.0, index=historial.columns)
)

informe_columnas = pd.DataFrame({
    "columna_original": historial.columns,
    "nombre_descriptivo": [
        traducciones_columnas.get(columna, columna)
        for columna in historial.columns
    ],
    "tipo_de_dato": [
        str(historial[columna].dtype)
        for columna in historial.columns
    ],
    "valores_faltantes": [
        int(faltantes[columna])
        for columna in historial.columns
    ],
    "porcentaje_faltantes": [
        round(float(porcentajes_faltantes[columna]), 2)
        for columna in historial.columns
    ],
})

print(
    informe_columnas[
        [
            "nombre_descriptivo",
            "tipo_de_dato",
            "valores_faltantes",
            "porcentaje_faltantes",
        ]
    ].to_string(index=False)
)

total_celdas_vacias = int(faltantes.sum())
columnas_con_faltantes = int((faltantes > 0).sum())

print(
    "\nTotal de celdas vacias: "
    f"{total_celdas_vacias:,}".replace(",", ".")
)
print(
    f"Columnas con valores faltantes: "
    f"{columnas_con_faltantes} de {total_columnas}"
)

# ============================================================
# 6. REVISION DE DUPLICADOS
# ============================================================

print("\n5. REVISION DE DUPLICADOS")

duplicados_exactos = int(historial.duplicated().sum())

porcentaje_duplicados = (
    duplicados_exactos / total_registros * 100
    if total_registros > 0
    else 0.0
)

print(f"Filas duplicadas exactas: {duplicados_exactos:,}")
print(
    "Porcentaje de filas duplicadas exactas: "
    f"{porcentaje_duplicados:.2f} %".replace(".", ",")
)

# Los usuarios pueden tener muchas sesiones.
# Repetir user_id no es por si solo un error.
if "session_id" in historial.columns:
    repeticiones_sesion = int(
        historial["session_id"].duplicated().sum()
    )
    print(
        "Repeticiones adicionales del identificador de sesion: "
        f"{repeticiones_sesion:,}"
    )

if "user_id" in historial.columns:
    usuarios_repetidos = int(
        historial["user_id"].duplicated().sum()
    )
    print(
        "Repeticiones adicionales del identificador de usuario: "
        f"{usuarios_repetidos:,}"
    )

print(
    "Nota: no se eliminan duplicados ni identificadores repetidos "
    "automaticamente."
)

# ============================================================
# 7. VALIDACION DE FECHAS
# ============================================================

print("\n6. VALIDACION DE FECHAS")

if "watch_date" in historial.columns:
    fechas = pd.to_datetime(
        historial["watch_date"],
        errors="coerce"
    )

    fechas_invalidas = int(
        historial["watch_date"].notna().sum()
        - fechas.notna().sum()
    )
    fechas_faltantes = int(historial["watch_date"].isna().sum())

    print(f"Fechas validas: {int(fechas.notna().sum()):,}")
    print(f"Fechas faltantes: {fechas_faltantes:,}")
    print(f"Fechas no interpretables: {fechas_invalidas:,}")

    if fechas.notna().any():
        print(
            "Fecha mas antigua: "
            f"{fechas.min().strftime('%Y-%m-%d')}"
        )
        print(
            "Fecha mas reciente: "
            f"{fechas.max().strftime('%Y-%m-%d')}"
        )
else:
    fechas_invalidas = 0
    fechas_faltantes = 0
    print("No existe la columna watch_date.")

# ============================================================
# 8. VALIDACION DE DURACION
# ============================================================

print("\n7. VALIDACION DE LA DURACION")

if "watch_duration_minutes" in historial.columns:
    duracion = pd.to_numeric(
        historial["watch_duration_minutes"],
        errors="coerce"
    )

    duracion_negativa = int((duracion < 0).sum())
    duracion_cero = int((duracion == 0).sum())
    duracion_faltante = int(duracion.isna().sum())

    print(f"Duraciones faltantes o no numericas: {duracion_faltante:,}")
    print(f"Duraciones negativas: {duracion_negativa:,}")
    print(f"Duraciones iguales a cero: {duracion_cero:,}")

    duracion_valida = duracion[duracion >= 0]

    if not duracion_valida.empty:
        print(
            "Duracion media valida (minutos): "
            f"{duracion_valida.mean():.2f}".replace(".", ",")
        )
        print(
            "Duracion mediana valida (minutos): "
            f"{duracion_valida.median():.2f}".replace(".", ",")
        )
        print(
            "Duracion maxima no negativa (minutos): "
            f"{duracion_valida.max():.2f}".replace(".", ",")
        )
else:
    duracion_negativa = 0
    duracion_cero = 0
    duracion_faltante = 0
    print("No existe la columna watch_duration_minutes.")

# ============================================================
# 9. VALIDACION DEL PORCENTAJE DE REPRODUCCION
# ============================================================

print("\n8. VALIDACION DEL PORCENTAJE DE REPRODUCCION")

if "progress_percentage" in historial.columns:
    progreso = pd.to_numeric(
        historial["progress_percentage"],
        errors="coerce"
    )

    progreso_fuera_rango = int(
        ((progreso < 0) | (progreso > 100)).sum()
    )
    progreso_faltante = int(progreso.isna().sum())

    print(
        "Porcentajes faltantes o no numericos: "
        f"{progreso_faltante:,}"
    )
    print(
        "Porcentajes fuera del rango de 0 a 100: "
        f"{progreso_fuera_rango:,}"
    )

    progreso_valido = progreso[
        progreso.between(0, 100, inclusive="both")
    ]

    if not progreso_valido.empty:
        print(
            "Porcentaje medio valido: "
            f"{progreso_valido.mean():.2f} %".replace(".", ",")
        )
        print(
            "Porcentaje minimo valido: "
            f"{progreso_valido.min():.2f} %".replace(".", ",")
        )
        print(
            "Porcentaje maximo valido: "
            f"{progreso_valido.max():.2f} %".replace(".", ",")
        )
else:
    progreso_fuera_rango = 0
    progreso_faltante = 0
    print("No existe la columna progress_percentage.")

# ============================================================
# 10. VALIDACION DE CALIFICACIONES
# ============================================================

print("\n9. VALIDACION DE CALIFICACIONES")

if "user_rating" in historial.columns:
    calificacion = pd.to_numeric(
        historial["user_rating"],
        errors="coerce"
    )

    calificaciones_faltantes = int(calificacion.isna().sum())

    # Se supone una escala de 1 a 5 porque los datos de reseñas
    # del proyecto utilizan esa escala. Los valores fuera de ella
    # se reportan para revision, no se modifican.
    calificaciones_fuera_rango = int(
        (
            calificacion.notna()
            & ~calificacion.between(1, 5, inclusive="both")
        ).sum()
    )

    print(
        f"Calificaciones faltantes o no numericas: "
        f"{calificaciones_faltantes:,}"
    )
    print(
        "Calificaciones fuera de la escala de 1 a 5: "
        f"{calificaciones_fuera_rango:,}"
    )

    calificaciones_validas = calificacion[
        calificacion.between(1, 5, inclusive="both")
    ]

    if not calificaciones_validas.empty:
        print(
            "Calificacion media valida: "
            f"{calificaciones_validas.mean():.2f} sobre 5"
        )
else:
    calificaciones_faltantes = 0
    calificaciones_fuera_rango = 0
    print("No existe la columna user_rating.")

# ============================================================
# 11. RESUMEN GENERAL DE CALIDAD
# ============================================================

print("\n10. RESUMEN GENERAL DE CALIDAD")

indicadores = {
    "total_registros": total_registros,
    "total_columnas": total_columnas,
    "total_celdas_vacias": total_celdas_vacias,
    "columnas_con_faltantes": columnas_con_faltantes,
    "filas_duplicadas_exactas": duplicados_exactos,
    "porcentaje_filas_duplicadas": round(porcentaje_duplicados, 2),
    "fechas_no_interpretables": fechas_invalidas,
    "duraciones_negativas": duracion_negativa,
    "porcentajes_reproduccion_fuera_rango": progreso_fuera_rango,
    "calificaciones_fuera_rango_1_5": calificaciones_fuera_rango,
}

for nombre, valor in indicadores.items():
    print(f"- {nombre}: {valor}")

# ============================================================
# 12. EXPORTACION DE INFORMES
# ============================================================

# Informe de columnas, tipos y valores faltantes.
informe_columnas.to_csv(
    CARPETA_RESULTADOS / "inspeccion_historial.csv",
    index=False,
    encoding="utf-8-sig"
)

# Informe de valores faltantes.
informe_columnas[
    [
        "columna_original",
        "nombre_descriptivo",
        "valores_faltantes",
        "porcentaje_faltantes",
    ]
].to_csv(
    CARPETA_RESULTADOS / "valores_faltantes_historial.csv",
    index=False,
    encoding="utf-8-sig"
)

# Resumen general.
pd.DataFrame({
    "indicador": list(indicadores.keys()),
    "valor": list(indicadores.values()),
}).to_csv(
    CARPETA_RESULTADOS / "resumen_calidad_historial.csv",
    index=False,
    encoding="utf-8-sig"
)

# Informe de registros que necesitan revision.
registros_revision = pd.DataFrame(index=historial.index)

if "session_id" in historial.columns:
    registros_revision["session_id"] = historial["session_id"]

if "user_id" in historial.columns:
    registros_revision["user_id"] = historial["user_id"]

if "watch_date" in historial.columns:
    registros_revision["watch_date_original"] = historial["watch_date"]
    registros_revision["fecha_no_interpretable"] = (
        historial["watch_date"].notna()
        & pd.to_datetime(
            historial["watch_date"],
            errors="coerce"
        ).isna()
    )

if "watch_duration_minutes" in historial.columns:
    registros_revision["duracion_negativa"] = (
        pd.to_numeric(
            historial["watch_duration_minutes"],
            errors="coerce"
        ) < 0
    )

if "progress_percentage" in historial.columns:
    valores_progreso = pd.to_numeric(
        historial["progress_percentage"],
        errors="coerce"
    )
    registros_revision["progreso_fuera_rango"] = (
        valores_progreso.notna()
        & ~valores_progreso.between(
            0, 100, inclusive="both"
        )
    )

if "user_rating" in historial.columns:
    valores_calificacion = pd.to_numeric(
        historial["user_rating"],
        errors="coerce"
    )
    registros_revision["calificacion_fuera_rango"] = (
        valores_calificacion.notna()
        & ~valores_calificacion.between(
            1, 5, inclusive="both"
        )
    )

columnas_revision = [
    columna
    for columna in registros_revision.columns
    if columna not in ["session_id", "user_id", "watch_date_original"]
]

if columnas_revision:
    mascara_revision = registros_revision[columnas_revision].any(axis=1)
    detalle_revision = registros_revision.loc[mascara_revision].copy()
else:
    detalle_revision = registros_revision.iloc[0:0].copy()

detalle_revision.to_csv(
    CARPETA_RESULTADOS / "registros_para_revision_historial.csv",
    index=False,
    encoding="utf-8-sig"
)

# ============================================================
# 13. FINALIZACION
# ============================================================

print("\n11. INFORMES GENERADOS")
print("- resultados/inspeccion_historial.csv")
print("- resultados/valores_faltantes_historial.csv")
print("- resultados/resumen_calidad_historial.csv")
print("- resultados/registros_para_revision_historial.csv")

print("\nINSPECCION TERMINADA")
print("El archivo original watch_history.csv no fue modificado.")
print("=" * 68)