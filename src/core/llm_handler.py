from utils.config import get_required_env
import os
from groq import Groq

class LLMHandler:
    """Maneja la integración con el LLM para analizar código C++."""
    
    def __init__(self, code: str):
        """Inicializa el handler con el código a analizar."""
        self.code = code
        self.system_prompt = self._get_system_prompt()

    def _call_api(self, user_prompt: str) -> str:
        """Realiza la llamada a la API de Groq con el system prompt y user prompt dados."""
        client = Groq(
            api_key=get_required_env("GROQ_API_KEY"),
        )
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            model=get_required_env("GROQ_API_MODEL"),
            temperature=0.1,
        )
        return chat_completion.choices[0].message.content

    def _get_system_prompt(self) -> str:
        """Devuelve el prompt del sistema usado para todas las solicitudes a la API."""
        return """Eres un experto analizador de algoritmos C++.
                    Requisitos del codigo obligatorios:
                    - Debe leer los datos de entrada y debe imprimir los resultados con el formato allí indicado. 
                    No debe agregar mensajes ni agregar o eliminar datos en el proceso de lectura.
                    - No se quede en un ciclo infinito.
                    - El criterio de evaluación será la complejidad computacional de la solución.
                    Es necesario incluir en la cabecera del archivo comentarios que expliquen la complejidad de la solución del problema para cada caso.
                    - En adición a lo anterior, para efectos de la calificación se tendrán en cuenta aspectos de estilo como no usar
                    break ni continue y que las funciones deben tener únicamente una instrucción return que debe estar en la
                    última línea.
                    Tu rol es analizar código C++ y proporcionar segun lo solicitado por el usuario:
                    - Análisis de complejidad temporal (notación Big O) / Análisis de complejidad espacial
                    - Errores potenciales y advertencias
                    - Sugerencias de optimización
                    Información adicional que recibirás:
                    - Número de loops encontrados
                    - Loops anidados
                    - Si la función es recursiva
                    - Estructura del código
                    Instrucciones:
                    - Verificar cumplimiento de los requisitos obligatorios del codigo
                    - Sé conciso y técnico
                    - Usa notación Big O
                    - Explica el POR QUÉ de cada análisis
                    - Si no detectas algo, di "No detectado"
                    - Nunca hagas suposiciones sin evidencia
                    Tono: Profesional, educativo, directo.

                    """

    def _build_complexity_prompt(self, code: str, indicators: dict) -> str:
        """Construye el prompt del usuario para análisis de complejidad."""
        return f"""
        Analiza la complejidad de este código C++:

Estructura detectada:
{indicators}
Código:
{code}

Proporciona:
1. Complejidad temporal (peor, mejor, promedio caso)
2. Complejidad espacial
3. Explicación clara
"""

    def _build_optimized_prompt(self, code: str, indicators: dict) -> str:
        """Construye el prompt del usuario para sugerencias de optimización."""
        return f"""
        Sugiere optimizaciones para este código C++:

Estructura detectada:
{indicators}

Código:
{code}
Proporciona:
1. 3 formas de optimizar (si es posible)
2. Complejidad resultante
3. Trade-offs (qué ganas/pierdes)
4. Dificultad de implementación
"""

    def _build_errors_prompt(self, code: str, indicators: dict) -> str:
        """Construye el prompt del usuario para búsqueda de errores potenciales."""
        return f"""
Identifica errores y problemas en este código C++:

Estructura detectada:
{indicators}
Código:
{code}

Busca:
1. Errores de lógica
2. Memory leaks potenciales
3. Acceso a arrays fuera de límites
4. Variables no inicializadas
5. Malas prácticas de C++

Sé específico: menciona línea si es posible.
        """

    def analyze_complexity(self, indicators: dict) -> str:
        """Analiza la complejidad temporal y espacial del código."""
        user_prompt = self._build_complexity_prompt(self.code, indicators)
        return self._call_api(user_prompt)

    def analyze_optimization(self, indicators: dict) -> str:
        """Sugiere optimizaciones para el código dado."""
        user_prompt = self._build_optimized_prompt(self.code, indicators)
        return self._call_api(user_prompt)

    def analyze_errors(self, indicators: dict) -> str:
        """Busca y reporta posibles errores lógicos o malas prácticas."""
        user_prompt = self._build_errors_prompt(self.code, indicators)
        return self._call_api(user_prompt)
