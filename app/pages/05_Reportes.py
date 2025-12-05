import streamlit as st
from pathlib import Path
import pandas as pd
import io

from src.utils.constants import PROCESSED_DIR
from src.analytics.kpis import compute_kpis
from src.analytics.analysis import abc_by_revenue
from src.analytics.projections import top_velocity


st.set_page_config(page_title="Reportes", layout="wide")
st.title("📑 Reportes Ejecutivos")

processed_path = Path(PROCESSED_DIR) / "ventas_procesadas.parquet"

if not processed_path.exists():
    st.info("Primero procesá y guardá datos consolidados (por ejemplo desde la página principal / Dashboard).")
    st.stop()

df = pd.read_parquet(processed_path)

tipo_reporte = st.radio(
    "Tipo de reporte",
    options=["Ejecutivo (Excel)", "Detalle ABC (Excel)", "Top Velocidad (Excel)", "PDF (futuro)"],
    horizontal=True,
)

if tipo_reporte == "Ejecutivo (Excel)":
    st.subheader("Reporte Ejecutivo (Excel)")

    kpis = compute_kpis(df)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Facturación total", f"${kpis['facturacion_total']:,.0f}")
    c2.metric("Unidades totales", f"{kpis['unidades_totales']:,.0f}")
    c3.metric("Ticket promedio", f"${kpis['ticket_promedio']:,.0f}")
    c4.metric("SKUs", f"{kpis['skus']}")

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Detalle")
    buffer.seek(0)

    st.download_button(
        label="⬇️ Descargar reporte ejecutivo (Excel)",
        data=buffer,
        file_name="reporte_ejecutivo.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

elif tipo_reporte == "Detalle ABC (Excel)":
    st.subheader("Reporte ABC (Excel)")

    tabla_abc = abc_by_revenue(df)
    st.dataframe(tabla_abc.head(50), use_container_width=True)

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        tabla_abc.to_excel(writer, index=False, sheet_name="ABC")
    buffer.seek(0)

    st.download_button(
        label="⬇️ Descargar detalle ABC (Excel)",
        data=buffer,
        file_name="reporte_abc.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

elif tipo_reporte == "Top Velocidad (Excel)":
    st.subheader("Reporte Top Velocidad (Excel)")

    top_n = st.slider("Top N productos", min_value=20, max_value=200, value=50, step=10)
    tabla_top = top_velocity(df, n=top_n)
    st.dataframe(tabla_top, use_container_width=True)

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        tabla_top.to_excel(writer, index=False, sheet_name="Top_Velocidad")
    buffer.seek(0)

    st.download_button(
        label="⬇️ Descargar Top Velocidad (Excel)",
        data=buffer,
        file_name="reporte_top_velocidad.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

else:  # PDF (futuro)
    st.subheader("Reporte PDF (en desarrollo)")
    st.info(
        "Aquí se integrará un generador de PDF (por ejemplo con ReportLab o FPDF) "
        "que combine KPIs, tablas ABC y gráficos clave en un informe ejecutivo listo para enviar."
    )
