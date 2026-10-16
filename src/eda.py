"""Funciones puras para exploración, segmentación y correlaciones."""
from __future__ import annotations
import pandas as pd


def numeric_columns(df: pd.DataFrame) -> list[str]:
    return df.select_dtypes(include="number").columns.tolist()


def profile(df: pd.DataFrame) -> dict:
    missing = int(df.isna().sum().sum())
    return {
        "filas": int(df.shape[0]),
        "columnas": int(df.shape[1]),
        "faltantes": missing,
        "porcentaje_faltantes": round(100 * missing / df.size, 2) if df.size else 0,
        "duplicados": int(df.duplicated().sum()),
        "numericas": len(numeric_columns(df)),
    }


def null_summary(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        "columna": df.columns,
        "nulos": df.isna().sum().values,
        "porcentaje": (df.isna().mean().values * 100).round(2),
    }).sort_values("nulos", ascending=False, kind="stable").reset_index(drop=True)


def grouped_summary(df: pd.DataFrame, group: str, feature: str) -> pd.DataFrame:
    if group not in df or feature not in numeric_columns(df):
        raise ValueError("Variable de agrupación o variable numérica no válida.")
    return (
        df.groupby(group, dropna=False)[feature]
        .agg(conteo="count", promedio="mean", mediana="median", desviacion="std")
        .round(3)
        .reset_index()
    )


def correlation_pairs(df: pd.DataFrame, limit: int = 5) -> pd.DataFrame:
    features = [c for c in numeric_columns(df) if c != "cultivar" and df[c].nunique(dropna=True) > 1]
    if len(features) < 2:
        return pd.DataFrame(columns=["variable_a", "variable_b", "correlacion"])
    corr = df[features].corr(numeric_only=True)
    pairs=[]
    for i, a in enumerate(features):
        for b in features[i+1:]:
            v=corr.loc[a,b]
            if pd.notna(v):
                pairs.append({"variable_a":a,"variable_b":b,"correlacion":float(v)})
    return pd.DataFrame(pairs).reindex(columns=["variable_a","variable_b","correlacion"]).sort_values(
        "correlacion",key=lambda s:s.abs(),ascending=False
    ).head(limit).reset_index(drop=True)
