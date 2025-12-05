"""
DataCleaner - limpieza y normalización básica.
"""

import pandas as pd


def clean_and_enrich(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Fechas
    df["FechaComprobante"] = pd.to_datetime(df["FechaComprobante"], errors="coerce")

    # Textos
    for col in ["Departamento", "Familia", "SubFamilia", "Marca", "Descripcion"]:
        df[col] = df[col].astype(str).str.strip()

    # Derivadas de fecha
    df["Año"] = df["FechaComprobante"].dt.year
    df["Mes"] = df["FechaComprobante"].dt.month
    df["Día"] = df["FechaComprobante"].dt.day
    df["DiaSemana_Num"] = df["FechaComprobante"].dt.dayofweek
    df["DiaSemana_Nom"] = df["FechaComprobante"].dt.day_name()

    return df
