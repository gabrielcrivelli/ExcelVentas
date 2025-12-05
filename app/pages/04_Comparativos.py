import sys
from pathlib import Path
# Agregar el directorio raíz al path para permitir imports desde src/
PROJECT_ROOT = Path(__file__).parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd

from src.utils.constants import PROCESSED_DIR
from src.analytics.comparatives import monthly_summary
from src.visualization.charts import line_monthly_sales

st.set_page_config(page_title="Comparativos Mensuales", layout="wide")

st.title("📅 Comparativos Mensuales")
st.write("Evolución de las ventas mes a mes.")

processed_path = Path(PROCESSED_DIR) / "ventas_procesadas.parquet"

if not processed_path.exists():
    st.info("Primeró procesá datos en la página principal.")
else:
    df = pd.read_parquet(processed_path)
    summary = monthly_summary(df)

    st.subheader("📊 Facturación mensual")
    st.dataframe(summary, width='stretch')

    st.subheader("📈 Gráfico de evolución")
    st.plotly_chart(line_monthly_sales(df), width='stretch')
