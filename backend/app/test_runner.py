import subprocess
import os
import sys

def discover_and_run_tests(repo_path):
    """
    Automatically detects project type and runs tests using the 'cwd' parameter.
    This is thread-safe and prevents the main process from losing its context.
    """
    repo_path = os.path.abspath(repo_path)
    
    # 1. Detection Logic (Using repo_path to check for files)
    if os.path.exists(os.path.join(repo_path, "package.json")):
        # Node.js project
        cmd = ["npm", "test"]
    elif os.path.exists(os.path.join(repo_path, "requirements.txt")) or \
         any(f.endswith(".py") for f in os.listdir(repo_path)):
        # Python project - using the current environment's python to run pytest
        # This ensures 'pytest' is found even if it's not in the global PATH
        cmd = [sys.executable, "-m", "pytest", "--verbose", "--tb=short"]
    else:
        return "No recognizable test suite (package.json or .py files) found.", 1

    # 2. Execution & Capture
    try:
        # We use 'cwd' to run the command inside the repo WITHOUT moving our main process
        result = subprocess.run(
            cmd,
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=120,
            # Windows specific: Prevents console window popup and handles shell built-ins
            shell=True if os.name == 'nt' else False 
        )
        
        # Combine stdout and stderr for the AI Analyzer
        full_logs = (result.stdout or "") + "\n" + (result.stderr or "")
        return full_logs, result.returncode
        
    except subprocess.TimeoutExpired:
        return "ERROR: Test execution timed out after 120 seconds. Check for infinite loops.", 1
    except Exception as e:
        return f"ERROR: Unexpected runner failure: {str(e)}", 1