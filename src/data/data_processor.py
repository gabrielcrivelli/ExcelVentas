"""
DataProcessor - consolida, calcula métricas básicas y permite elegir columnas de salida.
"""

from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
import yaml

from src.data.data_loader import load_all_excels
from src.data.data_cleaner import clean_and_enrich

DEFAULT_SCHEMAS: Dict[str, List[str]] = {
    "detalle": [
        "Sucursal", "FechaComprobante", "Año", "Mes", "Día",
        "IdArticulo", "Marca", "Descripcion",
        "Departamento", "Familia", "SubFamilia",
        "Cantidad", "PrecioUnitario", "ImporteTotal",
    ],
    "ejecutivo": [
        "Sucursal", "Año", "Mes",
        "Departamento", "Familia",
        "IdArticulo", "Descripcion", "Marca",
        "Cantidad", "ImporteTotal",
        "Venta_Diaria_Prom",
        "Stock_15_Dias", "Stock_30_Dias", "Stock_60_Dias",
    ],
    "stock_planning": [
        "Sucursal", "IdArticulo", "Descripcion", "Marca",
        "Departamento", "Familia",
        "Venta_Diaria_Prom",
        "Stock_15_Dias", "Stock_30_Dias", "Stock_60_Dias",
    ],
}


def load_schemas(config_path: Path) -> Dict[str, List[str]]:
    if not config_path.exists():
        return DEFAULT_SCHEMAS
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    schemas = cfg.get("schemas", {})
    merged = DEFAULT_SCHEMAS.copy()
    for name, body in schemas.items():
        merged[name] = body.get("columns", [])
    return merged


def add_velocity_and_stock(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if df["FechaComprobante"].notna().any():
        dias = (df["FechaComprobante"].max() - df["FechaComprobante"].min()).days + 1
    else:
        dias = 1
    dias = max(dias, 1)

    ventas = (
        df.groupby(["Sucursal", "IdArticulo"], as_index=False)["Cantidad"]
        .sum()
        .rename(columns={"Cantidad": "Cantidad_Total"})
    )
    ventas["Venta_Diaria_Prom"] = ventas["Cantidad_Total"] / dias

    df = df.merge(
        ventas[["Sucursal", "IdArticulo", "Venta_Diaria_Prom"]],
        on=["Sucursal", "IdArticulo"],
        how="left",
    )

    df["Stock_15_Dias"] = (df["Venta_Diaria_Prom"] * 15).round(0)
    df["Stock_30_Dias"] = (df["Venta_Diaria_Prom"] * 30).round(0)
    df["Stock_60_Dias"] = (df["Venta_Diaria_Prom"] * 60).round(0)

    return df


def apply_schema(
    df: pd.DataFrame,
    schema_name: str,
    schemas: Dict[str, List[str]],
    custom_columns: Optional[List[str]] = None,
) -> pd.DataFrame:
    if schema_name == "custom":
        if not custom_columns:
            raise ValueError("Para 'custom' se deben pasar columnas personalizadas.")
        cols = custom_columns
    else:
        cols = schemas.get(schema_name, [])
    cols_valid = [c for c in cols if c in df.columns]
    if not cols_valid:
        raise ValueError("Ninguna columna del esquema existe en el DataFrame.")
    return df[cols_valid]


def process_all(
    raw_dir: Path,
    schemas_config: Path,
    schema_name: str,
    custom_columns: Optional[List[str]] = None,
) -> pd.DataFrame:
    df = load_all_excels(raw_dir)
    df = clean_and_enrich(df)
    df = add_velocity_and_stock(df)
    schemas = load_schemas(schemas_config)
    return apply_schema(df, schema_name, schemas, custom_columns)
