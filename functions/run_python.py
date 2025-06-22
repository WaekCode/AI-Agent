import os,subprocess

def run_python_file(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)
        if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        
        if not os.path.exists(full_path):
            return f'Error: File "{file_path}" not found.'
        
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'

        try:
            result = subprocess.run(["python3", full_path],timeout=30, capture_output=True, text=True,cwd=working_directory)
        except subprocess.TimeoutExpired as e:
            return f"Error: executing Python file: {e}"
        

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        

        if not stdout and not stderr:
            return 'No output produced.'
        output = f'STDOUT: {stdout}\nSTDERR: {stderr}'
        if result.returncode != 0:
            output += f"\nProcess exited with code {result.returncode}"
            

        return output
        

        
        

        


    except Exception as e:
        return f"Error: executing Python file: {e}"