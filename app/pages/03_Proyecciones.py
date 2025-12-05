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
from src.analytics.projections import top_velocity

st.set_page_config(page_title="Proyecciones de Stock", layout="wide")

st.title("🚀 Proyecciones de Stock")
st.write("Identifica productos con mayor velocidad de venta para proyectar necesidades de stock.")

processed_path = Path(PROCESSED_DIR) / "ventas_procesadas.parquet"

if not processed_path.exists():
    st.info("Primeró procesá datos en la página principal.")
else:
    df = pd.read_parquet(processed_path)

    top_n = st.slider("Cantidad de productos a mostrar", 10, 100, 50)
    top_vel = top_velocity(df, top_n=top_n)

    st.subheader(f"🔝 Top {top_n} productos por velocidad")
    st.dataframe(top_vel, width='stretch')

    # Botón para descargar Excel
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        top_vel.to_excel(writer, index=False, sheet_name="TopVelocidad")
    buffer.seek(0)

    st.download_button(
        label="⬇️ Descargar Excel",
        data=buffer,
        file_name="top_velocidad.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
