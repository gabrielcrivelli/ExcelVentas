import streamlit as st
from pathlib import Path
import pandas as pd

from src.utils.constants import PROCESSED_DIR
from src.analytics.comparatives import monthly_summary
from src.visualization.charts import line_monthly_sales


st.set_page_config(page_title="Comparativos", layout="wide")
st.title("📈 Comparativos Mensuales y por Sucursal")

processed_path = Path(PROCESSED_DIR) / "ventas_procesadas.parquet"

if not processed_path.exists():
    st.info("Primero procesá y guardá datos consolidados (por ejemplo desde la página principal / Dashboard).")
    st.stop()

df = pd.read_parquet(processed_path)

# Resumen mensual
resumen_mensual = monthly_summary(df)

# Filtro sucursal
sucursales = ["Todas"] + sorted(resumen_mensual["Sucursal"].dropna().unique().tolist())
sucursal_sel = st.selectbox("Sucursal", sucursales)

if sucursal_sel != "Todas":
    resumen_filtrado = resumen_mensual[resumen_mensual["Sucursal"] == sucursal_sel]
else:
    resumen_filtrado = resumen_mensual

st.subheader("Tabla mensual")
st.dataframe(
    resumen_filtrado.sort_values(["Año", "Mes", "Sucursal"]),
    use_container_width=True,
)

st.subheader("Evolución mensual de facturación (todas las sucursales)")
st.plotly_chart(line_monthly_sales(df), use_container_width=True)

st.caption(
    "Sugerencia: interpretá subas/bajas mes-a-mes en conjunto con cambios de precios, promociones y estacionalidad."
)
