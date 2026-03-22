# algo-analyzer
Bot de discord y CLI para analizar tu codigo de C++ [En progreso...]

# Instalacion

## Clona el repositorio y accede a su carpeta
```bash
git clone https://github.com/julianandresdev/algo-analyzer.git
cd algo-analyzer
```

## Instala y configura el proyecto

### MacOS
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows
```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

En PowerShell, activa el entorno con `.\venv\Scripts\Activate.ps1` en lugar de `venv\Scripts\activate`.

Necesitas Python 3.9 o superior. Las dependencias principales estan en `requirements.txt`: tree-sitter (analisis sintactico), python-dotenv (variables de entorno), pytest (pruebas) y el resto de librerias transitivas.

Para correr las pruebas, con el entorno virtual activado:
```bash
pytest
```
# EN PROGRESO...

# Creditos
**Autor:** [Julian Andres](https://github.com/julianandresdev)\
**Licencia:** MIT 
