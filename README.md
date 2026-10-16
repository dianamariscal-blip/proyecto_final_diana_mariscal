# Laboratorio de análisis enológico — Proyecto Final Integrador

Aplicación Streamlit que analiza **UCI Wine** (178 observaciones, 13 variables químicas numéricas y etiqueta de tres cultivares), compara segmentos, visualiza correlaciones, evalúa un clasificador Random Forest y consulta un agente con **Ollama local**.

> **Alcance del dato:** las etiquetas 0, 1, 2 identifican cultivares. Este dataset **no** proporciona mediciones de calidad sensorial, precio o riesgo de salud. Una correlación no establece causalidad.

## Fuente y uso

- UCI Machine Learning Repository, *Wine* (CC BY 4.0): https://archive.ics.uci.edu/dataset/109/wine
- Copia incluida en `data/vinos_uci.csv`, generada a partir de `sklearn.datasets.load_wine`.
- También se permite subir un CSV UTF-8 de hasta 15 MB con al menos dos columnas. La clasificación se activa solo si se cumplen sus condiciones.

## Requisitos previos

- Windows 10/11, macOS o Linux.
- Python 3.11 o 3.12 recomendado y Git opcional.
- Ollama instalado en el mismo equipo; para el agente se recomienda `llama3.2:3b` o `llama3.2:1b` si hay pocos recursos.
- Acceso a Internet solo para **instalar** paquetes y descargar el modelo. El uso posterior con Ollama es local.

## Instalación en Windows (PowerShell)

```powershell
cd Proyecto_Final_Analisis_Vinos_IA
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Si `py -3.11` no está disponible, usa `py -m venv .venv` o `python -m venv .venv` con Python 3.11/3.12. Si PowerShell bloquea la activación, abre CMD y ejecuta `.venv\Scripts\activate.bat`.

## Instalación en macOS / Linux

```bash
cd Proyecto_Final_Analisis_Vinos_IA
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Instalar y ejecutar Ollama

1. Descarga Ollama desde https://ollama.com/download e instálalo en tu computador.
2. En otra terminal ejecuta:

```bash
ollama pull llama3.2:3b
ollama list
```

Si el equipo tiene recursos limitados:

```bash
ollama pull llama3.2:1b
```

En Windows o macOS la aplicación Ollama suele ejecutar el servidor automáticamente. Si no está activo, ejecuta `ollama serve` en una terminal adicional. No ejecutes dos servidores Ollama simultáneamente.

## Ejecutar la aplicación

Con el entorno virtual activo:

```bash
python -m streamlit run app.py
```

Abre la dirección local que muestra la terminal (normalmente `http://localhost:8501`). Elige **Wine (UCI) incluido**, revisa Datos y calidad, Exploración, Clasificación y finalmente Agente local.

**Consultas sugeridas al agente:**
- «¿Cuáles son las correlaciones más fuertes?»
- «Compara el promedio de alcohol entre cultivares» (selecciona `cultivar` y `alcohol` antes).
- «¿Cuántos registros, columnas y valores faltantes hay?»

En cada respuesta abre «Ver cálculos usados por el agente» para comprobar el contexto objetivo.

## Estructura

```text
Proyecto_Final_Analisis_Vinos_IA/
├── app.py                     # Streamlit, navegación
├── src/
│   ├── data_loader.py         # Datos y CSV
│   ├── eda.py                 # Funciones analíticas
│   ├── visualizations.py      # Plotly
│   ├── modeling.py            # Random Forest, métricas
│   ├── llm_client.py          # Cliente de Ollama
│   └── agent.py               # Agente y herramientas
├── data/vinos_uci.csv         # Dataset incluido, UCI Wine
├── tests/test_core.py         # Pruebas automatizadas
├── assets/                    # Evidencias reales del estudiante
├── requirements.txt
├── .gitignore
├── ARCHITECTURE.md
└── GUIA_PUBLICACION.md
```

## Pruebas

```bash
python -m pytest -q
```

Las pruebas comprueban perfilado, segmentación, correlaciones, modelo y selección de herramientas del agente, sin exigir Ollama. La salida de un LLM real **solo puede verificarse** en la computadora del estudiante con Ollama instalado.

## Limitaciones y buenas prácticas

- Dataset de tamaño pequeño; exactitud en un solo holdout no garantiza desempeño general.
- La explicación del agente es texto generado: coteja cada afirmación con el contexto JSON.
- El CSV subido solo se usa dentro de la sesión de Streamlit; no hay almacenamiento remoto ni servicio externo de IA.
- No se incluyen pesos ni modelos de Ollama en el repositorio.
- El entrenamiento se calcula al pulsar el botón; si cambia el dataset o la variable objetivo, vuelve a entrenar.
- Ollama normalmente responde en `http://127.0.0.1:11434`; debe estar accesible desde el mismo equipo.
- **No** publiques contraseñas, datos privados o capturas con información sensible en GitHub o YouTube.

## Autores y entrega

Diana Mariscal y URLs de GitHub/YouTube en el informe, Anexos B y C. Ver `GUIA_PUBLICACION.md` para un procedimiento paso a paso.
