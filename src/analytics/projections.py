"""
Proyecciones de stock y velocidad de venta.
"""

import pandas as pd


def top_velocity(df: pd.DataFrame, top_n: int = 50) -> pd.DataFrame:
    """
    Calcula los artículos de mayor velocidad (unidades / mes).
    """
    agg = df.groupby("IdArticulo", as_index=False).agg(
        {"Cantidad": "sum", "Descripcion": "first"}
    )
    months = df[["Año", "Mes"]].drop_duplicates().shape[0]
    agg["VelocidadMensual"] = agg["Cantidad"] / months if months > 0 else 0
    return agg.sort_values("VelocidadMensual", ascending=False).head(top_n)
