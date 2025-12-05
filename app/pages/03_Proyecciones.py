import streamlit as st
from pathlib import Path
import pandas as pd
import io

from src.utils.constants import PROCESSED_DIR
from src.analytics.projections import top_velocity


st.set_page_config(page_title="Proyecciones de Stock", layout="wide")
st.title("📦 Proyecciones de Stock y Velocidad de Venta")

processed_path = Path(PROCESSED_DIR) / "ventas_procesadas.parquet"

if not processed_path.exists():
    st.info("Primero procesá y guardá datos consolidados (por ejemplo desde la página principal / Dashboard).")
    st.stop()

df = pd.read_parquet(processed_path)

# Filtros
col1, col2, col3 = st.columns(3)
sucursales = ["Todas"] + sorted(df["Sucursal"].dropna().unique().tolist())
sucursal_sel = col1.selectbox("Sucursal", sucursales)

top_n = col2.slider("Top N por velocidad de venta diaria", min_value=10, max_value=200, value=50, step=10)

if sucursal_sel != "Todas":
    df_filtrado = df[df["Sucursal"] == sucursal_sel]
else:
    df_filtrado = df

tabla_top = top_velocity(df_filtrado, n=top_n)

st.subheader("Top productos por velocidad de venta (Venta_Diaria_Prom)")
st.dataframe(
    tabla_top.style.format(
        {
            "Venta_Diaria_Prom": "{:,.2f}",
            "Stock_15_Dias": "{:,.0f}",
            "Stock_30_Dias": "{:,.0f}",
            "Stock_60_Dias": "{:,.0f}",
        }
    ),
    use_container_width=True,
    height=600,
)

# Descarga Excel
buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    tabla_top.to_excel(writer, index=False, sheet_name="Top_Velocidad")
buffer.seek(0)

st.download_button(
    label="⬇️ Descargar Top N en Excel",
    data=buffer,
    file_name=f"top_velocity_{sucursal_sel or 'todas'}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)
