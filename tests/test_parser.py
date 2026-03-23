"""Pruebas de CPPAnalyzer con ejemplos .cpp y casos límite."""

from pathlib import Path

from core.parser import CPPAnalyzer

EXAMPLES = Path(__file__).resolve().parent.parent / "example_codes"


def read_example(name: str) -> str:
    return (EXAMPLES / name).read_text(encoding="utf-8")


class TestCPPAnalyzerExamples:
    def test_bubble_sort_has_nested_loops(self):
        code = read_example("bubbleSort.cpp")
        analyzer = CPPAnalyzer(code)
        assert len(analyzer.get_loops()) == 2
        assert len(analyzer.get_nested_loops()) >= 1
        assert len(analyzer.get_functions()) == 1

    def test_fibonacci_recursive(self):
        code = read_example("Fibonacci.cpp")
        analyzer = CPPAnalyzer(code)
        funcs = analyzer.get_functions()
        assert len(funcs) == 2
        recursive = [f for f in funcs if analyzer.check_recursion(f)]
        assert len(recursive) == 1

    def test_hello_world_no_loops(self):
        code = read_example("hello_world.cpp")
        analyzer = CPPAnalyzer(code)
        assert analyzer.get_loops() == []
        assert analyzer.get_nested_loops() == []
        assert len(analyzer.get_functions()) == 1


class TestCPPAnalyzerEdgeCases:
    def test_empty_source(self):
        analyzer = CPPAnalyzer("")
        assert analyzer.get_loops() == []
        assert analyzer.get_functions() == []
        assert analyzer.get_nested_loops() == []
        data = analyzer.get_complexity_indicators()
        assert data["total_lines"] == 0

    def test_whitespace_only(self):
        analyzer = CPPAnalyzer("   \n\t\n  ")
        assert analyzer.get_loops() == []
        assert analyzer.get_functions() == []

    def test_no_functions_only_comment(self):
        code = "// solo un comentario\n"
        analyzer = CPPAnalyzer(code)
        assert analyzer.get_functions() == []

    def test_complexity_indicators_shape(self):
        analyzer = CPPAnalyzer(read_example("bubbleSort.cpp"))
        data = analyzer.get_complexity_indicators()
        assert set(data.keys()) == {
            "loops",
            "functions",
            "nested_loops",
            "total_lines",
        }
        assert data["total_lines"] > 0
