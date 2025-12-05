import sys
from pathlib import Path
# Agregar el directorio raíz al path para permitir imports desde src/
PROJECT_ROOT = Path(__file__).parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd

from src.utils.constants import PROCESSED_DIR
from src.analytics.analysis import abc_by_revenue
from src.analytics.kpis import compute_kpis

st.title("🅰️🅱️🅾️ Análisis ABC")
st.write("Clasificación de productos según su contribución a la facturación.")

processed_path = Path(PROCESSED_DIR) / "ventas_procesadas.parquet"

if not processed_path.exists():
    st.info("Primeró procesá datos en la página principal.")
else:
    df = pd.read_parquet(processed_path)
    abc = abc_by_revenue(df)

    st.subheader("📈 Distribución ABC")
    dist = abc["Clasificacion"].value_counts()
    st.write(f"- **A**: {dist.get('A', 0)} productos ({dist.get('A', 0)/len(abc)*100:.1f}%)")
    st.write(f"- **B**: {dist.get('B', 0)} productos ({dist.get('B', 0)/len(abc)*100:.1f}%)")
    st.write(f"- **C**: {dist.get('C', 0)} productos ({dist.get('C', 0)/len(abc)*100:.1f}%)")

    st.subheader("📊 Tabla ABC completa")
    st.dataframe(abc, width='stretch')
