"""Pruebas de LLMHandler: prompts y analizadores sin llamar a la API de Groq."""

from pathlib import Path

import pytest

from core.llm_handler import LLMHandler

EXAMPLES = Path(__file__).resolve().parent.parent / "example_codes"
EXAMPLE_CPP_FILES = ("bubbleSort.cpp", "Fibonacci.cpp", "hello_world.cpp")


def read_example(name: str) -> str:
    return (EXAMPLES / name).read_text(encoding="utf-8")


class TestLLMHandlerInit:
    """Pruebas de inicialización de LLMHandler."""

    @pytest.mark.parametrize("filename", EXAMPLE_CPP_FILES)
    def test_stores_code_and_builds_system_prompt(self, filename):
        """Verifica que el código se almacena y el prompt base se construye correctamente."""
        code = read_example(filename)
        handler = LLMHandler(code)
        assert handler.code == code
        assert len(handler.system_prompt) > 0
        assert "Big O" in handler.system_prompt


class TestLLMHandlerBuildPrompts:
    """Pruebas para la construcción de los distintos prompts de usuario."""

    @pytest.mark.parametrize("filename", EXAMPLE_CPP_FILES)
    def test_build_complexity_prompt_contains_code_and_indicators(self, filename):
        """Verifica que el prompt de complejidad incluya el código y los indicadores."""
        code = read_example(filename)
        handler = LLMHandler(code)
        indicators = {"loops": 0, "nested": False}
        text = handler._build_complexity_prompt(code, indicators)
        assert code in text
        assert str(indicators) in text or "loops" in text.lower()

    @pytest.mark.parametrize("filename", EXAMPLE_CPP_FILES)
    def test_build_optimized_prompt_contains_code(self, filename):
        """Verifica que el prompt de optimización incluya código y pida optimizaciones."""
        code = read_example(filename)
        handler = LLMHandler(code)
        text = handler._build_optimized_prompt(code, {"loops": 1})
        assert code in text
        assert "optimiz" in text.lower()

    @pytest.mark.parametrize("filename", EXAMPLE_CPP_FILES)
    def test_build_errors_prompt_mentions_risks(self, filename):
        """Verifica que el prompt de errores incluya código y pida buscar errores."""
        code = read_example(filename)
        handler = LLMHandler(code)
        text = handler._build_errors_prompt(code, {})
        assert "error" in text.lower() or "problema" in text.lower()
        assert code in text


class TestLLMHandlerAnalyzeWithMock:
    """Evita red: sustituye _call_api."""

    @pytest.fixture
    def mock_response(self):
        return "respuesta simulada del modelo"

    @pytest.mark.parametrize("filename", EXAMPLE_CPP_FILES)
    def test_analyze_complexity_uses_call_api(
        self, filename, mock_response, monkeypatch
    ):
        """Asegura que analyze_complexity llame a _call_api correctamente."""
        code = read_example(filename)
        handler = LLMHandler(code)
        captured = []

        def fake_call(self, user_prompt):
            captured.append(user_prompt)
            return mock_response

        monkeypatch.setattr(LLMHandler, "_call_api", fake_call)
        indicators = {"loops": [], "total_lines": len(code.splitlines())}
        out = handler.analyze_complexity(indicators)
        assert out == mock_response
        assert len(captured) == 1
        assert "complejidad" in captured[0].lower()

    @pytest.mark.parametrize("filename", EXAMPLE_CPP_FILES)
    def test_analyze_optimization_uses_call_api(
        self, filename, mock_response, monkeypatch
    ):
        """Asegura que analyze_optimization llame a _call_api."""
        code = read_example(filename)
        handler = LLMHandler(code)

        def fake_call(self, user_prompt):
            return mock_response

        monkeypatch.setattr(LLMHandler, "_call_api", fake_call)
        out = handler.analyze_optimization({"nested_loops": 0})
        assert out == mock_response

    @pytest.mark.parametrize("filename", EXAMPLE_CPP_FILES)
    def test_analyze_errors_uses_call_api(self, filename, mock_response, monkeypatch):
        """Asegura que analyze_errors llame a _call_api."""
        code = read_example(filename)
        handler = LLMHandler(code)

        def fake_call(self, user_prompt):
            return mock_response

        monkeypatch.setattr(LLMHandler, "_call_api", fake_call)
        out = handler.analyze_errors({})
        assert out == mock_response


class TestLLMHandlerEdgeCases:
    """Pruebas de casos extremos para LLMHandler."""

    def test_empty_code_string(self):
        """Verifica que el handler tolere strings de código vacíos."""
        h = LLMHandler("")
        assert h.code == ""
        text = h._build_complexity_prompt("", {})
        assert "Código:" in text or "código" in text.lower()
