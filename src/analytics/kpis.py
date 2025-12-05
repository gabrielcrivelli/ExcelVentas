"""
Cálculo de KPIs principales.
"""

import pandas as pd


def compute_kpis(df: pd.DataFrame) -> dict:
    """
    Calcula KPIs principales del dataset consolidado:
    - Facturación total
    - Unidades vendidas
    - Ticket promedio
    - Cantidad de SKUs únicos
    """
    total_sales = df["ImporteTotal"].sum()
    total_units = df["Cantidad"].sum()
    avg_ticket = total_sales / df["IdArticulo"].nunique() if df["IdArticulo"].nunique() > 0 else 0
    unique_skus = df["IdArticulo"].nunique()

    return {
        "total_sales": total_sales,
        "total_units": total_units,
        "avg_ticket": avg_ticket,
        "unique_skus": unique_skus,
    }
