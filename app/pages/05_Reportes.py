import sys
from pathlib import Path
# Agregar el directorio raíz al path para permitir imports desde src/
PROJECT_ROOT = Path(__file__).parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd
import io

from src.utils.constants import PROCESSED_DIR
from src.analytics.kpis import compute_kpis
from src.analytics.analysis import abc_by_revenue
from src.analytics.projections import top_velocity

st.set_page_config(page_title="Reportes Consolidados", layout="wide")

st.title("📄 Reportes Consolidados")
st.write("Genera reportes completos con todos los análisis.")

processed_path = Path(PROCESSED_DIR) / "ventas_procesadas.parquet"

if not processed_path.exists():
    st.info("Primeró procesá datos en la página principal.")
else:
    df = pd.read_parquet(processed_path)

    st.subheader("📊 KPIs Principales")
    kpis = compute_kpis(df)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Facturación", f"${kpis['total_sales']:,.0f}")
    col2.metric("Unidades", f"{kpis['total_units']:,.0f}")
    col3.metric("Ticket promedio", f"${kpis['avg_ticket']:,.0f}")
    col4.metric("SKUs", f"{kpis['unique_skus']}")

    # Generar reporte Excel completo
    st.subheader("⬇️ Descargar reporte completo")

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        # Pestaña 1: Datos consolidados
        df.to_excel(writer, index=False, sheet_name="Datos")

        # Pestaña 2: Análisis ABC
        abc = abc_by_revenue(df)
        abc.to_excel(writer, index=False, sheet_name="ABC")

        # Pestaña 3: Top velocidad
        top_vel = top_velocity(df, top_n=100)
        top_vel.to_excel(writer, index=False, sheet_name="TopVelocidad")

    buffer.seek(0)

    st.download_button(
        label="⬇️ Descargar reporte completo Excel",
        data=buffer,
        file_name="reporte_completo.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    st.success("✅ Reporte generado con éxito. Incluías: Datos consolidados, Análisis ABC y Top Velocidad.")
