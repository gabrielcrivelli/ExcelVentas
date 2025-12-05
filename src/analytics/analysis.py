"""
Funciones de análisis (ABC, etc.)
"""

import pandas as pd


def abc_by_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula clasificación ABC de productos por facturación acumulada:
    - A: Top 80%
    - B: Siguiente 15%
    - C: Último 5%
    """
    agg = df.groupby("IdArticulo", as_index=False).agg(
        {"ImporteTotal": "sum", "Descripcion": "first"}
    )
    agg = agg.sort_values("ImporteTotal", ascending=False).reset_index(drop=True)
    total_revenue = agg["ImporteTotal"].sum()
    agg["cumsum_revenue"] = agg["ImporteTotal"].cumsum()
    agg["%_acum"] = agg["cumsum_revenue"] / total_revenue * 100

    agg["Clasificacion"] = "C"
    agg.loc[agg["%_acum"] <= 80, "Clasificacion"] = "A"
    agg.loc[(agg["%_acum"] > 80) & (agg["%_acum"] <= 95), "Clasificacion"] = "B"

    return agg
