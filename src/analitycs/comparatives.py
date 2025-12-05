import pandas as pd


def monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["Año", "Mes", "Sucursal"], as_index=False)[["Cantidad", "ImporteTotal"]]
        .sum()
    )
