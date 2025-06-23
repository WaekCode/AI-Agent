import os
def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)
        if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        MAX_CHARS = 10000
        with open(full_path, 'r') as f:
            file_contents = f.read()
        
        if len(file_contents) > MAX_CHARS:
            return file_contents[:MAX_CHARS] + f'[...File "{file_path}" truncated at 10000 characters]'    
        else: 
            return file_contents
    
    except Exception as e:
        return f'Error:{e}'