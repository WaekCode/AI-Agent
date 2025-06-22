import os
def get_file_content(working_directory, file_path):
    try:
        if not os.path.abspath(file_path).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        
        if not os.path.isfile(file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        MAX_CHARS = 10000


        with open(file_path,'r') as f:
            file_contets = f.read()
        
        if len(file_contets) > MAX_CHARS:
            return file_contets[:MAX_CHARS] + f'[...File "{file_path}" truncated at 10000 characters]'    
        else: 
            return file_contets
    
    except Exception as e:
        return f'Error:{e}'