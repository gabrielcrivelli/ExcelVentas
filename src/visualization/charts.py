import pandas as pd
import plotly.express as px


def bar_sales_by_department(df: pd.DataFrame):
    agg = (
        df.groupby("Departamento", as_index=False)[["Cantidad", "ImporteTotal"]]
        .sum()
        .sort_values("ImporteTotal", ascending=False)
    )
    fig = px.bar(
        agg,
        x="ImporteTotal",
        y="Departamento",
        orientation="h",
        title="Facturación por Departamento",
        labels={"ImporteTotal": "Facturación", "Departamento": "Departamento"},
    )
    return fig


def line_monthly_sales(df: pd.DataFrame):
    agg = (
        df.groupby(["Año", "Mes"], as_index=False)[["ImporteTotal"]]
        .sum()
        .sort_values(["Año", "Mes"])
    )
    agg["Periodo"] = agg["Año"].astype(str) + "-" + agg["Mes"].astype(str).str.zfill(2)
    fig = px.line(
        agg,
        x="Periodo",
        y="ImporteTotal",
        title="Evolución Mensual de Facturación",
        markers=True,
    )
    return fig
