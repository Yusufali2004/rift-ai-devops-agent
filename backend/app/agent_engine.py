import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_llm_fix(error_log, file_content, bug_type):
    """
    Sends the error and code to Gemini to get a surgical fix.
    """
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    prompt = f"""
    You are an Autonomous DevOps Repair Agent. 
    BUG TYPE: {bug_type}
    ERROR LOG:
    {error_log}
    
    ORIGINAL FILE CONTENT:
    {file_content}
    
    TASK: Provide a surgical fix for this error.
    RETURN ONLY A JSON OBJECT with these keys:
    - "explanation": brief string
    - "fixed_code": the ENTIRE new content for the file
    
    Strictly output valid JSON.
    """
    
    response = model.generate_content(prompt)
    # Clean up the response if LLM adds markdown backticks
    clean_json = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(clean_json)

def apply_patch(repo_path, relative_file_path, new_content):
    """
    Physically writes the fix to the file system.
    """
    full_path = os.path.join(repo_path, relative_file_path)
    
    # Ensure we don't accidentally write outside the repo (security check)
    if not os.path.abspath(full_path).startswith(os.path.abspath(repo_path)):
        raise PermissionError("Attempted to write outside sandbox!")

    with open(full_path, "w") as f:
        f.write(new_content)
    
    print(f"Successfully patched {relative_file_path}")