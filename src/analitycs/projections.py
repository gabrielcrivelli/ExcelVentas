import pandas as pd


def top_velocity(df: pd.DataFrame, n: int = 50) -> pd.DataFrame:
    cols = [
        "Sucursal", "IdArticulo", "Descripcion", "Marca",
        "Departamento", "Familia",
        "Venta_Diaria_Prom", "Stock_15_Dias", "Stock_30_Dias", "Stock_60_Dias",
    ]
    cols = [c for c in cols if c in df.columns]
    return (
        df[cols]
        .drop_duplicates(subset=["Sucursal", "IdArticulo"])
        .sort_values("Venta_Diaria_Prom", ascending=False)
        .head(n)
    )
