"""Módulo para gestionar la carga de variables de entorno y configuración general."""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / ".env"
# Carga variables desde el .env en la raíz del repositorio.
load_dotenv(dotenv_path=ENV_PATH)


def get_required_env(name: str) -> str:
    """Devuelve la variable de entorno o lanza error si falta."""
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"La variable de entorno '{name}' no está configurada. "
            f"Revisa el archivo {ENV_PATH}."
        )
    return value