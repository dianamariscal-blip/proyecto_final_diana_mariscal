"""Evaluación reproducible de clasificación; sin fuga de información."""
from __future__ import annotations
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, balanced_accuracy_score, classification_report, confusion_matrix


def train_classifier(df:pd.DataFrame, target:str, seed:int=42)->dict:
    if target not in df:
        raise ValueError("No existe la variable objetivo.")
    features=df.select_dtypes(include="number").drop(columns=[target],errors="ignore")
    features=features.loc[:,features.notna().any()]
    labels=df[target]
    keep=labels.notna()
    features,labels=features.loc[keep],labels.loc[keep].astype(str)
    counts=labels.value_counts()
    if features.shape[1] < 1 or len(counts) not in range(2,11) or counts.min()<4 or len(labels)<30:
        raise ValueError("Clasificación disponible con 2-10 clases, mínimo 4 registros por clase y 30 filas, más una columna numérica.")
    x_train,x_test,y_train,y_test=train_test_split(features,labels,test_size=0.25,random_state=seed,stratify=labels)
    model=Pipeline([
        ("imputer",SimpleImputer(strategy="median")),
        ("forest",RandomForestClassifier(n_estimators=160,random_state=seed,n_jobs=1))
    ])
    model.fit(x_train,y_train)
    predictions=model.predict(x_test)
    classes=sorted(labels.unique().tolist())
    return {
        "accuracy":float(accuracy_score(y_test,predictions)),
        "balanced_accuracy":float(balanced_accuracy_score(y_test,predictions)),
        "train_size":int(len(y_train)),"test_size":int(len(y_test)),
        "classes":classes,
        "matrix":confusion_matrix(y_test,predictions,labels=classes),
        "report":classification_report(y_test,predictions,output_dict=True,zero_division=0),
        "importances":pd.DataFrame({"variable":features.columns,"importancia":model.named_steps["forest"].feature_importances_}).sort_values("importancia",ascending=False),
    }
