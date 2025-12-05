"""
Aplicación principal de Streamlit - BI Retail Analytics

- Sube múltiples archivos Excel mensuales.
- Consolida, limpia y enriquece los datos.
- Aplica un esquema de salida (detalle/ejecutivo/stock/custom).
- Guarda un parquet central en data/processed/ventas_procesadas.parquet.
- Muestra KPIs y permite descargar un Excel con el resultado.
"""


import io
import sys
from pathlib import Path
# Agregar el directorio raíz al path para permitir imports desde src/
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
import pandas as pd
import streamlit as st

from src.data.data_processor import process_all
from src.utils.constants import RAW_DIR, PROCESSED_DIR, SCHEMAS_CONFIG


st.set_page_config(
    page_title="BI Retail Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📊 BI Retail Analytics")
st.markdown(
    "Plataforma para consolidar ventas mensuales de hipermercado, "
    "calcular KPIs y generar salidas en Excel configurables."
)

# ---------------- SIDEBAR ---------------- #

st.sidebar.header("⚙️ Opciones de procesamiento")

uploaded_files = st.sidebar.file_uploader(
    "📁 Subí uno o más archivos Excel mensuales",
    type=["xlsx"],
    accept_multiple_files=True,
)

schema_name = st.sidebar.selectbox(
    "Esquema de columnas para el Excel de salida",
    options=["detalle", "ejecutivo", "stock_planning", "custom"],
    index=0,
)

custom_cols_str = ""
if schema_name == "custom":
    custom_cols_str = st.sidebar.text_area(
        "Columnas personalizadas (separadas por coma)",
        value="Sucursal,Año,Mes,Departamento,Familia,IdArticulo,Descripcion,Cantidad,ImporteTotal",
        height=80,
    )

run_btn = st.sidebar.button("🚀 Procesar y consolidar")

# ---------------- CONTENIDO PRINCIPAL ---------------- #

st.subheader("1️⃣ Cargar y procesar datos")

st.write(
    "- Subí los archivos Excel mensuales de cada sucursal en la barra lateral.\n"
    "- Elegí el esquema de columnas que querés en el Excel de salida.\n"
    "- Presioná **"Procesar y consolidar"** para generar el dataset consolidado."
)

if run_btn:
    if not uploaded_files:
        st.warning("Subí al menos un archivo Excel en la barra lateral.")
        st.stop()

    # 1) Guardar los archivos subidos en data/raw
    raw_dir = Path(RAW_DIR)
    raw_dir.mkdir(parents=True, exist_ok=True)

    for uf in uploaded_files:
        dest = raw_dir / uf.name
        with open(dest, "wb") as f:
            f.write(uf.getbuffer())

    # 2) Preparar columnas custom (si aplica)
    custom_cols = (
        [c.strip() for c in custom_cols_str.split(",") if c.strip()]
        if schema_name == "custom"
        else None
    )

    st.info("🔄 Procesando archivos, consolidando y aplicando esquema de columnas...")
    # 3) Consolidar todo usando tu pipeline de datos
    df_out = process_all(
        raw_dir=raw_dir,
        schemas_config=Path(SCHEMAS_CONFIG),
        schema_name=schema_name,
        custom_columns=custom_cols,
    )

    st.success(f"✅ Datos procesados: {len(df_out):,} filas, {df_out['IdArticulo'].nunique():,} SKUs.")

    # 4) GUARDAR PARQUET CENTRAL EN data/processed/ventas_procesadas.parquet
    processed_dir = Path(PROCESSED_DIR)
    processed_dir.mkdir(parents=True, exist_ok=True)

    parquet_path = processed_dir / "ventas_procesadas.parquet"
    df_out.to_parquet(parquet_path, index=False)

    # 5) Mostrar preview en pantalla
    st.subheader("2️⃣ Vista previa de datos consolidados")
    st.dataframe(df_out.head(50), use_container_width=True)

    # 6) Descargar Excel con el resultado
    st.subheader("3️⃣ Descargar Excel de salida")

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df_out.to_excel(writer, index=False, sheet_name="Consolidado")
    buffer.seek(0)

    st.download_button(
        label="⬇️ Descargar Excel consolidado",
        data=buffer,
        file_name="ventas_consolidadas.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

else:
    st.info(
        "👉 Subí archivos y configurá opciones en la barra lateral, "
        "luego presioná **"Procesar y consolidar"** para comenzar."
    )

st.markdown("---")
st.caption(
    "El archivo consolidado se usa en las demás páginas (ABC, Proyecciones, Comparativos, Reportes)."
)
