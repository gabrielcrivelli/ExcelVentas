import sys
from pathlib import Path
# Agregar el directorio raíz al path para permitir imports desde src/
PROJECT_ROOT = Path(__file__).parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd

from src.utils.constants import PROCESSED_DIR
from src.analytics.kpis import compute_kpis
from src.visualization.charts import bar_sales_by_department, line_monthly_sales

st.title("📊 Dashboard Ejecutivo")

processed_path = Path(PROCESSED_DIR) / "ventas_procesadas.parquet"

if not processed_path.exists():
    st.info("Primeró procesá datos en la página principal.")
else:
    df = pd.read_parquet(processed_path)
    kpis = compute_kpis(df)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Facturación total", f"${kpis['total_sales']:,.0f}")
    col2.metric("Unidades", f"{kpis['total_units']:,.0f}")
    col3.metric("Ticket promedio", f"${kpis['avg_ticket']:,.0f}")
    col4.metric("SKUs", f"{kpis['unique_skus']}")

    st.plotly_chart(bar_sales_by_department(df), width='stretch')
    st.plotly_chart(line_monthly_sales(df), width='stretch')
