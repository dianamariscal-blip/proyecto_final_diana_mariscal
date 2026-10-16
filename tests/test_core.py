"""Pruebas deterministas (sin Streamlit ni Ollama ejecutándose)."""
import pandas as pd
from src.data_loader import load_builtin,load_uploaded
from src.eda import profile,grouped_summary,correlation_pairs
from src.modeling import train_classifier
from src.agent import AgenteDatos

class FakeClient:
    def generate(self,system,user):
        assert "CONTEXTO_VERIFICADO_JSON" in user
        return "Interpretación simulada para prueba unitaria."


def test_builtin_profile():
    df=load_builtin()
    stats=profile(df)
    assert df.shape==(178,14)
    assert stats["faltantes"]==0
    assert df["cultivar"].value_counts().sort_index().tolist()==[59,71,48]


def test_upload_semicolon_and_limits():
    df=load_uploaded(b"a;b\n1;2\n3;4\n")
    assert df.shape==(2,2)


def test_group_and_correlations():
    df=load_builtin()
    groups=grouped_summary(df,"cultivar","alcohol")
    assert len(groups)==3
    pairs=correlation_pairs(df,5)
    assert len(pairs)==5
    assert all(pairs["correlacion"].abs()<=1)


def test_model_is_deterministic():
    df=load_builtin()
    a=train_classifier(df,"cultivar")
    b=train_classifier(df,"cultivar")
    assert a["accuracy"]==b["accuracy"]
    assert a["test_size"]==45
    assert a["accuracy"]>=0.8


def test_agent_tools_without_llm():
    df=load_builtin()
    agent=AgenteDatos(FakeClient())
    text,context=agent.responder(df,"Compara por cultivar el alcohol",grupo="cultivar",variable="alcohol")
    assert context["herramienta_ejecutada"]=="segmentos"
    assert "comparacion" in context
    _,c2=agent.responder(df,"¿Qué correlaciones observas?")
    assert c2["herramienta_ejecutada"]=="correlaciones"
