import os
def get_files_info(working_directory, directory=None):
    try:
        # Treat None or '.' as working_directory itself
        target_dir = os.path.join(working_directory, directory or '.')

        # Security check: disallow paths outside working_directory
        if not os.path.realpath(target_dir).startswith(os.path.realpath(working_directory)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        result_lines = []
        for entry in os.listdir(target_dir):
            entry_path = os.path.join(target_dir, entry)
            file_size = os.path.getsize(entry_path)
            is_dir = os.path.isdir(entry_path)
            result_lines.append(f"- {entry}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(result_lines)
    except Exception as e:
        return f"Error: {str(e)}"