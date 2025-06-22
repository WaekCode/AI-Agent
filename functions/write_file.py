import os

def write_file(working_directory, file_path, content):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(file_path)

        # Make sure the file path is inside the working directory
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Create parent directories if the file does not exist
        if not os.path.exists(os.path.dirname(abs_file_path)):
            os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)


        # Write content to the file (overwrite)
        with open(abs_file_path, 'w', ) as f:
            f.write(content)
      
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {e}'
