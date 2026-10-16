"""Cliente HTTP sencillo para Ollama local, con errores explícitos."""
from __future__ import annotations
import requests

DEFAULT_BASE = "http://127.0.0.1:11434"

class OllamaError(RuntimeError):
    """Error de conexión, modelo o formato de respuesta de Ollama."""


class OllamaClient:
    def __init__(self, model:str="llama3.2:3b", base_url:str=DEFAULT_BASE):
        self.model=model
        self.base_url=base_url.rstrip("/")

    def available_models(self)->list[str]:
        try:
            resp=requests.get(f"{self.base_url}/api/tags",timeout=4)
            resp.raise_for_status()
            return [item.get("name","") for item in resp.json().get("models",[])]
        except (requests.RequestException,ValueError) as exc:
            raise OllamaError("No se pudo conectar con Ollama. Abre Ollama e intenta nuevamente.") from exc

    def generate(self,system:str,user:str)->str:
        payload={
            "model":self.model,
            "messages":[{"role":"system","content":system},{"role":"user","content":user}],
            "stream":False,
            "options":{"temperature":0.1,"num_predict":320},
        }
        try:
            resp=requests.post(f"{self.base_url}/api/chat",json=payload,timeout=(5,150))
            if resp.status_code==404:
                raise OllamaError(f"Modelo '{self.model}' no disponible. Ejecuta: ollama pull {self.model}")
            resp.raise_for_status()
            content=resp.json()["message"]["content"].strip()
            if not content:
                raise OllamaError("Ollama devolvió una respuesta vacía.")
            return content
        except (requests.RequestException,ValueError,KeyError,TypeError) as exc:
            raise OllamaError("No hubo respuesta válida de Ollama. Confirma que esté iniciado y que el modelo esté descargado.") from exc
