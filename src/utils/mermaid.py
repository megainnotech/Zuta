import subprocess
import tempfile
import os

def validate_mermaid_syntax(mermaid_code: str) -> str:
    """
    Validates Mermaid syntax by running the @mermaid-js/mermaid-cli (mmdc).
    Writes to a temp file, runs mmdc, and returns empty string if valid, 
    or the error message if invalid.
    """
    if not mermaid_code or not mermaid_code.strip():
        return "Mermaid code is empty."

    # Strip markdown code blocks if present
    if mermaid_code.startswith("```mermaid"):
        mermaid_code = mermaid_code[len("```mermaid"):].strip()
    if mermaid_code.startswith("```"):
        mermaid_code = mermaid_code[3:].strip()
    if mermaid_code.endswith("```"):
        mermaid_code = mermaid_code[:-3].strip()

    # Create temporary files for input and output
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as temp_in:
        temp_in.write(mermaid_code)
        temp_in_path = temp_in.name
    
    temp_out_path = temp_in_path + ".svg"

    try:
        # Run mmdc command
        # --puppeteerConfigFile might be needed if running in restricted docker env
        # but usually mmdc -i <in> -o <out> is enough
        result = subprocess.run(
            ['mmdc', '-i', temp_in_path, '-o', temp_out_path],
            capture_output=True,
            text=True,
            check=False 
        )

        if result.returncode != 0:
            return f"Mermaid CLI Error:\n{result.stderr}\nOutput:\n{result.stdout}"
        
        return "" # Empty string means success
        
    except FileNotFoundError:
        return "Error: 'mmdc' command not found. Ensure @mermaid-js/mermaid-cli is installed."
    except Exception as e:
        return f"Unexpected error during validation: {str(e)}"
    finally:
        # Cleanup temp files
        if os.path.exists(temp_in_path):
            os.remove(temp_in_path)
        if os.path.exists(temp_out_path):
            os.remove(temp_out_path)
