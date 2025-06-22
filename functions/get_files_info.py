import os

def get_files_info(working_directory, directory=None):
    try:
        if directory and not os.path.realpath(directory).startswith(os.path.realpath(working_directory)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if directory and not os.path.isdir(directory):
            return f'Error: "{directory}" is not a directory'

        directory = directory or working_directory
        result_lines = []

        for entry in os.listdir(directory):
            entry_path = os.path.join(directory, entry)
            file_size = os.path.getsize(entry_path)
            is_dir = os.path.isdir(entry_path)
            result_lines.append(f"- {entry}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(result_lines)

    except Exception as e:
        return f"Error: {str(e)}"
