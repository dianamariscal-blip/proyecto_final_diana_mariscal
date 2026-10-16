# Arquitectura del proyecto

```text
Interfaz de Streamlit (app.py)
       ├─ data_loader.py     → CSV incluido / CSV cargado
       ├─ eda.py             → perfil, nulos, segmentos y correlaciones
       ├─ visualizations.py  → gráficos Plotly
       ├─ modeling.py        → partición, entrenamiento y evaluación
       └─ agent.py           → selección determinística de herramientas
              └─ llm_client.py → Ollama /api/chat (localhost)
```

Paradigmas: imperativo (control y validaciones), funcional (funciones puras de exploración), orientado a objetos (`AgenteDatos`, `OllamaClient`) y declarativo (UI y gráficos). El LLM recibe resúmenes calculados por Python y no ejecuta código arbitrario. Sin dependencia de servicios remotos.
