"""
DataLoader - lectura de Excels mensuales desde data/raw.
"""

from pathlib import Path
from typing import List
import pandas as pd


REQUIRED_COLS = [
    "FechaComprobante", "IdArticulo", "Marca", "Descripcion",
    "Departamento", "Familia", "SubFamilia",
    "Cantidad", "PrecioUnitario", "ImporteTotal",
]


def infer_sucursal_from_filename(path: Path) -> str:
    name = path.name.upper()
    if "HIPER" in name:
        return "HIPER"
    if "CORRIENTES" in name:
        return "CORRIENTES"
    return "DESCONOCIDA"


def load_all_excels(raw_dir: Path) -> pd.DataFrame:
    files: List[Path] = sorted(raw_dir.glob("*.xlsx"))
    if not files:
        raise FileNotFoundError(f"No se encontraron .xlsx en {raw_dir}")

    dfs = []
    for fp in files:
        sucursal = infer_sucursal_from_filename(fp)
        df = pd.read_excel(fp)
        missing = set(REQUIRED_COLS) - set(df.columns)
        if missing:
            raise ValueError(f"{fp.name} carece de columnas: {missing}")
        df["Sucursal"] = sucursal
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)
