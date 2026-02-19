import subprocess
import os

def discover_and_run_tests(repo_path):
    """
    Automatically detects if the repo is Python or Node 
    and runs the appropriate test suite.
    """
    # Move into the cloned repo directory
    os.chdir(repo_path)
    
    # 1. Detection Logic
    if os.path.exists("package.json"):
        # Node.js project
        cmd = ["npm", "test"]
    elif os.path.exists("requirements.txt") or any(f.endswith(".py") for f in os.listdir(".")):
        # Python project - using pytest as the standard
        cmd = ["pytest", "--verbose"]
    else:
        return "No recognizable test suite (package.json or .py files) found.", 1

    # 2. Execution & Capture
    try:
        # We use capture_output=True to grab the logs for the Analyzer Agent
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        # Combine stdout and stderr because some frameworks report errors in stderr
        full_logs = result.stdout + "\n" + result.stderr
        return full_logs, result.returncode
        
    except subprocess.TimeoutExpired:
        return "ERROR: Test execution timed out after 120 seconds.", 1
    except Exception as e:
        return f"ERROR: Unexpected runner failure: {str(e)}", 1