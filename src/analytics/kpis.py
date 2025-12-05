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
    # Validar que el dataframe no esté vacío
    if df is None or len(df) == 0:
        return {
            "total_sales": 0,
            "total_units": 0,
            "avg_ticket": 0,
            "unique_skus": 0,
        }
    
    # Usar columnas reales del dataframe
    # Obtener el nombre correcto de la columna de importe
    importe_col = None
    for col in df.columns:
        if col.lower() in ['importetotal', 'importe_total', 'importe', 'total']:
            importe_col = col
            break
    
    # Obtener el nombre correcto de la columna de cantidad
    cantidad_col = None
    for col in df.columns:
        if col.lower() in ['cantidad', 'qty', 'quantity']:
            cantidad_col = col
            break
    
    # Obtener el nombre correcto de la columna de ID de artículo
    idarticulo_col = None
    for col in df.columns:
        if col.lower() in ['idarticulo', 'id_articulo', 'sku', 'product_id']:
            idarticulo_col = col
            break
    
    # Calcular KPIs con validación
    total_sales = 0
    total_units = 0
    unique_skus = 0
    
    if importe_col and importe_col in df.columns:
        total_sales = df[importe_col].sum()
    
    if cantidad_col and cantidad_col in df.columns:
        total_units = df[cantidad_col].sum()
    
    if idarticulo_col and idarticulo_col in df.columns:
        unique_skus = df[idarticulo_col].nunique()
    
    # Calcular ticket promedio
    avg_ticket = total_sales / total_units if total_units > 0 else 0
    
    return {
        "total_sales": total_sales,
        "total_units": total_units,
        "avg_ticket": avg_ticket,
        "unique_skus": unique_skus,
    }
