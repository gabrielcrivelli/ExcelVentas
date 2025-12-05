"""
Análisis comparativos mensuales
"""

import pandas as pd


def monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrupa ventas por Año y Mes.
    """
    return df.groupby(["Año", "Mes"], as_index=False).agg({"ImporteTotal": "sum"})
