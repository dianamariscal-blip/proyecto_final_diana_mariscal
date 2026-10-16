"""Carga segura de CSV y de la muestra Wine-UCI."""
from __future__ import annotations
from io import BytesIO
from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "vinos_uci.csv"
MAX_BYTES = 15 * 1024 * 1024


def load_builtin() -> pd.DataFrame:
    """Retorna una copia del dataset público de referencia."""
    return pd.read_csv(DATA_PATH)


def load_uploaded(contents: bytes) -> pd.DataFrame:
    """Lee CSV delimitado por comas o punto y coma, con un límite explícito."""
    if not contents:
        raise ValueError("El archivo CSV está vacío.")
    if len(contents) > MAX_BYTES:
        raise ValueError("El archivo supera el límite de 15 MB.")
    try:
        frame = pd.read_csv(BytesIO(contents), sep=None, engine="python", encoding="utf-8-sig")
    except (UnicodeError, pd.errors.ParserError) as exc:
        raise ValueError("No se pudo leer el CSV. Usa UTF-8 y delimitadores estándar.") from exc
    if frame.empty or len(frame.columns) < 2:
        raise ValueError("El CSV debe contener al menos una fila y dos columnas.")
    frame.columns = [str(c).strip() for c in frame.columns]
    if frame.columns.duplicated().any():
        raise ValueError("El CSV tiene encabezados duplicados.")
    return frame
