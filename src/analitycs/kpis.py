"""
KPIs básicos a partir de un DataFrame de líneas de venta.
"""

import pandas as pd
from typing import Dict


def compute_kpis(df: pd.DataFrame) -> Dict:
    total_sales = float(df["ImporteTotal"].sum())
    total_units = float(df["Cantidad"].sum())
    num_lines = int(len(df))
    avg_ticket = float(total_sales / num_lines) if num_lines else 0.0

    return {
        "facturacion_total": total_sales,
        "unidades_totales": total_units,
        "lineas": num_lines,
        "ticket_promedio": avg_ticket,
        "skus": int(df["IdArticulo"].nunique()),
        "departamentos": int(df["Departamento"].nunique()),
        "marcas": int(df["Marca"].nunique()),
    }
