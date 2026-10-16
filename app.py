"""Laboratorio de perfiles químicos: interfaz principal de Streamlit."""
from __future__ import annotations
import streamlit as st
import pandas as pd
import hashlib
from src.data_loader import load_builtin,load_uploaded
from src.eda import profile,null_summary,numeric_columns,grouped_summary,correlation_pairs
from src.visualizations import histogram,grouped_box,correlation_heatmap,feature_importances
from src.modeling import train_classifier
from src.agent import AgenteDatos
from src.llm_client import OllamaClient,OllamaError

st.set_page_config(page_title="Laboratorio enológico | IA local",page_icon="🍇",layout="wide")
st.title("🍇 Laboratorio de análisis enológico")
st.caption("Datos reales de UCI Wine · análisis reproducible · interpretación local con Ollama")

with st.sidebar:
    st.header("Fuente de datos")
    source=st.radio("Elegir fuente",["Wine (UCI) incluido","Subir CSV propio"],index=0)
    upload=st.file_uploader("Subir archivo CSV (máx. 15 MB)",type=["csv"]) if source=="Subir CSV propio" else None
    st.divider()
    st.info("El dataset Wine identifica tres clases de cultivar mediante medidas químicas; NO evalúa calidad sensorial.")

try:
    if source=="Subir CSV propio":
        if upload is None:
            st.warning("Selecciona un archivo CSV para continuar.")
            st.stop()
        df=load_uploaded(upload.getvalue())
    else:
        df=load_builtin()
except (ValueError,FileNotFoundError,pd.errors.EmptyDataError) as exc:
    st.error(f"No fue posible cargar el dataset: {exc}")
    st.stop()

ncols=numeric_columns(df)
catcols=df.columns.tolist()
info=profile(df)
data_id=hashlib.sha256(df.to_csv(index=False).encode("utf-8")).hexdigest()
metrics=st.columns(4)
for col,(name,value) in zip(metrics,[
    ("Registros",info["filas"]),("Columnas",info["columnas"]),
    ("Nulos",info["faltantes"]),("Duplicados",info["duplicados"])
]):
    col.metric(name,value)

tab1,tab2,tab3,tab4=st.tabs(["📋 Datos y calidad","📊 Exploración","🌲 Clasificación","🤖 Agente local"])

with tab1:
    st.subheader("Muestra del dataset")
    st.dataframe(df.head(20),use_container_width=True)
    a,b=st.columns(2)
    with a:
        st.markdown("**Resumen de valores faltantes**")
        st.dataframe(null_summary(df),hide_index=True,use_container_width=True)
    with b:
        st.markdown("**Estadísticas numéricas**")
        if ncols:
            st.dataframe(df[ncols].describe().T.round(3),use_container_width=True)
        else:
            st.info("No se encontraron columnas numéricas.")
    st.download_button("Descargar datos activos",data=df.to_csv(index=False).encode("utf-8"),file_name="dataset_analizado.csv",mime="text/csv")

with tab2:
    if not ncols:
        st.warning("Este análisis requiere columnas numéricas.")
    else:
        var=st.selectbox("Variable para distribución",ncols,index=0)
        st.plotly_chart(histogram(df,var),use_container_width=True)
        group_default=catcols.index("cultivar") if "cultivar" in catcols else 0
        group=st.selectbox("Agrupar por",catcols,index=group_default)
        c1,c2=st.columns([1.2,1])
        with c1:st.plotly_chart(grouped_box(df,var,group),use_container_width=True)
        with c2:
            st.markdown("**Comparación por grupo**")
            st.dataframe(grouped_summary(df,group,var),use_container_width=True,hide_index=True)
        st.markdown("**Correlaciones más intensas (valor absoluto)**")
        corr=correlation_pairs(df,5)
        st.dataframe(corr.round(3),hide_index=True,use_container_width=True)
        heatcols=ncols[:13]
        if len(heatcols)>1:
            st.plotly_chart(correlation_heatmap(df,heatcols),use_container_width=True)
        st.caption("Una correlación no demuestra causalidad.")

with tab3:
    st.write("Clasificador supervisado con división estratificada 75/25, semilla 42 y bosque aleatorio.")
    target=st.selectbox("Variable objetivo",catcols,index=catcols.index("cultivar") if "cultivar" in catcols else 0)
    if st.button("Entrenar y evaluar",type="primary"):
        try:
            with st.spinner("Entrenando modelo..."):
                result=train_classifier(df,target)
            st.session_state["model_result"]=result
            st.session_state["model_target"]=target
            st.session_state["model_data_id"]=data_id
        except ValueError as exc:
            st.error(str(exc))
    if st.session_state.get("model_target")==target and st.session_state.get("model_data_id")==data_id and "model_result" in st.session_state:
        result=st.session_state["model_result"]
        a,b,c=st.columns(3)
        a.metric("Exactitud en test",f"{result['accuracy']:.1%}")
        b.metric("Exactitud balanceada",f"{result['balanced_accuracy']:.1%}")
        c.metric("Casos de prueba",result["test_size"])
        st.plotly_chart(feature_importances(result["importances"].head(10)),use_container_width=True)
        st.markdown("**Matriz de confusión (filas: clases reales; columnas: predicciones)**")
        st.dataframe(pd.DataFrame(result["matrix"],index=result["classes"],columns=result["classes"]),use_container_width=True)
        st.caption("Resultados del conjunto de prueba; no son una predicción de calidad de vino.")

with tab4:
    st.write("El agente ejecuta herramientas Python autorizadas y pide a Ollama interpretar únicamente los cálculos obtenidos.")
    model=st.selectbox("Modelo de Ollama",["llama3.2:3b","llama3.2:1b"],index=0)
    client=OllamaClient(model=model)
    if st.button("Verificar conexión con Ollama"):
        try:
            installed=client.available_models()
            if model in installed:
                st.success(f"Ollama disponible. Modelo {model} descargado.")
            else:
                st.warning(f"Ollama responde, pero falta {model}. Ejecuta en terminal: ollama pull {model}")
        except OllamaError as exc:
            st.error(str(exc))
    default_group="cultivar" if "cultivar" in df.columns else df.columns[0]
    grp=st.selectbox("Columna para comparar",catcols,index=catcols.index(default_group))
    col=st.selectbox("Medida numérica",ncols,index=ncols.index("alcohol") if "alcohol" in ncols else 0) if ncols else None
    question=st.text_area("Pregunta para el agente",value="¿Cuáles son las correlaciones más fuertes y qué implican?",max_chars=600,height=85)
    if st.button("Consultar al agente",type="primary"):
        agent=AgenteDatos(client)
        try:
            with st.spinner("Consultando modelo local..."):
                answer,ctx=agent.responder(df,question,grupo=grp,variable=col)
            st.subheader("Interpretación generada por el modelo")
            st.write(answer)
            with st.expander("Ver cálculos usados por el agente (contexto verificable)"):
                st.json(ctx)
        except (ValueError,OllamaError) as exc:
            st.error(str(exc))
    st.caption("No se necesita clave de API: Ollama se ejecuta en tu equipo, puerto 11434. Requiere instalar y descargar el modelo.")
