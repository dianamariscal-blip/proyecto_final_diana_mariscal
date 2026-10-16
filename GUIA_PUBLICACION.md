# Guía práctica: GitHub y video de YouTube

## A. Publicar en GitHub (método recomendado: Git en terminal)

1. Entra a https://github.com y crea tu cuenta si no tienes.
2. Clic en **New repository** (o + → New repository). Nombre sugerido: `proyecto-final-vinos-ia`.
3. Selecciona **Public** para facilitar la revisión. No marques «Add a README» ni «Add .gitignore»: ya vienen incluidos.
4. Instala Git desde https://git-scm.com/downloads si aún no lo tienes.
5. Abre una terminal **dentro de la carpeta del proyecto**, no en la carpeta superior ni con el .zip sin descomprimir.
6. Ejecuta lo siguiente (reemplaza TU_USUARIO):

```bash
git init
git add .
git commit -m "Proyecto final: Streamlit, análisis y Ollama"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/proyecto-final-vinos-ia.git
git push -u origin main
```

7. Si Git solicita configurar la identidad, antes del commit ejecuta `git config --global user.name "Tu nombre"` y `git config --global user.email "tu@email.com"`. Para autenticarte, GitHub solicita un acceso moderno (navegador, Git Credential Manager, CLI o token), no la contraseña tradicional.
8. Abre el enlace del repositorio en una ventana privada. Comprueba `app.py`, `src/`, `data/`, `requirements.txt` y `README.md`. Este será el enlace del **Anexo B**.
9. Para publicar correcciones: `git add .`, `git commit -m "Actualiza proyecto"` y `git push`.

**Alternativa sin terminal:** dentro del repositorio en GitHub elige **Add file → Upload files**, arrastra el contenido descomprimido y guarda los cambios. Revisa que la estructura de carpetas quede correcta; no subas `.venv`, `__pycache__` ni archivos secretos. Si el navegador no admite la carpeta completa, sube las subcarpetas según corresponda o usa Git.

## B. Grabar y subir el video a YouTube

1. Ejecuta `ollama list`, verifica el modelo y abre el proyecto usando `python -m streamlit run app.py`.
2. Graba pantalla y voz con OBS Studio, Zoom, Clipchamp o la herramienta de tu elección. Selecciona la ventana del navegador y, brevemente, la terminal para evidenciar Ollama.
3. Graba un máximo de **5 minutos**, mostrando: apertura del proyecto, datos, estadísticas de nulos, visualizaciones, entrenamiento y métricas, prueba de conexión con Ollama y consulta respondida con el contexto JSON verificable.
4. Revisa audio, legibilidad y evita mostrar correos, contraseñas, tokens o información privada.
5. Entra a https://studio.youtube.com, pulsa **Crear → Subir videos**, selecciona tu archivo y completa el título, por ejemplo: «Proyecto final integrador | Streamlit + Ollama + UCI Wine».
6. Durante la publicación elige visibilidad **No listado** (no «Privado») o «Público» y guarda/publica. El modo no listado permite verlo a quien tenga el enlace.
7. Copia la URL, ábrela en una ventana privada para comprobar que funciona y pégala en el **Anexo C**.

### Guion de demostración sugerido (4 min 40 s)

| Tiempo | Qué mostrar |
|---|---|
| 0:00–0:30 | Objetivo, dataset público y arquitectura modular |
| 0:30–1:10 | Lanzamiento local, indicadores, datos, nulos |
| 1:10–2:00 | Distribución, cajas por cultivar, correlaciones |
| 2:00–2:40 | Clasificador, métricas y variables importantes |
| 2:40–4:10 | `ollama list`, conexión, pregunta al agente y JSON de respaldo |
| 4:10–4:40 | Conclusión, limitaciones y mención del repositorio |

Nota: los límites y contenidos se basan en la guía de la asignatura; no se requiere transmitir en vivo ni realizar un despliegue cloud.
