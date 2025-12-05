"""
Funciones de análisis (ABC, etc.)
"""

import pandas as pd


def _find_column(df: pd.DataFrame, possible_names: list) -> str:
    """Busca la primera columna que coincida con los nombres posibles."""
    for name in possible_names:
        for col in df.columns:
            if col.lower() == name.lower():
                return col
    return None


def abc_by_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula clasificación ABC de productos por facturación acumulada:
    - A: Top 80%
    - B: Siguiente 15%
    - C: Último 5%
    """
    if df is None or len(df) == 0:
        return pd.DataFrame()
    
    # Buscar columnas necesarias
    id_col = _find_column(df, ['idarticulo', 'id_articulo', 'sku', 'product_id'])
    importe_col = _find_column(df, ['importetotal', 'importe_total', 'importe', 'total'])
    desc_col = _find_column(df, ['descripcion', 'description', 'name'])
    
    if not id_col or not importe_col:
        return pd.DataFrame()
    
    # Agrupar por producto
    agg = df.groupby(id_col, as_index=False).agg({
        importe_col: 'sum',
        desc_col: 'first' if desc_col else 'count'
    }) if desc_col else df.groupby(id_col, as_index=False).agg({
        importe_col: 'sum'
    })
    
    # Ordenar por importe
    agg = agg.sort_values(importe_col, ascending=False).reset_index(drop=True)
    total_revenue = agg[importe_col].sum()
    
    # Calcular acumulado y porcentaje
    agg['cumsum_revenue'] = agg[importe_col].cumsum()
    agg['%_acum'] = agg['cumsum_revenue'] / total_revenue * 100
    
    # Clasificar
    agg['Clasificacion'] = 'C'
    agg.loc[agg['%_acum'] <= 80, 'Clasificacion'] = 'A'
    agg.loc[(agg['%_acum'] > 80) & (agg['%_acum'] <= 95), 'Clasificacion'] = 'B'
    
    return agg
