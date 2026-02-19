def classify_error(log):
    # Order matters: check for syntax/indentation first
    if re.search(r"IndentationError", log, re.I):
        return "INDENTATION"
    if re.search(r"SyntaxError|Parse error", log, re.I):
        return "SYNTAX"
    if re.search(r"ImportError|ModuleNotFoundError|Cannot find module", log, re.I):
        return "IMPORT"
    if re.search(r"TypeError", log, re.I):
        return "TYPE_ERROR"
    if re.search(r"unused import|trailing whitespace|flake8", log, re.I):
        return "LINTING"
    
    # If the code runs but the test fails (e.g., AssertionError)
    return "LOGIC"