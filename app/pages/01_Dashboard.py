import streamlit as st
import pandas as pd
from pathlib import Path

from src.utils.constants import PROCESSED_DIR
from src.analytics.kpis import compute_kpis
from src.visualization.charts import bar_sales_by_department, line_monthly_sales

st.title("📊 Dashboard Ejecutivo")

processed_path = Path(PROCESSED_DIR) / "ventas_procesadas.parquet"

if not processed_path.exists():
    st.info("Primero procesá datos en la página principal.")
else:
    df = pd.read_parquet(processed_path)
    kpis = compute_kpis(df)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Facturación total", f"${kpis['facturacion_total']:,.0f}")
    col2.metric("Unidades", f"{kpis['unidades_totales']:,.0f}")
    col3.metric("Ticket promedio", f"${kpis['ticket_promedio']:,.0f}")
    col4.metric("SKUs", f"{kpis['skus']}")

    st.plotly_chart(bar_sales_by_department(df), use_container_width=True)
    st.plotly_chart(line_monthly_sales(df), use_container_width=True)
