import streamlit as st
from pathlib import Path
import pandas as pd

from src.utils.constants import PROCESSED_DIR
from src.analytics.analysis import abc_by_revenue
from src.analytics.kpis import compute_kpis
from src.visualization.charts import bar_sales_by_department  # opcional


st.set_page_config(page_title="Análisis ABC", layout="wide")
st.title("🔠 Análisis ABC por Facturación")

processed_path = Path(PROCESSED_DIR) / "ventas_procesadas.parquet"

if not processed_path.exists():
    st.info("Primero procesá y guardá datos consolidados (por ejemplo desde la página principal / Dashboard).")
    st.stop()

# Cargar datos
df = pd.read_parquet(processed_path)

# KPIs globales
kpis = compute_kpis(df)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Facturación total", f"${kpis['facturacion_total']:,.0f}")
c2.metric("Unidades totales", f"{kpis['unidades_totales']:,.0f}")
c3.metric("Ticket promedio", f"${kpis['ticket_promedio']:,.0f}")
c4.metric("SKUs activos", f"{kpis['skus']}")

st.markdown("---")

# Filtros
col_f1, col_f2 = st.columns(2)
sucursales = ["Todas"] + sorted(df["Sucursal"].dropna().unique().tolist())
sucursal_sel = col_f1.selectbox("Sucursal", sucursales)

if sucursal_sel != "Todas":
    df_filtrado = df[df["Sucursal"] == sucursal_sel]
else:
    df_filtrado = df

# Calcular ABC
tabla_abc = abc_by_revenue(df_filtrado)

# Resumen por clase
resumen = (
    tabla_abc.groupby("ABC", as_index=False)["ImporteTotal"]
    .sum()
    .rename(columns={"ImporteTotal": "Facturacion"})
)
total_fact = resumen["Facturacion"].sum()
resumen["% Facturacion"] = (resumen["Facturacion"] / total_fact * 100).round(2)

st.subheader("Distribución ABC")
st.dataframe(resumen, use_container_width=True)

# Filtro por clase ABC
clase_sel = st.radio(
    "Clase ABC a mostrar",
    options=["Todas", "A", "B", "C"],
    horizontal=True,
)

if clase_sel != "Todas":
    tabla_mostrar = tabla_abc[tabla_abc["ABC"] == clase_sel]
else:
    tabla_mostrar = tabla_abc

st.subheader("Detalle de productos (ordenados por facturación)")
st.dataframe(
    tabla_mostrar[
        ["IdArticulo", "Descripcion", "Marca", "ImporteTotal", "Facturacion_Acum", "Pct_Acum", "ABC"]
    ].style.format({"ImporteTotal": "{:,.0f}", "Facturacion_Acum": "{:,.0f}", "Pct_Acum": "{:.2f}"}),
    use_container_width=True,
    height=500,
)

st.caption("Los productos A concentran aprox. 80% de la facturación; B el siguiente ~15%; C el resto.")
