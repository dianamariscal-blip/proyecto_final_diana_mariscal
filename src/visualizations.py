"""Visualizaciones Plotly; los cálculos residen en eda.py."""
from __future__ import annotations
import pandas as pd
import plotly.express as px


def histogram(df: pd.DataFrame, feature: str):
    return px.histogram(df, x=feature, nbins=22, marginal="box", title=f"Distribución de {feature}", template="plotly_white")


def grouped_box(df: pd.DataFrame, feature: str, group: str):
    tmp=df.copy()
    tmp[group]=tmp[group].astype("string").fillna("Sin dato")
    return px.box(tmp, x=group, y=feature, color=group, points="outliers", title=f"{feature} por {group}", template="plotly_white")


def correlation_heatmap(df: pd.DataFrame, columns: list[str]):
    corr=df[columns].corr(numeric_only=True).round(2)
    return px.imshow(corr,text_auto=True,aspect="auto", zmin=-1,zmax=1,color_continuous_scale="RdBu_r", title="Matriz de correlación (Pearson)")


def feature_importances(frame: pd.DataFrame):
    return px.bar(frame.sort_values("importancia"),x="importancia",y="variable",orientation="h",title="Importancia de variables (bosque aleatorio)",template="plotly_white")
