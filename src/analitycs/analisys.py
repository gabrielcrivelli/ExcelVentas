import pandas as pd


def abc_by_revenue(df: pd.DataFrame) -> pd.DataFrame:
    tmp = (
        df.groupby(["IdArticulo", "Descripcion", "Marca"], as_index=False)["ImporteTotal"]
        .sum()
        .sort_values("ImporteTotal", ascending=False)
    )
    tmp["Facturacion_Acum"] = tmp["ImporteTotal"].cumsum()
    total = tmp["ImporteTotal"].sum()
    tmp["Pct_Acum"] = tmp["Facturacion_Acum"] / total * 100

    def clasificar(p):
        if p <= 80:
            return "A"
        elif p <= 95:
            return "B"
        return "C"

    tmp["ABC"] = tmp["Pct_Acum"].apply(clasificar)
    return tmp
