import tree_sitter_cpp as tscpp
from tree_sitter import Language, Parser

CPP_LANGUAGE = Language(tscpp.language())
_parser = Parser(CPP_LANGUAGE)


class CPPAnalyzer:
    """Analiza código C++ con tree-sitter: bucles, funciones y llamadas."""

    def __init__(self, code: str) -> None:
        self.code = code
        self._bytes = code.encode("utf-8")
        self.tree = _parser.parse(self._bytes)
        self.root = self.tree.root_node

    def _get_loops(self, node):
        """Recorre el AST y acumula nodos `for_statement`."""
        result = []
        if node.type == "for_statement":
            result.append(node)
        for child in node.children:
            result.extend(self._get_loops(child))
        return result

    def _get_nested_loops(self, loops):
        """Pares (externo, interno) donde el interno está anidado en el externo."""
        result = []
        for outer in loops:
            for inner in loops:
                if outer is inner:
                    continue
                if outer.start_point[0] < inner.start_point[0] and outer.end_point[
                    0
                ] > inner.end_point[0]:
                    result.append((outer, inner))
        return result

    def _get_functions(self, node):
        """Recorre el AST y acumula nodos `function_definition`."""
        result = []
        if node.type == "function_definition":
            result.append(node)
        for child in node.children:
            result.extend(self._get_functions(child))
        return result

    def _get_calls(self, node):
        """Recorre el AST y acumula nodos `call_expression`."""
        result = []
        if node.type == "call_expression":
            result.append(node)
        for child in node.children:
            result.extend(self._get_calls(child))
        return result

    def _check_recursion(self, function):
        """True si el cuerpo de la función llama al mismo nombre que el declarador."""
        function_name = None
        calls = []
        for child in function.children:
            if child.type == "function_declarator":
                for sub in child.children:
                    if sub.type == "identifier":
                        function_name = self._bytes[
                            sub.start_byte : sub.end_byte
                        ].decode("utf-8")
            if child.type == "compound_statement":
                calls = self._get_calls(child)

        if function_name is None:
            return False

        for call in calls:
            for part in call.children:
                if part.type == "identifier":
                    call_name = self._bytes[
                        part.start_byte : part.end_byte
                    ].decode("utf-8")
                    if call_name == function_name:
                        return True
        return False

    def get_loops(self):
        """Devuelve la lista de nodos AST de todos los `for` encontrados."""
        return self._get_loops(self.root)

    def get_nested_loops(self):
        """Devuelve pares de bucles anidados a partir de `get_loops()`."""
        return self._get_nested_loops(self.get_loops())

    def check_recursion(self, function):
        """Indica si la función dada (nodo AST) es recursiva."""
        return self._check_recursion(function)

    def get_functions(self):
        """Devuelve la lista de nodos AST de todas las definiciones de función."""
        return self._get_functions(self.root)

    def get_complexity_indicators(self):
        """Resumen: bucles, funciones, bucles anidados y líneas del fuente."""
        loops = self.get_loops()
        functions = self.get_functions()
        nested_loops = self.get_nested_loops()
        return {
            "loops": loops,
            "functions": functions,
            "nested_loops": nested_loops,
            "total_lines": len(self.code.splitlines()),
        }
