import ast
import re
import tokenize
from typing import Generator, Tuple

# Define your error code and message
ERROR_CODE = "NE001"
ERROR_MSG = "NE001 Non-English  characters detected: {}"

# Regex pattern to detect Cyrillic characters (Unicode range U+0400 to U+04FF)
CYRILLIC_PATTERN = re.compile(r"[\u0400-\u04FF]+")


class Plugin:
    name = "flake8_noneng"
    version = "0.1.0"

    def __init__(self, tree, filename):
        self.tree = tree
        self.filename = filename

    def run(self) -> Generator[Tuple[int, int, str, type], None, None]:
        # 1. Check string literals and docstrings in AST nodes
        for node in ast.walk(self.tree):
            # Check string literals (e.g., assigned strings)
            if isinstance(node, ast.Str):  # Python <3.8
                value = node.s
                lineno = node.lineno
                col_offset = node.col_offset
            elif hasattr(ast, "Constant") and isinstance(node, ast.Constant) and isinstance(node.value, str):  # Python 3.8+
                value = node.value
                lineno = node.lineno
                col_offset = node.col_offset
            else:
                # Check for docstrings attached to modules, classes, functions
                if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    docstring = ast.get_docstring(node)
                    if docstring:
                        if node.body and isinstance(node.body[0], ast.Expr):
                            doc_node = node.body[0]
                            lineno = getattr(doc_node, 'lineno', 1)
                            col_offset = getattr(doc_node, 'col_offset', 0)
                        else:
                            lineno = 1
                            col_offset = 0
                        value = docstring
                    else:
                        continue
                else:
                    continue

            # Search for Cyrillic characters in the string
            matches = CYRILLIC_PATTERN.findall(value)
            if matches:
                # Flatten and deduplicate matches
                chars = set("".join(matches))
                yield (
                    lineno,
                    col_offset,
                    ERROR_MSG.format("".join(sorted(chars))),
                    type(self),
                )

        # 2. Check comments using tokenize
        try:
            with open(self.filename, 'rb') as f:
                tokens = tokenize.tokenize(f.readline)
                for token in tokens:
                    if token.type == tokenize.COMMENT:
                        comment_text = token.string
                        matches = CYRILLIC_PATTERN.findall(comment_text)
                        if matches:
                            chars = set("".join(matches))
                            yield (
                                token.start[0],  # line number
                                token.start[1],  # column offset
                                ERROR_MSG.format("".join(sorted(chars))),
                                type(self),
                            )
        except Exception:
            # Silently skip comment checks if file can't be opened/tokenized
            pass
