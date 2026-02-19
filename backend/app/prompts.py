FIX_PROMPT_TEMPLATE = """
You are a Senior DevOps Engineer. 
TASK: Fix the code error provided below.

ERROR LOG:
{error_log}

FILE CONTENT:
{file_content}

INSTRUCTIONS:
1. Identify the exact line causing the {bug_type} error.
2. Provide ONLY the corrected code for that specific block.
3. Do not rewrite the whole file.
4. Ensure the fix follows the project's coding style.

OUTPUT FORMAT (JSON):
{{
  "file": "path/to/file",
  "line": 15,
  "fix": "corrected code snippet",
  "explanation": "brief description of why this was fixed"
}}
"""