import parso
from langchain_core.tools import tool

@tool
def check_python_syntax(code: str) -> str:
    """
    Check Python code syntax without executing it.
    Use this when the user provides Python code and you need to detect syntax errors.
    """
    grammar = parso.load_grammar()
    if not code.strip():
        return "No Code Provided"
    

    tree = grammar.parse(code)
    errors = grammar.iter_errors(tree)
    list_errors = list(errors)
    if not list_errors:
        return "Syntax check passed. No Python syntax errors found."
    else:
        errors_formatted = []
        for e in list_errors:
            line = e.start_pos[0]
            column = e.start_pos[1]
            error_message = e.message
            errors_formatted.append(f"SyntaxError at line {line}, column {column}: {error_message}")
        return "\n".join(errors_formatted)
        

developer_tools = [
    check_python_syntax,
]